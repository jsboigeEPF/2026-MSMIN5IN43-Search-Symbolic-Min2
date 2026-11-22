"""Tests du membre B : génération, découpage et conversion vers Popper.
Lancer depuis groupe-<nom-court>/ :  pytest -q
"""
import re

import pandas as pd

from src.data import family
from src.data.to_popper import write_popper_task

EX_LINE = re.compile(r"^(pos|neg)\([a-z][a-z0-9_]*\([a-z0-9_,']+\)\)\.$")
FACT_LINE = re.compile(r"^[a-z][a-z0-9_]*\([a-z0-9_,']+\)\.$")


def _code_lines(path):
    return [l for l in path.read_text().splitlines()
            if l.strip() and not l.startswith("%") and not l.startswith(":-")]


def test_to_popper_ecrit_des_fichiers_valides(tmp_path):
    task = {
        "dataset": "mini", "name": "grandparent", "arity": 2,
        "bk": ["parent(alice,bob)", "parent(bob,chloe)"],
        "body_preds": [("parent", 2)],
        "types": {"grandparent": ("person", "person"), "parent": ("person", "person")},
        "bias": {"max_vars": 3, "max_body": 2, "max_clauses": 1, "enable_recursion": False},
        "train": [(("alice", "chloe"), 1), (("bob", "alice"), 0)],
        "test": [(("alice", "bob"), 0)],
    }
    out = write_popper_task(task, tmp_path / "t")
    for name in ("bk.pl", "exs.pl", "bias.pl", "test_exs.pl", "meta.json"):
        assert (out / name).exists()
    assert all(FACT_LINE.match(l) for l in _code_lines(out / "bk.pl"))
    assert _code_lines(out / "exs.pl") == ["pos(grandparent(alice,chloe)).",
                                           "neg(grandparent(bob,alice))."]
    bias = (out / "bias.pl").read_text()
    assert "head_pred(grandparent,2)." in bias and "body_pred(parent,2)." in bias


def test_famille_meme_decoupage_pour_popper_et_baselines(tmp_path, monkeypatch):
    monkeypatch.setattr(family, "POPPER_DIR", tmp_path / "popper")
    monkeypatch.setattr(family, "PROCESSED_DIR", tmp_path / "processed")
    family.build(verbose=False)
    for task in family.TASKS:
        pdir = tmp_path / "popper" / "family" / task
        cdir = tmp_path / "processed" / "family" / task
        # 1) Les exemples de test Popper == les lignes de test.csv
        test_pl = {re.search(r"\((\w+),(\w+)\)\)", l).groups()
                   for l in _code_lines(pdir / "test_exs.pl")}
        test_csv = set(map(tuple, pd.read_csv(cdir / "test.csv")[["x", "y"]].values))
        assert test_pl == test_csv
        # 2) Aucun exemple à la fois en apprentissage et en test
        train_csv = set(map(tuple, pd.read_csv(cdir / "train.csv")[["x", "y"]].values))
        assert not (train_csv & test_csv)
        # 3) Format Prolog valide et des positifs des deux côtés
        lines = _code_lines(pdir / "exs.pl")
        assert all(EX_LINE.match(l) for l in lines)
        assert any(l.startswith("pos") for l in lines)
        assert any(l.startswith("pos") for l in _code_lines(pdir / "test_exs.pl"))


def test_famille_relations_coherentes():
    people, pairs = family.generate_tree()
    rel = family.relations(people, pairs)
    assert 18 <= len(people) <= 26
    # grandparent(X,Y) <=> il existe Z : parent(X,Z), parent(Z,Y)
    for x, y in rel["grandparent"]:
        assert any((x, z) in rel["parent"] and (z, y) in rel["parent"] for z in people)
    # tout grand-parent est un ancêtre, et un oncle est toujours un homme
    assert rel["grandparent"] <= rel["ancestor"]
    assert all(people[x]["sex"] == "m" for x, _ in rel["uncle"])


def test_oncles_et_tantes_des_deux_cotes():
    """Sans oncle maternel ni tante paternelle, Popper ne peut pas distinguer
    male(X) (bonne règle) de male(Z) (le parent est un homme) : on l'interdit."""
    from itertools import permutations
    from src.data.common import split_ids

    people, pairs = family.generate_tree()
    rel = family.relations(people, pairs)
    all_pairs = list(permutations(sorted(people), 2))
    labels = [int(p in rel["uncle"]) for p in all_pairs]
    train, test = split_ids([f"{x}__{y}" for x, y in all_pairs], labels)

    cases = set()
    for x, z in rel["sibling"]:
        for z2, y in rel["parent"]:
            if z == z2:
                part = "train" if f"{x}__{y}" in train else "test"
                cases.add((people[x]["sex"], people[z]["sex"], part))
    for part in ("train", "test"):
        assert ("m", "f", part) in cases, f"aucun oncle maternel en {part}"
        assert ("f", "m", part) in cases, f"aucune tante paternelle en {part}"
