"""Verification independante des regles apprises.

La regle de Popper est executee dans SWI-Prolog, hors de Popper, sur les
exemples de test (test_exs.pl) que Popper n'a jamais vus pendant l'apprentissage.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _head_pred(task_dir):
    """Nom et arite du predicat a apprendre, lus dans bias.pl (head_pred)."""
    texte = (Path(task_dir) / "bias.pl").read_text()
    m = re.search(r"head_pred\(\s*(\w+)\s*,\s*(\d+)\s*\)", texte)
    if not m:
        raise ValueError(f"head_pred introuvable dans {task_dir}/bias.pl")
    return m.group(1), int(m.group(2))


def _nb_exemples(task_dir):
    texte = (Path(task_dir) / "test_exs.pl").read_text()
    return len(re.findall(r"\bpos\(", texte)), len(re.findall(r"\bneg\(", texte))


def verify(task_dir, prog, timeout=60):
    """Compte tp, fn, tn, fp de la regle `prog` sur test_exs.pl.

    prog = None (aucune regle apprise) : tout est predit faux.
    """
    task_dir = Path(task_dir).resolve()
    n_pos, n_neg = _nb_exemples(task_dir)
    if not prog:
        return {"tp": 0, "fn": n_pos, "tn": n_neg, "fp": 0}
    nom, arite = _head_pred(task_dir)
    script = f"""
:- style_check(-singleton).
:- style_check(-discontiguous).
:- table {nom}/{arite}.
:- consult('{(task_dir / 'bk.pl').as_posix()}').
{prog}
:- consult('{(task_dir / 'test_exs.pl').as_posix()}').
verdict(E, Oui, Non) :- catch((call(E) -> V = Oui ; V = Non), _, V = Non), writeln(V).
main :- forall(pos(E), verdict(E, tp, fn)), forall(neg(E), verdict(E, fp, tn)).
"""
    with tempfile.TemporaryDirectory() as d:
        fichier = Path(d) / "verif.pl"
        fichier.write_text(script)
        out = subprocess.run(["swipl", "-q", "-g", "main", "-t", "halt", str(fichier)],
                             capture_output=True, text=True, timeout=timeout)
    mots = out.stdout.split()
    compte = {k: mots.count(k) for k in ("tp", "fn", "tn", "fp")}
    if sum(compte.values()) != n_pos + n_neg:
        raise RuntimeError(f"Verification incomplete pour {task_dir} :\n{out.stderr[-2000:]}")
    return compte


def metriques(c):
    """Precision, rappel et exactitude a partir des comptes (0.0 si non defini)."""
    tp, fn, tn, fp = c["tp"], c["fn"], c["tn"], c["fp"]
    total = tp + fn + tn + fp
    return {
        "precision": round(tp / (tp + fp), 4) if tp + fp else 0.0,
        "rappel": round(tp / (tp + fn), 4) if tp + fn else 0.0,
        "exactitude": round((tp + tn) / total, 4) if total else 0.0,
    }


if __name__ == "__main__":
    # Usage : python -m src.ilp.verify <dossier_tache> "<regle prolog>"
    c = verify(sys.argv[1], sys.argv[2])
    print(c, metriques(c))
