"""Le verificateur independant compte juste sur une regle connue."""
import shutil
from pathlib import Path

from src.ilp.verify import metriques, verify

FIX = Path(__file__).parent / "fixtures" / "grandparent_mini"


def tache(tmp_path):
    """Mini-tache : les exemples du fixture servent d'exemples de test."""
    for f in ("bk.pl", "bias.pl"):
        shutil.copy(FIX / f, tmp_path / f)
    shutil.copy(FIX / "exs.pl", tmp_path / "test_exs.pl")
    return tmp_path


def test_bonne_regle(tmp_path):
    c = verify(tache(tmp_path), "grandparent(A,B):- parent(A,C),parent(C,B).")
    assert c == {"tp": 3, "fn": 0, "tn": 3, "fp": 0}
    assert metriques(c)["precision"] == 1.0


def test_mauvaise_regle(tmp_path):
    # "grand-parent = parent" : rate les 3 positifs, accepte le negatif (alice,bob)
    c = verify(tache(tmp_path), "grandparent(A,B):- parent(A,B).")
    assert c == {"tp": 0, "fn": 3, "tn": 2, "fp": 1}


def test_aucune_regle(tmp_path):
    c = verify(tache(tmp_path), None)
    assert c == {"tp": 0, "fn": 3, "tn": 3, "fp": 0}
