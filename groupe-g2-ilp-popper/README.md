# Apprentissage inductif logique avec Popper — Groupe G2

## 1. Présentation du projet

Ce projet a pour objectif d'étudier l'apprentissage inductif logique (*Inductive Logic Programming*, ILP) à travers l'utilisation de **Popper**.

L'objectif est de découvrir automatiquement des règles logiques à partir d'exemples positifs et négatifs, puis de comparer les performances de cette approche à celles de méthodes classiques d'apprentissage automatique.

Deux jeux de données sont utilisés :

- **Family** : données généalogiques permettant d'apprendre des relations entre individus, notamment `grandparent`, `ancestor` et `uncle`.
- **Zoo** : données décrivant les caractéristiques de différentes espèces animales, avec une classification en sept catégories.

Les performances de Popper sont comparées à trois méthodes de référence :
- Arbre de décision complet.
- Arbre de décision limité à une profondeur de 3.
- Forêt aléatoire composée de 100 arbres.

Le projet étudie à la fois les performances prédictives, les temps d'apprentissage, la complexité des modèles et leur interprétabilité.

**Groupe :** G2  
**Membres :** LEHEC Emma, SEIF Serena, AMBROSI Mila  
**Formation :** EPF — Projet d'intelligence artificielle

---

## 2. Architecture du projet

L'organisation du dépôt est la suivante :

```text
groupe-g2-ilp-popper/
│
├── src/
│   ├── data/
│   │   ├── family.py
│   │   ├── zoo.py
│   │   └── to_popper.py
│   │
│   ├── ilp/
│   │   ├── experiments.py
│   │   ├── run_popper.py
│   │   └── verify.py
│   │
│   ├── baselines/
│   │   └── train.py
│   │
│   └── eval/
│       ├── metrics.py
│       ├── compare.py
│       └── plots.py
│
├── tests/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── popper/
│
├── results/
│   ├── popper.jsonl
│   ├── baselines.json
│   ├── comparaison.csv
│   └── graphiques/
│
├── requirements.txt
├── .env.example
└── README.md
```

### Rôle des principaux modules

| Module | Fonction |
|---|---|
| `src/data/` | Chargement, préparation et conversion des jeux de données |
| `src/ilp/` | Exécution de Popper et vérification indépendante des programmes appris |
| `src/baselines/` | Entraînement des méthodes de référence |
| `src/eval/` | Calcul des métriques, comparaison et génération des graphiques |
| `tests/` | Tests automatisés des principales fonctionnalités |
| `results/` | Résultats des expériences et comparaisons |

Les fichiers intermédiaires générés dans `data/` sont reconstruits à partir des scripts de préparation des données.

---

## 3. Installation

### Prérequis

Le projet nécessite :

- Python 3.12 ou une version compatible.
- SWI-Prolog.
- pip.
- Git.

### Installation de SWI-Prolog

Sur Ubuntu ou WSL Ubuntu :

```bash
sudo apt update
sudo apt install swi-prolog
```

Vérifier l'installation :

```bash
swipl --version
```

### Création de l'environnement Python

Cloner le dépôt :

```bash
git clone https://github.com/EmmaLehec/fork_2026-MSMIN5IN43-Search-Symbolic-Min2.git
cd groupe-g2-ilp-popper
```

Créer et activer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Utilisation du projet

Les commandes suivantes sont à exécuter depuis la racine du dépôt, avec l'environnement virtuel activé.

### 4.1. Génération des jeux de données

Générer les données généalogiques :

```bash
python -m src.data.family
```

Générer les données Zoo :

```bash
python -m src.data.zoo
```

Les deux générateurs réalisent un découpage stratifié entre apprentissage et test, avec une proportion de 70 % pour l'apprentissage et 30 % pour le test.

La graine utilisée pour le découpage est fixée à 42. Pour Family, la génération de l'arbre utilise également une graine dédiée, fixée à 91.

Les données sont ensuite converties au format nécessaire à Popper et au format tabulaire utilisé par les méthodes de référence.

### 4.2. Exécution de Popper

Lancer les expériences sur l'ensemble des tâches :

```bash
python -m src.ilp.experiments
```

Les résultats sont enregistrés dans :

```text
results/popper.jsonl
```

Chaque ligne correspond à une expérience et contient notamment :
- Le jeu de données et la tâche.
- La variante du biais d'apprentissage.
- Les métriques calculées.
- Le programme logique appris.
- Le temps d'exécution.
- La matrice de confusion sur les exemples de test.

### 4.3. Entraînement des méthodes de référence

Lancer les méthodes de comparaison :

```bash
python -m src.baselines.train
```

Les résultats sont enregistrés dans :

```text
results/baselines.json
```

Les trois méthodes entraînées sont :
- Un arbre de décision sans limite de profondeur.
- Un arbre de décision de profondeur maximale 3.
- Une forêt aléatoire de 100 arbres.

### 4.4. Comparaison des résultats

Générer le tableau comparatif :

```bash
python -m src.eval.compare
```

Le fichier produit est :

```text
results/comparaison.csv
```

