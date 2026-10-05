# ==================================================
# FILE: scripts_processing\parse_idaice_outputs.py
# ==================================================

import pandas as pd
import argparse
from pathlib import Path


def process_idaice_prn(input_file: str, output_file: str):
    """
    Parse les fichiers de résultats bruts .prn d'IDA-ICE, moyenne les données
    horaires, et exporte une matrice .csv allégée pour l'API.
    """
    print(f"Parsing IDA-ICE output: {input_file}")
    try:
        # Les fichiers PRN d'IDA-ICE utilisent souvent des tabulations ou des espaces multiples
        df = pd.read_csv(input_file, delim_whitespace=True, skiprows=2)

        # Nettoyage et renommage standardisé
        if 'T_air' in df.columns and 'Q_heat' in df.columns:
            # Ré-échantillonnage horaire (hypothèse: les index sont des heures décimales)
            df['hour_int'] = df.index.astype(int)
            matrix = df.groupby('hour_int').mean()

            matrix.to_csv(output_file, index=False)
            print(f"Matrice exportée avec succès vers: {output_file}")
        else:
            print("Colonnes attendues introuvables. Vérifiez le format IDA-ICE.")

    except Exception as e:
        print(f"Erreur de traitement: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traitement des outputs IDA-ICE")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    process_idaice_prn(args.input, args.output)