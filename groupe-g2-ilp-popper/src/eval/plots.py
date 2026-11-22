from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Chemins
RESULTS_DIR = Path("results")
CSV_FILE = RESULTS_DIR / "comparaison.csv"
PLOTS_DIR = RESULTS_DIR / "plots"

# Méthodes et ordre d'affichage
METHODES = [
    "popper",
    "tree_full",
    "tree_depth3",
    "forest",
]

NOMS_METHODES = {
    "popper": "Popper",
    "tree_full": "Arbre complet",
    "tree_depth3": "Arbre profondeur 3",
    "forest": "Forêt aléatoire",
}


def charger_resultats():
    """Charge les résultats de comparaison."""
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {CSV_FILE}"
        )

    return pd.read_csv(CSV_FILE)


def tracer_metrique(df, metrique, nom_metrique):
    """Crée un graphique comparant les méthodes pour chaque tâche."""

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    for dataset in df["dataset"].unique():
        donnees = df[df["dataset"] == dataset]

        tableau = donnees.pivot(
            index="task",
            columns="methode",
            values=metrique
        )

        # Garantir le même ordre des méthodes
        tableau = tableau.reindex(columns=METHODES)

        ax = tableau.plot(
            kind="bar",
            figsize=(12, 6),
            width=0.8
        )

        ax.set_title(
            f"Comparaison des méthodes - {dataset.upper()}",
            fontsize=14
        )
        ax.set_xlabel("Tâche")
        ax.set_ylabel(nom_metrique)
        ax.set_ylim(0, 1.05)
        ax.set_xticklabels(
            tableau.index,
            rotation=0
        )

        ax.legend(
            [NOMS_METHODES[m] for m in METHODES],
            title="Méthode"
        )

        ax.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()

        chemin = PLOTS_DIR / f"{dataset}_{metrique}.png"
        plt.savefig(chemin, dpi=300)
        plt.close()

        print(f"Graphique créé : {chemin}")


def main():
    df = charger_resultats()

    tracer_metrique(
        df,
        "f1",
        "Score F1"
    )

    tracer_metrique(
        df,
        "balanced_accuracy",
        "Balanced accuracy"
    )


if __name__ == "__main__":
    main()
