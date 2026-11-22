"""Jeu 1 : arbre généalogique synthétique (membre B).

Génère un arbre d'une vingtaine de personnes sur 4 générations (graine fixée),
puis 3 tâches : grandparent, ancestor (récursif), uncle.
Pour chaque tâche :
  - exemples positifs = toutes les paires (X,Y) vraies ;
  - exemples négatifs = toutes les autres paires X != Y (hypothèse du monde clos) ;
  - découpage stratifié 70/30 avec la graine du projet ;
  - écriture pour Popper (data/popper/family/<tâche>/) ;
  - écriture pour les baselines (data/processed/family/<tâche>/train.csv, test.csv)
    avec des colonnes fabriquées à partir des paires.

Usage (depuis le dossier groupe-<nom-court>/) :
    python -m src.data.family
"""
from __future__ import annotations

import argparse
import random
from itertools import permutations

import pandas as pd

from .common import POPPER_DIR, PROCESSED_DIR, SEED, split_ids, write_baseline_csv
from .to_popper import write_popper_task

MALE_NAMES = ["arthur", "bruno", "cedric", "david", "emile", "felix", "gaston",
              "hugo", "ivan", "jules", "karim", "louis", "marc", "noah", "oscar",
              "paul", "quentin", "raphael", "simon", "theo"]
FEMALE_NAMES = ["alice", "berthe", "claire", "diane", "elise", "fanny", "gisele",
                "helene", "irene", "jeanne", "katia", "lea", "manon", "nina",
                "olga", "paula", "rose", "sarah", "tina", "zoe"]


# ---------------------------------------------------------------- l'arbre
# Graine de l'ARBRE : ~20 personnes, assez d'oncles, ET des oncles/tantes des deux
# côtés (paternel et maternel) dans l'apprentissage comme dans le test.
# L'ancienne graine 21 n'avait que des oncles paternels : voir data/README.md.
# Elle est distincte de SEED, qui sert au découpage 70/30.
TREE_SEED = 91


def generate_tree(seed: int = TREE_SEED, n_generations: int = 4, max_couples_per_gen: int = 3):
    """Renvoie (people, parent_pairs).

    people : dict nom -> {"sex": "m"/"f", "gen": 0..3}
    parent_pairs : liste de (parent, enfant)
    """
    rng = random.Random(seed)
    males, females = MALE_NAMES[:], FEMALE_NAMES[:]
    rng.shuffle(males)
    rng.shuffle(females)

    people: dict[str, dict] = {}
    parent_pairs: list[tuple[str, str]] = []

    def new_person(sex: str, gen: int) -> str:
        name = (males if sex == "m" else females).pop()
        people[name] = {"sex": sex, "gen": gen}
        return name

    # Génération 0 : un couple fondateur
    couples = [(new_person("m", 0), new_person("f", 0))]

    for gen in range(1, n_generations):
        children_of_gen = []
        for father, mother in couples:
            n_children = rng.choice([2, 3])
            for _ in range(n_children):
                child = new_person(rng.choice("mf"), gen)
                parent_pairs += [(father, child), (mother, child)]
                children_of_gen.append(child)
        if gen == n_generations - 1:
            break
        # Certains enfants se marient avec une personne extérieure (sans parents connus)
        rng.shuffle(children_of_gen)
        couples = []
        for child in children_of_gen[:max_couples_per_gen]:
            if people[child]["sex"] == "m":
                couples.append((child, new_person("f", gen)))
            else:
                couples.append((new_person("m", gen), child))
    return people, parent_pairs


# ---------------------------------------------------------------- relations
def relations(people, parent_pairs):
    parent = set(parent_pairs)
    children = {p: {c for (x, c) in parent if x == p} for p in people}
    parents_of = {c: {p for (p, x) in parent if x == c} for c in people}

    grandparent = {(x, y) for (x, z) in parent for (z2, y) in parent if z == z2}

    ancestor = set(parent)  # fermeture transitive
    while True:
        new = {(x, y) for (x, z) in ancestor for (z2, y) in parent if z == z2} - ancestor
        if not new:
            break
        ancestor |= new

    sibling = {(a, b) for a in people for b in people
               if a != b and parents_of[a] & parents_of[b]}
    uncle = {(x, y) for (x, z) in sibling for (z2, y) in parent
             if z == z2 and people[x]["sex"] == "m"}

    return {"parent": parent, "grandparent": grandparent, "ancestor": ancestor,
            "sibling": sibling, "uncle": uncle,
            "children": children, "parents_of": parents_of}


