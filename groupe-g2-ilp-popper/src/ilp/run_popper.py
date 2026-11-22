"""Lance Popper sur un dossier de tache (bk.pl, exs.pl, bias.pl).

Popper tourne dans un sous-processus isole, comme dans le notebook SL-4 du cours :
son moteur Prolog garde un etat global, et deux apprentissages dans le meme
processus melangeraient leurs faits. Un delai maximal evite tout blocage.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

WORKER = r'''
import json, sys, warnings
warnings.filterwarnings("ignore")
from popper.util import Settings, format_prog
# Patch de compatibilite Popper v4.4.0 repris de SL-4 : ordonne le litteral
# recursif en fin de corps (sinon certaines regles recursives sont mal ordonnees).
def tmp_score_(self, seen_vars, literal):
    pred, args = literal
    return self.recall.get((pred, tuple(1 if x in seen_vars else 0 for x in args)), float("inf"))
Settings.tmp_score_ = tmp_score_
from popper.loop import learn_solution
settings = Settings(kbpath=sys.argv[1], quiet=True)
prog, score, stats = learn_solution(settings)
print(json.dumps({"prog": format_prog(prog) if prog else None,
                  "score": list(score) if score else None}))
'''


def run_popper(task_dir, timeout=300):
    """Apprend une regle sur `task_dir`.

    Retourne un dict : prog (texte Prolog ou None), score d'apprentissage
    [tp, fn, tn, fp, taille] ou None, temps_s, statut
    ("ok", "aucune_regle", "timeout" ou "erreur").
    """
    debut = time.perf_counter()
    try:
        out = subprocess.run([sys.executable, "-c", WORKER, str(Path(task_dir))],
                             capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"prog": None, "score": None, "statut": "timeout",
                "temps_s": round(time.perf_counter() - debut, 2)}
    temps = round(time.perf_counter() - debut, 2)
    lignes = [l for l in out.stdout.strip().splitlines() if l.startswith("{")]
    if out.returncode != 0 or not lignes:
        return {"prog": None, "score": None, "statut": "erreur", "temps_s": temps,
                "detail": out.stderr[-2000:]}
    res = json.loads(lignes[-1])
    res["temps_s"] = temps
    res["statut"] = "ok" if res["prog"] else "aucune_regle"
    return res


if __name__ == "__main__":
    # Usage : python -m src.ilp.run_popper data/popper/family/grandparent
    print(json.dumps(run_popper(sys.argv[1]), indent=2, ensure_ascii=False))
