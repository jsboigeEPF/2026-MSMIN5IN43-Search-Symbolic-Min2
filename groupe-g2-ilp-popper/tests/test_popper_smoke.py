"""Test de fumee : Popper est installe et retrouve la regle grandparent."""
from pathlib import Path

from popper.loop import learn_solution
from popper.util import Settings, format_prog

TASK = Path(__file__).parent / "fixtures" / "grandparent_mini"


def test_popper_retrouve_grandparent():
    prog, score, _ = learn_solution(Settings(kbpath=str(TASK), quiet=True))
    assert prog is not None, "Popper n'a trouve aucune regle"
    print("\nRegle apprise :", format_prog(prog))
    tp, fn, tn, fp = score[0], score[1], score[2], score[3]
    assert (tp, fn, fp) == (3, 0, 0)   # couvre les 3 positifs, aucun negatif
