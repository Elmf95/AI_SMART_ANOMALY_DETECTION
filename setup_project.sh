#!/bin/bash

# Nom du projet
PROJECT_NAME="anomaly_detection"

# Création de la structure du dossier
echo "Création de la structure du projet..."
mkdir -p $PROJECT_NAME/{data,models,scripts,app,notebooks,tests}

# Aller dans le dossier du projet
cd $PROJECT_NAME

# Fichiers de base
echo "Création des fichiers de base..."
touch README.md requirements.txt .gitignore

# Initialisation de l'environnement virtuel
echo "Configuration de l'environnement virtuel..."
python -m venv venv
source venv/bin/activate

# Installation des dépendances
echo "Installation des dépendances initiales..."
pip install --upgrade pip
pip install pandas numpy matplotlib scikit-learn streamlit

# Sauvegarde des dépendances dans requirements.txt
pip freeze > requirements.txt

echo "Initialisation terminée. Votre projet est prêt !"
