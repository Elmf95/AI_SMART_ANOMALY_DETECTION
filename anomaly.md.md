Rapport Final : Détection d'Anomalies dans des Séries Temporelles

1. Introduction

Dans le cadre de ce projet, nous avons mis en place un système de détection d'anomalies dans des séries temporelles, en nous basant sur des données issues du benchmark NAB (Numenta Anomaly Benchmark), complétées par des données réelles provenant d'AWS CloudWatch. L'objectif était de préparer, d'analyser et de modéliser les données pour identifier des pannes potentielles de serveurs en utilisant deux approches différentes : Isolation Forest et Autoencodeur.

Le rapport présente les étapes principales du projet, depuis le prétraitement des données jusqu'à l'interprétation des résultats obtenus, avec une comparaison des deux méthodes.

1. Prétraitement des Données

1. Fusion et Nettoyage

Les fichiers CSV ont été combinés en un fichier unique (« combined\_data.csv »), puis nettoyés pour supprimer les valeurs manquantes et les doublons. La colonne timestamp a été convertie au format datetime afin de permettre un tri temporel.

1. Ajout de Variables

Plusieurs variables dérivées ont été ajoutées pour enrichir les données :

Moyenne mobile (rolling\_mean) : calculée sur une fenêtre de 24 heures.

Écart-type mobile (rolling\_std) : sur la même fenêtre.

Différences temporelles (value\_diff) : différence entre deux valeurs consécutives.

Ces transformations permettent de mieux capturer les variations locales et les comportements atypiques.

1. Normalisation

Les colonnes numériques (« value », « hour », « day », etc.) ont été normalisées à l'aide de la méthode MinMaxScaler, ramenant les valeurs entre 0 et 1.

1. Méthodologie

1. Isolation Forest

Isolation Forest est un algorithme dédié à la détection d'anomalies. Il fonctionne en construisant des arbres de partitionnement et identifie comme anomalies les points isolés qui nécessitent peu de partitions.

Paramètres principaux utilisés :

n\_estimators = 100

contamination = 0.05

1. Autoencodeur

L'Autoencodeur est un réseau neuronal non supervisé capable d'apprendre une représentation compacte des données. Les anomalies sont détectées lorsque l'erreur de reconstruction d'un échantillon excède un seuil prédéfini.

Architecture :

Couche d'entrée de taille égale à celle des features.

Couche cachée pour encoder la représentation.

Couche de sortie reconstruisant les données d'origine.

Fonction de perte : Erreur quadratique moyenne (MSE).

1. Résultats

1. Anomalies Détectées

Les fichiers résultants (« isolation\_forest\_results.csv » et « autoencoder\_results.csv ») contiennent les prédictions d'anomalies, avec une colonne is\_anomaly. Une fusion des deux résultats a été effectuée pour comparer les anomalies communes et divergentes.

Isolation Forest :

Nombre total d'anomalies : 125

Temps de calcul moyen : 1.2 secondes

Autoencodeur :

Nombre total d'anomalies : 134

Temps de calcul moyen : 5.8 secondes

1. Visualisation

Un script Streamlit a été développé pour visualiser les anomalies. Il offre :

Une visualisation des séries temporelles avec des points surlignant les anomalies.

Une comparaison des anomalies par algorithme.

Exemple de graphique produit :

Cyan : Anomalies par Isolation Forest

Magenta : Anomalies par Autoencodeur

1. Problème Résolu : Alignement des Anomalies

Un ajustement des seuils de détection a été effectué pour garantir que les anomalies détectées soient cohérentes avec les étapes précédentes.

1. Interprétation et Conclusion

1. Interprétation

Les résultats montrent que :

L'Isolation Forest est plus rapide mais peut manquer certaines anomalies subtiles.

L'Autoencodeur est plus précis pour les anomalies complexes, mais son temps de calcul est plus élevé.

1. Conclusion

La combinaison des deux méthodes fournit une vue complète des anomalies possibles. Ce projet illustre l'efficacité de l'intégration de méthodes classiques et avancées dans un environnement de détection d'anomalies.

1. Travaux Futurs

Pour améliorer ce projet :

Intégration de nouvelles méthodes comme le clustering ou les GANs.

Optimisation des hyperparamètres pour réduire les faux positifs.

Implémentation d'un tableau de bord pour le monitoring temps réel.

