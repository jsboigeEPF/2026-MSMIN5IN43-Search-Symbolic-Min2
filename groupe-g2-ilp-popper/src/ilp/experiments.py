"""Lance Popper sur toutes les taches de data/popper/<jeu>/<tache>/,
avec quelques variantes de biais, et ecrit results/popper.jsonl
(une ligne JSON par essai, lue par le notebook d'analyse).

Usage, depuis le dossier du groupe :  python -m src.ilp.experiments
"""
import json
import re
import shutil
import tempfile
from pathlib import Path

from src.ilp.run_popper import run_popper
from src.ilp.verify import metriques, verify

RACINE = Path(__file__).resolve().parents[2]          # groupe-g2-ilp-popper/
DATA = RACINE / "data" / "popper"
SORTIE = RACINE / "results" / "popper.jsonl"


def copie_avec_biais(task_dir, modifier):
    """Copie la tache dans un dossier temporaire et modifie son bias.pl."""
    d = Path(tempfile.mkdtemp(prefix="g2_variante_"))
    for f in task_dir.iterdir():
        if f.is_file():
            shutil.copy(f, d / f.name)
    (d / "bias.pl").write_text(modifier((d / "bias.pl").read_text()))
    return d


def max_vars(n):
    def modifier(bias):
        if re.search(r"max_vars\(\d+\)\.", bias):
            return re.sub(r"max_vars\(\d+\)\.", f"max_vars({n}).", bias)
        return bias + f"\nmax_vars({n}).\n"
    return modifier


def sans_sibling(bias):
    return re.sub(r"body_pred\(\s*sibling\s*,\s*2\s*\)\.\s*", "", bias)


def lancer(jeu, tache, variante, task_dir, sortie):
    r = run_popper(task_dir)
    c = verify(task_dir, r["prog"])
    ligne = {
        "jeu": jeu, "tache": tache, "methode": "popper", "variante": variante,
        **metriques(c),
        "taille": r["score"][-1] if r.get("score") else None,   # nb de litteraux
        "temps_s": r["temps_s"], "statut": r["statut"], "modele": r["prog"],
        **{f"test_{k}": v for k, v in c.items()},
    }
    sortie.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    sortie.flush()
    print(f"{jeu}/{tache} [{variante}] {r['statut']}  precision={ligne['precision']}  "
          f"rappel={ligne['rappel']}  temps={r['temps_s']}s\n    {r['prog']}")


def main():
    taches = sorted(p for p in DATA.glob("*/*") if (p / "bias.pl").exists())
    if not taches:
        raise SystemExit(f"Aucune tache dans {DATA} : lancer d'abord src.data.family et src.data.zoo")
    SORTIE.parent.mkdir(exist_ok=True)
    with SORTIE.open("w") as sortie:
        for task_dir in taches:
            jeu, tache = task_dir.parent.name, task_dir.name
            lancer(jeu, tache, "defaut", task_dir, sortie)
            variantes = []
            if jeu == "family":                       # experience sur le biais
                variantes += [(f"max_vars={n}", max_vars(n)) for n in (3, 4)]
            if tache == "uncle":                      # cas d'echec documente
                variantes.append(("sans_sibling", sans_sibling))
            for nom, modifier in variantes:
                d = copie_avec_biais(task_dir, modifier)
                try:
                    lancer(jeu, tache, nom, d, sortie)
                finally:
                    shutil.rmtree(d, ignore_errors=True)
    print(f"\nResultats ecrits dans {SORTIE}")


if __name__ == "__main__":
    main()