Il rassemble les résultats des différentes méthodes et des différentes tâches.

### 4.5. Génération des graphiques

```bash
python -m src.eval.plots
```

Les graphiques permettent de comparer les performances des méthodes sur Family et Zoo, notamment à travers le F1-score et la balanced accuracy.

---

## 5. Évaluation des performances

Plusieurs métriques sont utilisées pour évaluer les modèles :

| Métrique | Signification |
|---|---|
| Précision | Proportion de prédictions positives correctes parmi les prédictions positives |
| Rappel | Proportion d'exemples positifs correctement identifiés |
| F1-score | Moyenne harmonique de la précision et du rappel |
| Exactitude (*Accuracy*) | Proportion totale de prédictions correctes |
| Spécificité | Proportion de négatifs correctement identifiés |
| Balanced accuracy | Moyenne du rappel et de la spécificité |

L'utilisation de plusieurs métriques est importante, notamment pour Zoo, où certaines classes sont moins représentées que d'autres.

### Principaux résultats

Sur Family, Popper obtient un F1-score de 1 pour les trois tâches étudiées.

Sur Zoo, il obtient également un F1-score de 1 pour les classes suivantes :
- Bird
- Fish
- Insect
- Mammal

Ses performances sont plus faibles pour :
- Amphibian : F1-score de 0.
- Invertebrate : F1-score de 0,50.
- Reptile : F1-score de 0.

Les méthodes classiques présentent des résultats globalement plus réguliers sur Zoo.

### Temps d'exécution

Les temps moyens d'apprentissage observés sont :

| Méthode | Family | Zoo |
|---|---:|---:|
| Popper | 0,2400 s | 0,2514 s |
| Arbre profondeur 3 | 0,0017 s | 0,0013 s |
| Arbre complet | 0,0109 s | 0,0015 s |
| Forêt aléatoire | 0,0912 s | 0,0866 s |

Les arbres de décision sont les plus rapides dans les expériences réalisées. Popper présente un temps d'apprentissage supérieur, mais produit des règles logiques explicites.

### Complexité des modèles

La complexité est mesurée différemment selon les méthodes :
- Popper : nombre de littéraux dans le programme logique.
- Arbres de décision : nombre de nœuds.
- Forêt aléatoire : nombre total de nœuds des 100 arbres.

Ces unités ne sont pas directement comparables. Elles permettent néanmoins de caractériser la taille des modèles produits.

---

## 6. Tests

Les tests automatisés sont exécutés avec pytest :

```bash
python -m pytest -v
```

Ils couvrent notamment :
- La préparation et la conversion des données.
- Les relations généalogiques.
- Le calcul des métriques.
- La vérification indépendante des programmes logiques.
- Une exécution de contrôle de Popper.

Lors de la dernière exécution documentée, les 12 tests ont réussi.

---

## 7. Limites et perspectives

Plusieurs limites doivent être prises en compte dans l'interprétation des résultats.

**Taille des jeux de données**

Les jeux de données utilisés sont relativement petits : 24 individus pour Family et 101 animaux pour Zoo. Certaines classes sont peu représentées dans les données de test, ce qui rend leurs métriques sensibles à quelques erreurs.

**Biais d'apprentissage**

Les performances de Popper dépendent de la représentation des connaissances et des contraintes définies dans son biais. Des contraintes trop restrictives peuvent empêcher la découverte de règles suffisamment générales.

**Généralisation**

Certaines règles apprises sur Zoo ne permettent pas de reconnaître tous les exemples positifs du jeu de test. Des expérimentations complémentaires seraient nécessaires pour mieux étudier leur capacité de généralisation.

**Comparaison de la complexité**

Les unités de mesure des modèles diffèrent selon les méthodes. Une comparaison numérique directe entre littéraux et nœuds ne permet donc pas de conclure objectivement sur la simplicité des modèles.

**Perspectives**

Plusieurs améliorations pourraient être envisagées :
- Utiliser des jeux de données plus volumineux.
- Réaliser plusieurs découpages apprentissage/test ou une validation croisée.
- Étudier l'influence des paramètres du biais de Popper.
- Enrichir les connaissances de fond.
- Analyser plus précisément les erreurs de classification.

---

## 8. Répartition du travail

| Membre | Contributions |
|---|---|
| LEHEC Emma  | Préparation des données et représentation des connaissances |
| SEIF Serena | Apprentissage inductif logique avec Popper|
| Ambrosi Mila | Évaluation, comparaison et analyse des résultats |

---

## 9. Références et licences

- **Popper** : outil d'apprentissage inductif logique utilisé pour découvrir des programmes logiques.
- **UCI Zoo Dataset** : jeu de données Zoo, disponible auprès de l'UCI Machine Learning Repository, sous licence CC BY 4.0.
- **scikit-learn** : bibliothèque utilisée pour les arbres de décision et les forêts aléatoires.
- **SWI-Prolog** : moteur Prolog utilisé dans l'exécution de Popper.

Les licences des bibliothèques et des ressources utilisées doivent être respectées conformément à leurs distributions respectives.
