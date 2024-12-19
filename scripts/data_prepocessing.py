import os
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Gestion dynamique des chemins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les constantes depuis config.py
from config import CLEANED_DATA_DIR, PROCESSED_DATA_DIR

# Charger les données nettoyées
CLEANED_FILE = os.path.join(CLEANED_DATA_DIR, "cleaned_data.csv")
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, "prepared_data.csv")

print(f"Chargement des données nettoyées depuis : {CLEANED_FILE}")
data = pd.read_csv(
    CLEANED_FILE, parse_dates=["timestamp"]
)  # Conversion de 'timestamp' en datetime

# Vérification de l'existence de la colonne 'timestamp' pour le tri
if "timestamp" in data.columns:
    data = data.sort_values(by="timestamp")  # Tri par timestamp
else:
    print("Erreur : La colonne 'timestamp' est introuvable dans les données.")

# Normalisation des colonnes numériques
numerical_columns = [
    "value",
    "hour",
    "day",
    "month",
]  # Ajuste en fonction de tes colonnes
existing_columns = [col for col in numerical_columns if col in data.columns]
if existing_columns:
    print("Normalisation des colonnes numériques...")
    scaler = MinMaxScaler()
    data[existing_columns] = scaler.fit_transform(data[existing_columns])
else:
    print("Erreur : Aucune colonne numérique valide pour la normalisation.")

# Ajout de nouvelles features
print("Ajout de features dérivées (moyennes mobiles, différences)...")
if "value" in data.columns:
    data["rolling_mean"] = (
        data["value"].rolling(window=24).mean()
    )  # Moyenne mobile (24 heures)
    data["rolling_std"] = data["value"].rolling(window=24).std()  # Écart-type mobile
    data["value_diff"] = data["value"].diff()  # Différence avec t-1
else:
    print(
        "Erreur : La colonne 'value' est introuvable pour créer des features dérivées."
    )

# Supprimer les lignes avec NaN (causées par les rolling windows)
data = data.dropna()

# Sauvegarde des données traitées
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)  # Crée le dossier si nécessaire
data.to_csv(PROCESSED_FILE, index=False)
print(f"Données préparées sauvegardées dans : {PROCESSED_FILE}")

# Aperçu des données traitées
print("Aperçu des données après preprocessing :")
print(data.head())

# Visualisation des séries temporelles
if "timestamp" in data.columns and "value" in data.columns:
    print("Visualisation des séries temporelles...")
    plt.figure(figsize=(12, 6))
    plt.plot(data["timestamp"], data["value"], label="Valeur")
    plt.title("Séries temporelles des valeurs")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Erreur : Impossible de tracer les séries temporelles (colonnes manquantes).")
