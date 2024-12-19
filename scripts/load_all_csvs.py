import sys
import os
import pandas as pd

# Ajouter dynamiquement le chemin parent au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, create_directories


def load_csv_files(directory):
    """
    Charger tous les fichiers CSV d'un répertoire et les concaténer dans un seul DataFrame.
    """
    all_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")
    ]
    dataframes = []

    for file in all_files:
        try:
            print(f"🔄 Chargement du fichier : {file}")
            df = pd.read_csv(file, parse_dates=True)
            print(f"✅ {file} contient {len(df)} lignes et {df.shape[1]} colonnes.")
            dataframes.append(df)
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {file}: {e}")

    # Concaténation des DataFrames
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"✅ Concaténation terminée avec {len(dataframes)} fichiers.")
        print(
            f"🔎 Total : {combined_df.shape[0]} lignes et {combined_df.shape[1]} colonnes."
        )
        return combined_df
    else:
        print("❌ Aucun fichier CSV valide trouvé.")
        return None


def save_combined_data(df, output_file):
    """
    Sauvegarder le DataFrame combiné dans un fichier CSV.
    """
    output_path = os.path.join(PROCESSED_DATA_DIR, output_file)
    df.to_csv(output_path, index=False)
    print(f"✅ Données sauvegardées dans : {output_path}")


if __name__ == "__main__":
    # Créer les répertoires si nécessaire
    create_directories()

    # Charger et combiner tous les fichiers CSV
    combined_data = load_csv_files(RAW_DATA_DIR)

    if combined_data is not None:
        # Sauvegarder les données combinées
        save_combined_data(combined_data, "combined_data.csv")
