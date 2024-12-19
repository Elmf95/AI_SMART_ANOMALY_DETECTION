import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Gestion dynamique des chemins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import PROCESSED_DATA_DIR, PROCESSED_RESULTS_DIR

# Charger les données préparées
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, "prepared_data.csv")
RESULTS_FILE = os.path.join(PROCESSED_RESULTS_DIR, "anomaly_results.csv")

print(f"Chargement des données préparées depuis : {PROCESSED_FILE}")
data = pd.read_csv(PROCESSED_FILE, parse_dates=["timestamp"])

# Vérification de la colonne 'value'
if "value" not in data.columns:
    raise ValueError("Erreur : La colonne 'value' est introuvable dans les données.")

# Configuration de l'Isolation Forest
print("Entraînement de l'Isolation Forest...")
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
data["anomaly_score"] = model.fit_predict(data[["value"]])

# Détection des anomalies (score -1 pour les anomalies)
data["is_anomaly"] = data["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)
anomaly_count = data["is_anomaly"].sum()
print(f"Nombre total d'anomalies détectées : {anomaly_count}")

# Sauvegarder les résultats des anomalies
os.makedirs(PROCESSED_RESULTS_DIR, exist_ok=True)
data.to_csv(RESULTS_FILE, index=False)
print(f"Résultats sauvegardés dans : {RESULTS_FILE}")

# Visualisation des anomalies détectées
if "timestamp" in data.columns and "value" in data.columns:
    print("Visualisation des anomalies...")
    plt.figure(figsize=(12, 6))
    plt.plot(data["timestamp"], data["value"], label="Valeur", alpha=0.7)
    plt.scatter(
        data.loc[data["is_anomaly"] == 1, "timestamp"],
        data.loc[data["is_anomaly"] == 1, "value"],
        color="red",
        label="Anomalies",
    )
    plt.title("Anomalies détectées avec Isolation Forest")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Erreur : Impossible de tracer les anomalies (colonnes manquantes).")
