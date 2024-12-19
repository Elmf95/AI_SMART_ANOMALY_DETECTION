import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Gestion dynamique des chemins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import PROCESSED_RESULTS_DIR

# Fichiers de résultats
FOREST_RESULTS_FILE = os.path.join(
    PROCESSED_RESULTS_DIR, "isolation_forest_results.csv"
)
AUTOENCODER_RESULTS_FILE = os.path.join(
    PROCESSED_RESULTS_DIR, "autoencoder_results.csv"
)


@st.cache_data
def load_data():
    """
    Charge les données des deux algorithmes et fusionne pour comparaison.
    """
    forest_results = pd.read_csv(FOREST_RESULTS_FILE, parse_dates=["timestamp"])
    autoencoder_results = pd.read_csv(
        AUTOENCODER_RESULTS_FILE, parse_dates=["timestamp"]
    )

    # Fusionner les résultats
    combined_results = forest_results.merge(
        autoencoder_results[["timestamp", "is_anomaly"]],
        on="timestamp",
        suffixes=("_forest", "_autoencoder"),
    )
    return combined_results


# Charger les données
data = load_data()

# Vérification des anomalies
total_anomalies_forest = len(data[data["is_anomaly_forest"] == 1])
total_anomalies_autoencoder = len(data[data["is_anomaly_autoencoder"] == 1])

# Titre de l'application
st.title("Comparaison des anomalies détectées")
st.write(f"Anomalies détectées par Isolation Forest : {total_anomalies_forest}")
st.write(f"Anomalies détectées par Autoencodeur : {total_anomalies_autoencoder}")

# Options dans la barre latérale
st.sidebar.title("Options")
show_all_data = st.sidebar.checkbox("Afficher toutes les données", value=True)
highlight_forest_anomalies = st.sidebar.checkbox(
    "Mettre en évidence les anomalies Isolation Forest", value=True
)
highlight_autoencoder_anomalies = st.sidebar.checkbox(
    "Mettre en évidence les anomalies Autoencodeur", value=True
)

# Tracé des séries temporelles
st.header("Séries temporelles et anomalies détectées")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data["timestamp"], data["value"], label="Valeur", color="blue", alpha=0.7)

# Ajouter les anomalies Isolation Forest
if highlight_forest_anomalies:
    forest_anomalies = data[data["is_anomaly_forest"] == 1]
    ax.scatter(
        forest_anomalies["timestamp"],
        forest_anomalies["value"],
        color="cyan",
        label="Anomalies Isolation Forest",
        alpha=0.9,
        marker="o",
        s=100,
    )

# Ajouter les anomalies Autoencoder
if highlight_autoencoder_anomalies:
    autoencoder_anomalies = data[data["is_anomaly_autoencoder"] == 1]
    ax.scatter(
        autoencoder_anomalies["timestamp"],
        autoencoder_anomalies["value"],
        color="magenta",
        label="Anomalies Autoencodeur",
        alpha=0.9,
        marker="x",
        s=100,
    )

ax.set_xlim(data["timestamp"].min(), data["timestamp"].max())
ax.set_ylim(data["value"].min(), data["value"].max())
ax.set_title("Séries temporelles des valeurs avec anomalies")
ax.set_xlabel("Temps")
ax.set_ylabel("Valeur")
ax.legend()
ax.grid()

# Affichage du graphique
st.pyplot(fig)

# Affichage des données détaillées
st.header("Détails des anomalies détectées")
if show_all_data:
    st.write("Données fusionnées :")
    st.dataframe(data)
else:
    st.write("Données des anomalies détectées :")
    st.dataframe(
        data[(data["is_anomaly_forest"] == 1) | (data["is_anomaly_autoencoder"] == 1)]
    )
