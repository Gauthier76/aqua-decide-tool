# ==================================================
# FILE: backend\engine\matrix_interpolator.py
# ==================================================

import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator


class MatrixInterpolator:
    """
    Classe permettant d'interpoler les résultats transitoires (Polysun / IDA-ICE)
    pré-calculés pour éviter de relancer des simulations complètes.
    """

    def __init__(self, matrix_path: str):
        self.matrix_path = matrix_path
        self.data = None
        self._load_matrix()

    def _load_matrix(self):
        # Charge la matrice pré-calculée en mémoire
        try:
            self.data = pd.read_csv(self.matrix_path)
        except Exception as e:
            print(f"Erreur lors du chargement de la matrice: {e}")

    def get_interpolated_value(self, t_air, t_water, wind_speed):
        """
        Interpole la valeur de besoin de chaleur en fonction des inputs.
        (Méthode simplifiée pour le prototype).
        """
        if self.data is None:
            return 0.0

        # Logique d'interpolation N-D (Nearest ou Linear) basée sur les colonnes de la matrice
        # Exemple basique de recherche du plus proche voisin
        diff = np.abs(self.data['T_air'] - t_air) + \
               np.abs(self.data['T_water'] - t_water) + \
               np.abs(self.data['Wind'] - wind_speed)

        best_match_idx = diff.argmin()
        return self.data.loc[best_match_idx, 'Q_total_kW']