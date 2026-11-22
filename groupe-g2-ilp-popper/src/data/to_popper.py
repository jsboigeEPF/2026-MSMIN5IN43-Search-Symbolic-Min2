"""Conversion d'une tâche vers le format Popper (membre B).

Une « tâche » est décrite par un dictionnaire Python commun aux deux jeux :

    task = {
        "dataset": "family",              # nom du jeu
        "name": "grandparent",            # nom du prédicat cible
        "arity": 2,                       # arité du prédicat cible
        "bk": ["parent(ann,bob)", ...],   # faits de fond (sans le point final)
        "body_preds": [("parent", 2)],    # prédicats que Popper peut utiliser
        "types": {"parent": ("person", "person"), ...},
        "bias": {"max_vars": 3, "max_body": 2, "max_clauses": 1,
                 "enable_recursion": False},
        "train": [(("ann", "carl"), 1), (("bob", "ann"), 0), ...],
        "test":  [...],                   # même format, jamais vu par Popper
    }

`write_popper_task(task, out_dir)` écrit dans out_dir :
    bk.pl        faits de fond
    exs.pl       exemples d'APPRENTISSAGE  pos(...). / neg(...).
    bias.pl      biais de langage
    test_exs.pl  exemples de TEST (même format que exs.pl, pour verify.py du membre A)
    meta.json    graine, tailles, réglages (traçabilité)

Popper ne lit que bk.pl, exs.pl et bias.pl : test_exs.pl est ignoré par lui.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_ATOM_OK = re.compile(r"^[a-z][a-zA-Z0-9_]*$")


def atom(value) -> str:
    """Transforme une valeur Python en constante Prolog valide."""
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if _ATOM_OK.match(s):
        return s
    # Sinon on met entre apostrophes (et on échappe les apostrophes internes).
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def literal(pred: str, args) -> str:
    return f"{pred}({','.join(atom(a) for a in args)})"


def _examples_lines(name: str, examples) -> list[str]:
    """Tous les pos(...) d'abord, puis tous les neg(...) : Prolog veut les
    clauses d'un même prédicat groupées (sinon warnings « not together »)."""
    pos = [f"pos({literal(name, args)})." for args, label in examples if label == 1]
    neg = [f"neg({literal(name, args)})." for args, label in examples if label != 1]
    return pos + neg


def bias_text(task: dict) -> str:
    name, arity = task["name"], task["arity"]
    b = task["bias"]
    lines = [
        f"% Biais de langage pour la tâche {task['dataset']}/{name}",
        f"head_pred({name},{arity}).",
    ]
    lines += [f"body_pred({p},{a})." for p, a in task["body_preds"]]
    types = task.get("types") or {}
    if types:
        lines.append("")
        lines.append("% Types des arguments (réduisent l'espace de recherche)")
        for pred, tys in types.items():
            lines.append(f"type({pred},({','.join(tys)}{',' if len(tys) == 1 else ''})).")
    lines.append("")
    lines.append(f"max_vars({b['max_vars']}).")
    lines.append(f"max_body({b['max_body']}).")
    lines.append(f"max_clauses({b['max_clauses']}).")
    if b.get("enable_recursion"):
        lines.append("enable_recursion.")
    return "\n".join(lines) + "\n"


def write_popper_task(task: dict, out_dir, extra_meta: dict | None = None) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    name = task["name"]

    # Pas de directive ':-' ici : Popper relit bk.pl et ne les comprend pas.
    # Chaque prédicat de body_preds doit donc avoir au moins un fait.
    bk = [f"% Connaissances de fond : {task['dataset']}"]
    bk += sorted(set(f"{f}." for f in task["bk"]))
    (out / "bk.pl").write_text("\n".join(bk) + "\n", encoding="utf-8")

    (out / "exs.pl").write_text(
        f"% Exemples d'apprentissage ({len(task['train'])})\n"
        + "\n".join(_examples_lines(name, task["train"])) + "\n", encoding="utf-8")
    (out / "test_exs.pl").write_text(
        f"% Exemples de test ({len(task['test'])}) - NE PAS donner à Popper\n"
        + "\n".join(_examples_lines(name, task["test"])) + "\n", encoding="utf-8")

    (out / "bias.pl").write_text(bias_text(task), encoding="utf-8")

    meta = {
        "dataset": task["dataset"],
        "task": name,
        "arity": task["arity"],
        "n_bk_facts": len(set(task["bk"])),
        "train": {"pos": sum(l for _, l in task["train"]),
                  "neg": sum(1 - l for _, l in task["train"])},
        "test": {"pos": sum(l for _, l in task["test"]),
                 "neg": sum(1 - l for _, l in task["test"])},
        "bias": task["bias"],
        **(extra_meta or {}),
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return out
