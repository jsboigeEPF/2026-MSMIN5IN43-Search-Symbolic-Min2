import pytest

from src.eval.metrics import calculer_metriques


def test_metriques_classification_normale():
    confusion = {
        "tp": 8,
        "fp": 2,
        "tn": 9,
        "fn": 1,
    }

    resultat = calculer_metriques(confusion)

    assert resultat["precision"] == pytest.approx(0.8)
    assert resultat["rappel"] == pytest.approx(8 / 9)
    assert resultat["exactitude"] == pytest.approx(17 / 20)
    assert resultat["specificite"] == pytest.approx(9 / 11)
    assert resultat["f1"] == pytest.approx(16 / 19)
    assert resultat["balanced_accuracy"] == pytest.approx(
        ((8 / 9) + (9 / 11)) / 2
    )


def test_metriques_sans_prediction_positive():
    confusion = {
        "tp": 0,
        "fp": 0,
        "tn": 10,
        "fn": 2,
    }

    resultat = calculer_metriques(confusion)

    assert resultat["precision"] == 0.0
    assert resultat["rappel"] == 0.0
    assert resultat["specificite"] == 1.0
    assert resultat["f1"] == 0.0
    assert resultat["exactitude"] == pytest.approx(10 / 12)
    assert resultat["balanced_accuracy"] == 0.5


def test_metriques_matrice_vide():
    confusion = {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
    }

    resultat = calculer_metriques(confusion)

    for valeur in resultat.values():
        assert valeur == 0.0