def bk_facts(people, rel):
    facts = [f"parent({p},{c})" for p, c in rel["parent"]]
    facts += [f"{'male' if d['sex'] == 'm' else 'female'}({n})" for n, d in people.items()]
    facts += [f"sibling({a},{b})" for a, b in rel["sibling"]]
    return facts


# ---------------------------------------------------------------- tâches
TASKS = {
    # nom : (prédicats autorisés dans le corps, biais par défaut)
    "grandparent": ([("parent", 2)],
                    {"max_vars": 3, "max_body": 2, "max_clauses": 1, "enable_recursion": False}),
    "ancestor": ([("parent", 2)],
                 {"max_vars": 3, "max_body": 2, "max_clauses": 2, "enable_recursion": True}),
    "uncle": ([("parent", 2), ("sibling", 2), ("male", 1), ("female", 1)],
              {"max_vars": 3, "max_body": 3, "max_clauses": 1, "enable_recursion": False}),
}
TYPES = {"parent": ("person", "person"), "sibling": ("person", "person"),
         "male": ("person",), "female": ("person",)}


def pair_features(people, rel, x, y) -> dict:
    """Colonnes « à plat » pour les baselines : uniquement des relations directes
    (profondeur 1) entre X et Y, jamais la relation cible elle-même."""
    return {
        "x_parent_of_y": int((x, y) in rel["parent"]),
        "y_parent_of_x": int((y, x) in rel["parent"]),
        "siblings": int((x, y) in rel["sibling"]),
        "common_parent": int(bool(rel["parents_of"][x] & rel["parents_of"][y])),
        "x_male": int(people[x]["sex"] == "m"),
        "y_male": int(people[y]["sex"] == "m"),
        "x_nb_children": len(rel["children"][x]),
        "y_nb_children": len(rel["children"][y]),
        "x_has_parents": int(bool(rel["parents_of"][x])),
        "y_has_parents": int(bool(rel["parents_of"][y])),
        "x_generation": people[x]["gen"],
        "y_generation": people[y]["gen"],
        "generation_gap": people[y]["gen"] - people[x]["gen"],
    }


def build(seed: int = SEED, tree_seed: int = TREE_SEED, verbose: bool = True):
    people, parent_pairs = generate_tree(tree_seed)
    rel = relations(people, parent_pairs)
    facts = bk_facts(people, rel)
    all_pairs = list(permutations(sorted(people), 2))

    if verbose:
        print(f"Arbre : {len(people)} personnes, {len(parent_pairs)} liens parent, "
              f"{max(d['gen'] for d in people.values()) + 1} générations")

    for task_name, (body_preds, bias) in TASKS.items():
        positives = rel[task_name]
        labels = [int(p in positives) for p in all_pairs]
        ids = [f"{x}__{y}" for x, y in all_pairs]
        train_ids, test_ids = split_ids(ids, labels, seed=seed)

        examples = list(zip(all_pairs, labels, ids))
        task = {
            "dataset": "family",
            "name": task_name,
            "arity": 2,
            "bk": facts,
            "body_preds": body_preds,
            "types": {task_name: ("person", "person"),
                      **{p: TYPES[p] for p, _ in body_preds}},
            "bias": bias,
            "train": [(pair, lab) for pair, lab, i in examples if i in train_ids],
            "test": [(pair, lab) for pair, lab, i in examples if i in test_ids],
        }
        write_popper_task(task, POPPER_DIR / "family" / task_name,
                          extra_meta={"seed": seed, "tree_seed": tree_seed, "n_people": len(people)})

        rows = [{"id": i, "x": x, "y": y, **pair_features(people, rel, x, y), "label": lab}
                for (x, y), lab, i in examples]
        write_baseline_csv(pd.DataFrame(rows), train_ids, test_ids,
                           PROCESSED_DIR / "family" / task_name)
        if verbose:
            print(f"  {task_name:12s} pos={sum(labels):3d} neg={len(labels) - sum(labels):3d} "
                  f"| train={len(train_ids)} test={len(test_ids)}")
    return people, rel


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=SEED, help="graine du découpage 70/30")
    ap.add_argument("--tree-seed", type=int, default=TREE_SEED, help="graine de l'arbre")
    a = ap.parse_args()
    build(a.seed, a.tree_seed)
