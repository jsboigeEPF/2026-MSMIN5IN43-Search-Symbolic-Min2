import json
from pathlib import Path

import pandas as pd

from src.eval.metrics import calculer_metriques


# Racine du projet
ROOT = Path(__file__).resolve().parents[2]

FICHIER_POPPER = ROOT / "results" / "popper.jsonl"
FICHIER_BASELINES = ROOT / "results" / "baselines.json"
FICHIER_SORTIE = ROOT / "results" / "comparaison.csv"


def charger_popper():
    """Charge les résultats Popper en conservant uniquement les expériences
    par défaut réussies.
    """
    resultats = []

    with open(FICHIER_POPPER, encoding="utf-8") as fichier:
        for ligne in fichier:
            resultat = json.loads(ligne)

            if resultat["variante"] != "defaut":
                continue

            if resultat["statut"] != "ok":
                continue

            confusion = {
                "tp": resultat["test_tp"],
                "fp": resultat["test_fp"],
                "tn": resultat["test_tn"],
                "fn": resultat["test_fn"],
            }

            metriques = calculer_metriques(confusion)

            resultats.append({
                "dataset": resultat["jeu"],
                "task": resultat["tache"],
                "methode": "popper",
                **metriques,
                "taille": resultat["taille"],
                "unite_taille": "litteraux",
                "temps_s": resultat["temps_s"],
                "statut": resultat["statut"],
            })

    return resultats


def charger_baselines():
    """Charge les résultats des arbres de décision et de la forêt."""
    with open(FICHIER_BASELINES, encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    resultats = []

    for resultat in donnees["results"]:
        confusion = {
            "tp": resultat["tp"],
            "fp": resultat["fp"],
            "tn": resultat["tn"],
            "fn": resultat["fn"],
        }

        metriques = calculer_metriques(confusion)

        methode = resultat["method"]

        if methode == "forest":
            unite_taille = "noeuds_total_100_arbres"
        else:
            unite_taille = "noeuds"
            
        resultats.append({
            "dataset": resultat["dataset"],
            "task": resultat["task"],
            "methode": methode,
            **metriques,
            "taille": resultat["size"],
            "unite_taille": unite_taille,
            "temps_s": resultat["train_time_s"],
            "statut": "ok",
        })

    return resultats


def generer_comparaison():
    """Fusionne les résultats et exporte un CSV."""
    resultats = charger_popper() + charger_baselines()

    df = pd.DataFrame(resultats)

    df = df.sort_values(
        by=["dataset", "task", "methode"]
    ).reset_index(drop=True)

    FICHIER_SORTIE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FICHIER_SORTIE, index=False, encoding="utf-8-sig")

    colonnes = [
        "dataset",
        "task",
        "methode",
        "precision",
        "rappel",
        "exactitude",
        "f1",
        "balanced_accuracy",
        "taille",
        "unite_taille",
        "temps_s",
    ]

    print("\n=== COMPARAISON DES MÉTHODES ===\n")
    print(df[colonnes].to_string(index=False))

    print(f"\nFichier créé : {FICHIER_SORTIE}")

    return df


if __name__ == "__main__":
    generer_comparaison()
