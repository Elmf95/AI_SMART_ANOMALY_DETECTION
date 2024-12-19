Détection d'Anomalies dans des Séries Temporelles
Introduction
Dans le cadre de ce projet, nous avons mis en place un système de détection d'anomalies dans des séries temporelles, en nous basant sur des données issues du benchmark NAB (Numenta Anomaly Benchmark), complétées par des données réelles provenant d'AWS CloudWatch.
L'objectif était de préparer, d'analyser et de modéliser les données pour identifier des pannes potentielles de serveurs en utilisant deux approches différentes : Isolation Forest et Autoencodeur.

Ce rapport présente les étapes principales du projet, depuis le prétraitement des données jusqu'à l'interprétation des résultats obtenus, avec une comparaison des deux méthodes.

Prétraitement des Données
2.1 Fusion et Nettoyage
Les fichiers CSV ont été combinés en un fichier unique (combined_data.csv), puis nettoyés pour supprimer les valeurs manquantes et les doublons.
La colonne timestamp a été convertie au format datetime afin de permettre un tri temporel.
2.2 Ajout de Variables
Plusieurs variables dérivées ont été ajoutées pour enrichir les données :

Moyenne mobile (rolling_mean) : calculée sur une fenêtre de 24 heures.
Écart-type mobile (rolling_std) : sur la même fenêtre.
Différences temporelles (value_diff) : différence entre deux valeurs consécutives.
Ces transformations permettent de mieux capturer les variations locales et les comportements atypiques.

2.3 Normalisation
Les colonnes numériques (value, hour, day, etc.) ont été normalisées à l'aide de la méthode MinMaxScaler, ramenant les valeurs entre 0 et 1.

Méthodologie
3.1 Isolation Forest
Isolation Forest est un algorithme dédié à la détection d'anomalies. Il fonctionne en construisant des arbres de partitionnement et identifie comme anomalies les points isolés qui nécessitent peu de partitions.

Paramètres principaux utilisés :

n_estimators = 100
contamination = 0.05
3.2 Autoencodeur
L'Autoencodeur est un réseau neuronal non supervisé capable d'apprendre une représentation compacte des données. Les anomalies sont détectées lorsque l'erreur de reconstruction d'un échantillon excède un seuil prédéfini.

Architecture :

Couche d'entrée de taille égale à celle des features.
Couche cachée pour encoder la représentation.
Couche de sortie reconstruisant les données d'origine.
Fonction de perte : Erreur quadratique moyenne (MSE).
Résultats
4.1 Anomalies Détectées
Les fichiers résultants (isolation_forest_results.csv et autoencoder_results.csv) contiennent les prédictions d'anomalies, avec une colonne is_anomaly. Une fusion des deux résultats a été effectuée pour comparer les anomalies communes et divergentes.

Isolation Forest :

Nombre total d'anomalies : 125
Temps de calcul moyen : 1.2 secondes
Autoencodeur :

Nombre total d'anomalies : 134
Temps de calcul moyen : 5.8 secondes
4.2 Visualisation
Un script Streamlit a été développé pour visualiser les anomalies. Il offre :

Une visualisation des séries temporelles avec des points surlignant les anomalies.
Une comparaison des anomalies par algorithme.
Exemple de graphique produit :

Cyan : Anomalies par Isolation Forest
Magenta : Anomalies par Autoencodeur
4.3 Problème Résolu : Alignement des Anomalies
Un ajustement des seuils de détection a été effectué pour garantir que les anomalies détectées soient cohérentes avec les étapes précédentes.

Interprétation et Conclusion
5.1 Interprétation
Les résultats montrent que :

Isolation Forest est plus rapide mais peut manquer certaines anomalies subtiles.
Autoencodeur est plus précis pour les anomalies complexes, mais son temps de calcul est plus élevé.
5.2 Conclusion
La combinaison des deux méthodes fournit une vue complète des anomalies possibles. Ce projet illustre l'efficacité de l'intégration de méthodes classiques et avancées dans un environnement de détection d'anomalies.

Travaux Futurs
Pour améliorer ce projet :

Intégration de nouvelles méthodes comme le clustering ou les GANs.
Optimisation des hyperparamètres pour réduire les faux positifs.
Implémentation d'un tableau de bord pour le monitoring temps réel.
Instructions pour l'exécution
6.1 Installation des dépendances
Pour installer les dépendances nécessaires, exécutez la commande suivante :


pip install -r requirements.txt
6.2 Visualisation du projet

Pour lancer l'application Streamlit et visualiser les anomalies détectées, utilisez la commande suivante :


streamlit run app.py
