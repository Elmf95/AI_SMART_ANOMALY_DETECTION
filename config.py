import os

# Définir le répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Répertoires spécifiques
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
CLEANED_DATA_DIR = os.path.join(DATA_DIR, "cleaned")
MODELS_DIR = os.path.join(BASE_DIR, "models")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
APP_DIR = os.path.join(BASE_DIR, "app")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
PROCESSED_RESULTS_DIR = os.path.join(DATA_DIR, "processed")

# Exemple : Chemin vers un fichier CSV spécifique
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "PJM_Load_hourly.csv")


# Fonction pour créer les dossiers manquants
def create_directories():
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MODELS_DIR,
        SCRIPTS_DIR,
        APP_DIR,
        NOTEBOOKS_DIR,
        TESTS_DIR,
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
