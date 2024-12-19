import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import CLEANED_DATA_DIR


def load_cleaned_data(file_name):
    """
    Charger les données nettoyées depuis un fichier CSV.
    """
    file_path = os.path.join(CLEANED_DATA_DIR, file_name)
    print(f"🔄 Chargement des données nettoyées depuis : {file_path}")
    df = pd.read_csv(file_path, parse_dates=["timestamp"], index_col="timestamp")
    print(f"✅ Données chargées avec {df.shape[0]} lignes et {df.shape[1]} colonnes.")
    # S'assurer que l'index est trié par date
    df = df.sort_index()
    return df


def normalize_data(df):
    """
    Normaliser les colonnes numériques pour les ramener sur une échelle comparable.
    """
    print("🔧 Normalisation des données...")
    scaler = MinMaxScaler()
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    normalized_values = scaler.fit_transform(numeric_df)
    normalized_df = pd.DataFrame(
        normalized_values, columns=numeric_df.columns, index=df.index
    )
    print("✅ Données normalisées.")
    return normalized_df


def plot_time_series(df, columns, title="Séries temporelles des données"):
    """
    Visualiser les séries temporelles des colonnes spécifiées.
    """
    plt.figure(figsize=(15, 8))
    for col in columns:
        plt.plot(df.index, df[col], label=col)
    plt.title(title)
    plt.xlabel("Temps")
    plt.ylabel("Valeurs normalisées")
    plt.legend()
    plt.grid()
    plt.yscale("log")  # Échelle logarithmique pour mieux visualiser les écarts
    plt.show()


def plot_correlation_matrix(df):
    """
    Calculer et afficher la matrice de corrélation des colonnes numériques.
    """
    print("🔍 Visualisation de la matrice de corrélation...")
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    correlation_matrix = numeric_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matrice de corrélation")
    plt.show()


def mark_anomalies(df, anomalies):
    """
    Marquer les anomalies détectées sur la série temporelle principale.
    anomalies : Série de même longueur que df, avec 1 pour les anomalies, 0 sinon.
    """
    plt.figure(figsize=(15, 8))
    plt.plot(df.index, df["value"], label="Value", color="blue")
    plt.scatter(
        df.index, df["value"], c=anomalies, cmap="coolwarm", label="Anomalies", s=10
    )
    plt.title("Séries temporelles avec anomalies marquées")
    plt.xlabel("Temps")
    plt.ylabel("Valeurs")
    plt.legend()
    plt.grid()
    plt.show()


def describe_numeric_columns(df):
    """
    Afficher des statistiques descriptives pour les colonnes numériques.
    """
    print("📊 Statistiques descriptives des colonnes numériques :")
    print(df.describe())


if __name__ == "__main__":
    # Charger les données nettoyées
    file_name = "cleaned_data.csv"
    cleaned_data = load_cleaned_data(file_name)

    # Normaliser les données
    normalized_data = normalize_data(cleaned_data)

    # Zoom sur la période d'anomalies (ex: mars-avril 2014)
    print("🔍 Zoom sur la période critique...")

    # Correction de la période d'anomalies en utilisant un format de date correct
    anomaly_period = normalized_data["2014-03-01":"2014-04-01"]

    # Visualisation des séries temporelles normalisées
    print("📈 Visualisation des séries temporelles...")
    numeric_columns = normalized_data.columns
    plot_time_series(anomaly_period, numeric_columns, title="Zoom sur les anomalies")

    # Matrice de corrélation
    plot_correlation_matrix(normalized_data)

    # Statistiques descriptives
    describe_numeric_columns(normalized_data)

    # Exemple d'anomalies marquées (à remplacer par un vrai modèle de détection)
    print("⚠️ Marquage des anomalies fictives...")
    import numpy as np

    fake_anomalies = np.random.choice([0, 1], size=len(normalized_data), p=[0.95, 0.05])
    mark_anomalies(cleaned_data, fake_anomalies)
