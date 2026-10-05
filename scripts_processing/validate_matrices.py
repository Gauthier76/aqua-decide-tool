# ==================================================
# FILE: scripts_processing\validate_matrices.py
# ==================================================

import pandas as pd
import sys


def validate_matrix_physics(csv_file: str):
    """
    Script CI/CD pour vérifier que les matrices générées respectent
    les bornes de la physique du bâtiment (pas de puissance négative sans gain solaire, etc.)
    """
    print(f"Validation de la matrice {csv_file}...")
    df = pd.read_csv(csv_file)

    errors = 0
    if 'Q_evap_kW' in df.columns:
        if (df['Q_evap_kW'] < 0).any():
            print("❌ ERREUR: Pertes par évaporation négatives détectées.")
            errors += 1

    if 'RH_air' in df.columns:
        if (df['RH_air'] < 0).any() or (df['RH_air'] > 100).any():
            print("❌ ERREUR: Humidité relative hors limites (0-100%).")
            errors += 1

    if errors == 0:
        print("✅ Matrice physiquement cohérente.")
        sys.exit(0)
    else:
        print(f"Échec de la validation avec {errors} erreurs.")
        sys.exit(1)