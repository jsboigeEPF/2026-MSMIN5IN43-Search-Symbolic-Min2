"""Réglages partagés : graine, découpage 70/30 et sorties pour les baselines.

RÈGLE D'OR DU PROJET : le découpage est fait UNE SEULE FOIS ici, puis écrit
à la fois pour Popper (.pl) et pour scikit-learn (.csv). Popper et les
baselines voient donc exactement les mêmes exemples d'apprentissage et de test.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42          # graine fixée pour tout le projet
TEST_SIZE = 0.30   # 70 % apprentissage / 30 % test

# Racine du dossier groupe-<nom-court>/ (ce fichier est dans src/data/)
GROUP_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = GROUP_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"              # données téléchargées (ignorées par Git)
PROCESSED_DIR = DATA_DIR / "processed"  # CSV pour les baselines (ignorés par Git)
POPPER_DIR = DATA_DIR / "popper"        # dossiers de tâches Popper (ignorés par Git)


def split_ids(ids, labels, seed: int = SEED, test_size: float = TEST_SIZE):
    """Découpage stratifié : la proportion pos/neg est la même dans train et test."""
    train_ids, test_ids = train_test_split(
        list(ids), test_size=test_size, random_state=seed, stratify=list(labels))
    return set(train_ids), set(test_ids)


def write_baseline_csv(df: pd.DataFrame, train_ids: set, test_ids: set,
                       out_dir: Path, id_col: str = "id") -> None:
    """Écrit train.csv / test.csv (colonnes : id, attributs..., label)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df[df[id_col].isin(train_ids)].to_csv(out_dir / "train.csv", index=False)
    df[df[id_col].isin(test_ids)].to_csv(out_dir / "test.csv", index=False)
