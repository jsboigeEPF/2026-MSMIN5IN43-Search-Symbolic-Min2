"""Étape 6 : les baselines (membre B).

Pour chaque tâche déjà préparée à l'étape 4 (data/processed/<jeu>/<tâche>/),
on entraîne 3 modèles sur train.csv et on les évalue sur test.csv :

  - tree_full    : arbre de décision, profondeur libre (réglages par défaut)
  - tree_depth3  : arbre de décision limité à max_depth=3 (version « lisible »)
  - forest       : forêt aléatoire (100 arbres, réglages par défaut)

Tous avec random_state=0. Mêmes exemples, même découpage que Popper.

Pour chaque (jeu, tâche, méthode) on enregistre dans results/baselines.json :
précision, rappel, exactitude, F1, matrice de confusion, taille (nœuds),
profondeur, temps d'apprentissage, et l'arbre exporté en texte (lisibilité).

Usage (depuis groupe-<nom-court>/, APRÈS l'étape 4) :
    python -m src.baselines.train
    python -m src.baselines.train --datasets family
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.tree import DecisionTreeClassifier, export_text

from src.data.common import GROUP_ROOT, PROCESSED_DIR, SEED

RESULTS_FILE = GROUP_ROOT / "results" / "baselines.json"
RANDOM_STATE = 0
# Colonnes qui ne sont PAS des attributs : identifiants et étiquette
NON_FEATURES = {"id", "x", "y", "label"}


def make_models():
    return {
        "tree_full": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "tree_depth3": DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE),
        "forest": RandomForestClassifier(random_state=RANDOM_STATE),
    }


def load_task(task_dir: Path):
    train = pd.read_csv(task_dir / "train.csv")
    test = pd.read_csv(task_dir / "test.csv")
    features = [c for c in train.columns if c not in NON_FEATURES]
    return train[features], train["label"], test[features], test["label"], features


def model_size(model) -> dict:
    """Taille = nombre de nœuds (arbre) ou somme des nœuds de tous les arbres (forêt)."""
    if isinstance(model, RandomForestClassifier):
        trees = [est.tree_ for est in model.estimators_]
        return {"size": int(sum(t.node_count for t in trees)),
                "n_trees": len(trees),
                "depth": int(max(t.max_depth for t in trees)),
                "n_leaves": int(sum(t.n_leaves for t in trees))}
    t = model.tree_
    return {"size": int(t.node_count), "n_trees": 1,
            "depth": int(t.max_depth), "n_leaves": int(t.n_leaves)}


def evaluate(y_true, y_pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
    }


def run_task(dataset: str, task: str, task_dir: Path) -> list[dict]:
    X_tr, y_tr, X_te, y_te, features = load_task(task_dir)
    records = []
    for method, model in make_models().items():
        start = time.perf_counter()
        model.fit(X_tr, y_tr)
        train_time = time.perf_counter() - start
        rec = {
            "dataset": dataset,
            "task": task,
            "method": method,
            "params": {k: v for k, v in model.get_params().items()
                       if k in ("max_depth", "n_estimators", "random_state")},
            **evaluate(y_te, model.predict(X_te)),
            "train_accuracy": float(accuracy_score(y_tr, model.predict(X_tr))),
            **model_size(model),
            "train_time_s": round(train_time, 4),
            "n_train": int(len(y_tr)),
            "n_test": int(len(y_te)),
            "n_features": len(features),
        }
        # La forêt (100 arbres) n'est pas lisible : on n'exporte que les arbres seuls.
        if method != "forest":
            rec["model_text"] = export_text(model, feature_names=features)
        records.append(rec)
    return records


def main(datasets=None, out_file: Path = RESULTS_FILE, processed_dir: Path = PROCESSED_DIR):
    if not processed_dir.exists():
        raise SystemExit("Pas de données : lancez d'abord python -m src.data.family "
                         "et python -m src.data.zoo")
    results = []
    for ds_dir in sorted(p for p in processed_dir.iterdir() if p.is_dir()):
        if datasets and ds_dir.name not in datasets:
            continue
        for task_dir in sorted(p for p in ds_dir.iterdir() if p.is_dir()):
            for r in run_task(ds_dir.name, task_dir.name, task_dir):
                results.append(r)
                print(f"{r['dataset']:7s} {r['task']:13s} {r['method']:12s} "
                      f"P={r['precision']:.2f} R={r['recall']:.2f} "
                      f"Acc={r['accuracy']:.2f} taille={r['size']:5d} "
                      f"t={r['train_time_s']:.3f}s")

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "split_seed": SEED,
        "model_random_state": RANDOM_STATE,
        "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(results)} résultats écrits dans {out_file}")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets", nargs="*", help="ex. --datasets family zoo")
    main(ap.parse_args().datasets)
