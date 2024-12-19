import os
import sys
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Gestion dynamique des chemins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import PROCESSED_DATA_DIR, PROCESSED_RESULTS_DIR

# Charger les données préparées
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, "prepared_data.csv")
RESULTS_FILE = os.path.join(PROCESSED_RESULTS_DIR, "autoencoder_results.csv")

print(f"Chargement des données préparées depuis : {PROCESSED_FILE}")
data = pd.read_csv(PROCESSED_FILE, parse_dates=["timestamp"])

# Vérification de la colonne 'value'
if "value" not in data.columns:
    raise ValueError("Erreur : La colonne 'value' est introuvable dans les données.")

# Normalisation des données
scaler = MinMaxScaler()
data["scaled_value"] = scaler.fit_transform(data[["value"]])

# Convertir en tableau NumPy 2D pour le modèle
scaled_values = data["scaled_value"].values.reshape(-1, 1)

# Construction d'un autoencodeur simple
input_dim = scaled_values.shape[1]  # Dimension correcte
encoding_dim = 3  # Nombre de neurones dans le layer encodé
model = tf.keras.Sequential(
    [
        tf.keras.layers.InputLayer(input_shape=(input_dim,)),  # Spécifier input_shape
        tf.keras.layers.Dense(encoding_dim, activation="relu"),
        tf.keras.layers.Dense(input_dim, activation="sigmoid"),
    ]
)

model.compile(optimizer="adam", loss="mse")

# Entraînement de l'autoencodeur
print("Entraînement de l'autoencodeur...")
model.fit(scaled_values, scaled_values, epochs=20, batch_size=32, verbose=0)

# Calcul de l'erreur de reconstruction
reconstructions = model.predict(scaled_values)
reconstruction_error = np.mean(np.abs(reconstructions - scaled_values), axis=1)
data["reconstruction_error"] = reconstruction_error

# Définir un seuil basé sur le taux de contamination
contamination = 0.01  # Même valeur que pour l'Isolation Forest
threshold = np.percentile(reconstruction_error, 100 * (1 - contamination))
print(f"Seuil d'erreur de reconstruction défini à : {threshold:.4f}")

# Identifier les anomalies
data["is_anomaly"] = data["reconstruction_error"].apply(
    lambda x: 1 if x > threshold else 0
)
anomaly_count = data["is_anomaly"].sum()
print(f"Nombre total d'anomalies détectées avec l'autoencodeur : {anomaly_count}")

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
    plt.title("Anomalies détectées avec Autoencodeur")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Erreur : Impossible de tracer les anomalies (colonnes manquantes).")
