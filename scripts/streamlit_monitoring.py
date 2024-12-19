import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Gestion dynamique des chemins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import PROCESSED_RESULTS_DIR

# Charger les résultats des anomalies
RESULTS_FILE = os.path.join(PROCESSED_RESULTS_DIR, "anomaly_results.csv")


@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Le fichier {file_path} est introuvable.")
        return pd.DataFrame()
    data = pd.read_csv(file_path, parse_dates=["timestamp"])
    return data


# Application Streamlit
st.title("Monitoring des anomalies - Isolation Forest")
st.markdown(
    "Analyse en temps réel des anomalies détectées dans vos séries temporelles."
)

# Charger les données
st.write(f"Chargement des données depuis : {RESULTS_FILE}")
data = load_data(RESULTS_FILE)

if not data.empty:
    # Filtrer les anomalies
    anomalies = data[data["is_anomaly"] == 1]
    anomaly_count = len(anomalies)

    st.write(f"Nombre total d'anomalies détectées : **{anomaly_count}**")

    # Affichage des données brutes
    if st.checkbox("Afficher les données brutes"):
        st.write(data.head())

    # Visualisation des séries temporelles avec les anomalies
    st.subheader("Visualisation des anomalies détectées")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data["timestamp"], data["value"], label="Valeur", alpha=0.7)
    ax.scatter(
        anomalies["timestamp"],
        anomalies["value"],
        color="red",
        label="Anomalies",
    )
    ax.set_title("Anomalies détectées avec Isolation Forest")
    ax.set_xlabel("Date")
    ax.set_ylabel("Valeur")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Options d'exploration
    st.subheader("Explorer les anomalies")
    start_date = st.date_input("Date de début", value=data["timestamp"].min().date())
    end_date = st.date_input("Date de fin", value=data["timestamp"].max().date())

    filtered_data = data[
        (data["timestamp"] >= pd.Timestamp(start_date))
        & (data["timestamp"] <= pd.Timestamp(end_date))
    ]
    st.write(
        f"Nombre d'anomalies entre {start_date} et {end_date} : {len(filtered_data[filtered_data['is_anomaly'] == 1])}"
    )
    st.write(filtered_data)
else:
    st.warning(
        "Les données ne sont pas disponibles. Veuillez vérifier le fichier des résultats."
    )
