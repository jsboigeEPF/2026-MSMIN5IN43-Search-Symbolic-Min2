"""Test du membre B pour l'étape 6 : les baselines tournent et écrivent un JSON complet."""
import json

from src.baselines import train
from src.data import family

EXPECTED_KEYS = {"dataset", "task", "method", "precision", "recall", "accuracy",
                 "size", "train_time_s", "tp", "fp", "tn", "fn"}


def test_baselines_sur_la_genealogie(tmp_path, monkeypatch):
    # 1) Données de l'étape 4 dans un dossier temporaire
    monkeypatch.setattr(family, "POPPER_DIR", tmp_path / "popper")
    monkeypatch.setattr(family, "PROCESSED_DIR", tmp_path / "processed")
    family.build(verbose=False)

    # 2) Baselines sur ces données
    out = tmp_path / "baselines.json"
    train.main(datasets=["family"], out_file=out, processed_dir=tmp_path / "processed")

    results = json.loads(out.read_text())["results"]
    assert len(results) == 3 * len(family.TASKS)          # 3 méthodes x 3 tâches
    for r in results:
        assert EXPECTED_KEYS <= r.keys()
        assert 0.0 <= r["precision"] <= 1.0 and 0.0 <= r["recall"] <= 1.0
        assert r["tp"] + r["fp"] + r["tn"] + r["fn"] == r["n_test"]
        assert r["size"] >= 1
    # L'arbre limité est bien plus petit que la forêt, et il est exporté en texte
    by = {(r["task"], r["method"]): r for r in results}
    assert by[("grandparent", "tree_depth3")]["depth"] <= 3
    assert by[("grandparent", "tree_depth3")]["size"] < by[("grandparent", "forest")]["size"]
    assert "class" in by[("grandparent", "tree_depth3")]["model_text"]
