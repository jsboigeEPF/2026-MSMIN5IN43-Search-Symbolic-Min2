# Données du projet G2 (ILP)

Aucune donnée n'est commitée : seuls les scripts qui les produisent le sont.
Tout se régénère en deux commandes, depuis le dossier `groupe-<nom-court>/` :

```bash
python -m src.data.family   # jeu 1 : arbre généalogique synthétique
python -m src.data.zoo      # jeu 2 : UCI Zoo (téléchargé dans data/raw/)
```

## Jeux de données

| Jeu | Type | Tâches | Source | Licence |
|---|---|---|---|---|
| Arbre généalogique | relationnel, synthétique | `grandparent`, `ancestor` (récursif), `uncle` | généré par `src/data/family.py` (graine de l'arbre `TREE_SEED = 91`) | aucune (données créées par nous) |
| Zoo | tabulaire, booléen | une tâche « un contre tous » par classe : `mammal`, `bird`, `fish`, `reptile`, `amphibian`, `insect`, `invertebrate` | [UCI Machine Learning Repository, Zoo (id 111)](https://archive.ics.uci.edu/dataset/111/zoo), R. Forsyth, 1990 | CC BY 4.0 |

Téléchargement de Zoo : via le paquet `ucimlrepo` s'il est installé, sinon directement depuis
`https://archive.ics.uci.edu/static/public/111/zoo.zip`. Si le réseau bloque, télécharger
`zoo.data` à la main et lancer `python -m src.data.zoo --raw chemin/vers/zoo.data`.

## Protocole

- **Découpage 70 % / 30 %**, stratifié, graine `SEED = 42` (`src/data/common.py`).
  Il est fait une seule fois puis écrit pour Popper **et** pour les baselines :
  les deux voient exactement les mêmes exemples.
- **Généalogie** : positifs = toutes les paires (X, Y) vraies ; négatifs = toutes les autres
  paires X ≠ Y (monde clos). Les faits de fond (`parent/2`, `male/1`, `female/1`,
  `sibling/2`) décrivent tout l'arbre ; seules les étiquettes cibles sont découpées.
  `sibling/2` est fourni pour `uncle` : sans lui, Popper ne peut pas exclure le père
  (il faudrait l'inégalité X ≠ Z).
- **Zoo** : un seul découpage (stratifié sur la classe) pour toutes les tâches Zoo.
  Chaque attribut vrai devient un fait (`hair(aardvark).`), le nombre de pattes devient
  `legs_4(aardvark).` ; côté scikit-learn, une colonne par attribut (`legs` numérique).
  Option `--negations` : ajoute `no_hair(x).` etc. pour les attributs faux.
- **Généalogie pour les baselines** : un arbre de décision ne lit pas de relations. On fabrique
  pour chaque paire des colonnes de profondeur 1 seulement (`x_parent_of_y`, `siblings`,
  `common_parent`, sexe, nombre d'enfants, génération, écart de génération…), jamais la
  relation cible elle-même. Cette difficulté fait partie des résultats.

## Correction de l'arbre (graine 21 → 91)

Avec la première graine (21), tous les oncles étaient des frères du père et toutes les tantes des sœurs
de la mère. Popper ne pouvait donc pas distinguer la bonne règle `male(X)` de la règle fausse `male(Z)`
(« le parent est un homme ») : il a appris la seconde, et le test, biaisé de la même façon, ne l'a pas vu.
La graine 91 contient des oncles maternels et des tantes paternelles, en apprentissage et en test
(vérifié par `tests/test_data.py`). Ancienne version, pour l'avant/après :
`python -m src.data.family --tree-seed 21`.

## Fichiers produits (ignorés par Git)

```
data/raw/zoo.data                          fichier UCI brut
data/popper/<jeu>/<tâche>/bk.pl            faits de fond
data/popper/<jeu>/<tâche>/exs.pl           exemples d'apprentissage (pos/neg)
data/popper/<jeu>/<tâche>/bias.pl          biais de langage par défaut
data/popper/<jeu>/<tâche>/test_exs.pl      exemples de test (jamais donnés à Popper)
data/popper/<jeu>/<tâche>/meta.json        graine, effectifs, biais
data/processed/<jeu>/<tâche>/train.csv     mêmes exemples, en tableau, pour scikit-learn
data/processed/<jeu>/<tâche>/test.csv
```

Popper se lance sur un dossier de tâche : `Settings(kbpath='data/popper/family/grandparent')`.
