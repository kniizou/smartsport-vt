import sys
import os
from pathlib import Path

# Configuration du chemin
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Import des settings
try:
    from backend.settings import SIMPLE_JWT
    print("Configuration JWT valide :")
    print(SIMPLE_JWT)
except Exception as e:
    print("Erreur d'import :", e)