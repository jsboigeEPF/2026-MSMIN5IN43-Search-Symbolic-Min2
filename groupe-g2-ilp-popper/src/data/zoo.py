"""Jeu 2 : UCI Zoo (membre B).

101 animaux, 16 attributs (15 booléens + nombre de pattes), 7 classes.
Source : https://archive.ics.uci.edu/dataset/111/zoo - licence CC BY 4.0.
Le fichier n'est PAS commité : ce script le télécharge dans data/raw/.

Pour chaque classe (mammal, bird, fish...) on crée une tâche « un contre tous » :
  pos(mammal(aardvark)).  neg(mammal(chicken)).
Un SEUL découpage 70/30 (stratifié sur la classe) sert à toutes les tâches Zoo,
pour Popper comme pour les baselines.

Encodage « même information des deux côtés » :
  - attribut booléen vrai  -> fait Prolog  hair(aardvark).   | colonne hair = 1
  - nombre de pattes       -> fait Prolog  legs_4(aardvark). | colonne legs = 4
  (legs_4/1 plutôt que legs/2 : Popper gère mal les constantes numériques,
   et chaque valeur de pattes devient un prédicat lisible.)
  - option --negations : ajoute aussi no_hair(x). quand l'attribut est faux
    (Popper ne sait pas dire « n'a PAS de plumes » sans ces faits).

Usage (depuis le dossier groupe-<nom-court>/) :
    python -m src.data.zoo
    python -m src.data.zoo --raw chemin/vers/zoo.data   # fichier déjà téléchargé
    python -m src.data.zoo --negations
"""
from __future__ import annotations

import argparse
import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from .common import POPPER_DIR, PROCESSED_DIR, RAW_DIR, SEED, split_ids, write_baseline_csv
from .to_popper import write_popper_task

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/111/zoo.zip"
COLUMNS = ["animal_name", "hair", "feathers", "eggs", "milk", "airborne", "aquatic",
           "predator", "toothed", "backbone", "breathes", "venomous", "fins", "legs",
           "tail", "domestic", "catsize", "type"]
BOOL_ATTRS = [c for c in COLUMNS[1:-1] if c != "legs"]
CLASSES = {1: "mammal", 2: "bird", 3: "reptile", 4: "fish",
           5: "amphibian", 6: "insect", 7: "invertebrate"}
DEFAULT_BIAS = {"max_vars": 1, "max_body": 3, "max_clauses": 2, "enable_recursion": False}


# ---------------------------------------------------------------- téléchargement
def download(raw_dir: Path = RAW_DIR) -> Path:
    """Télécharge zoo.data dans data/raw/ (une seule fois) et renvoie son chemin."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / "zoo.data"
    if target.exists():
        return target
    try:  # 1) via le paquet officiel ucimlrepo s'il est installé
        from ucimlrepo import fetch_ucirepo
        df = fetch_ucirepo(id=111).data.original
        df[COLUMNS].to_csv(target, header=False, index=False)
        print("Zoo téléchargé avec ucimlrepo")
    except Exception as exc:  # 2) sinon, directement depuis l'archive UCI
        print(f"ucimlrepo indisponible ({exc.__class__.__name__}), téléchargement direct...")
        with urllib.request.urlopen(UCI_ZIP_URL, timeout=60) as resp:
            archive = zipfile.ZipFile(io.BytesIO(resp.read()))
        target.write_bytes(archive.read("zoo.data"))
    return target


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=COLUMNS)
    # Noms uniques et valides en Prolog (le jeu contient deux « frog »)
    names, seen = [], {}
    for raw in df["animal_name"].astype(str).str.strip().str.lower():
        base = "".join(ch if ch.isalnum() else "_" for ch in raw)
        if not base[0].isalpha():
            base = "a_" + base
        seen[base] = seen.get(base, 0) + 1
        names.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    df["animal_name"] = names
    return df


# ---------------------------------------------------------------- conversion
def bk_facts(df: pd.DataFrame, negations: bool = False) -> list[str]:
    facts = []
    for _, row in df.iterrows():
        a = row["animal_name"]
        for attr in BOOL_ATTRS:
            if row[attr] == 1:
                facts.append(f"{attr}({a})")
            elif negations:
                facts.append(f"no_{attr}({a})")
        facts.append(f"legs_{int(row['legs'])}({a})")
    return facts


def build(raw: Path | None = None, negations: bool = False, seed: int = SEED,
          classes: list[str] | None = None, verbose: bool = True):
    df = load(Path(raw) if raw else download())
    facts = bk_facts(df, negations)
    body_preds = sorted({(f.split("(")[0], 1) for f in facts})

    # Un seul découpage pour toutes les classes, stratifié sur le type
    train_ids, test_ids = split_ids(df["animal_name"], df["type"], seed=seed)
    if verbose:
        print(f"Zoo : {len(df)} animaux, {len(body_preds)} prédicats de fond, "
              f"train={len(train_ids)} test={len(test_ids)}")

    wanted = classes or list(CLASSES.values())
    for type_id, cls in CLASSES.items():
        if cls not in wanted:
            continue
        labels = (df["type"] == type_id).astype(int)
        examples = [((name,), int(lab)) for name, lab in zip(df["animal_name"], labels)]
        task = {
            "dataset": "zoo",
            "name": cls,
            "arity": 1,
            "bk": facts,
            "body_preds": body_preds,
            "types": {cls: ("animal",), **{p: ("animal",) for p, _ in body_preds}},
            "bias": DEFAULT_BIAS,
            "train": [e for e in examples if e[0][0] in train_ids],
            "test": [e for e in examples if e[0][0] in test_ids],
        }
        write_popper_task(task, POPPER_DIR / "zoo" / cls,
                          extra_meta={"seed": seed, "negations": negations})

        table = df[["animal_name"] + COLUMNS[1:-1]].rename(columns={"animal_name": "id"})
        table = table.assign(label=labels.values)
        write_baseline_csv(table, train_ids, test_ids, PROCESSED_DIR / "zoo" / cls)
        if verbose:
            print(f"  {cls:13s} pos={int(labels.sum()):3d} neg={int(len(labels) - labels.sum()):3d}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", type=Path, help="fichier zoo.data local (sinon téléchargement)")
    ap.add_argument("--negations", action="store_true", help="ajoute les faits no_<attribut>")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--classes", nargs="*", help="ex. --classes mammal bird fish")
    a = ap.parse_args()
    build(a.raw, a.negations, a.seed, a.classes)
