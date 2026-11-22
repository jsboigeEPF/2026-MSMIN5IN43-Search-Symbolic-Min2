# Permet « from src... » quand on lance simplement `pytest` depuis groupe-<nom-court>/
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
