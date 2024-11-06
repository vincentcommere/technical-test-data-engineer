# Réponses du test

## Questions :

1. Un fichier `requirements.txt` liste les librairies à utiliser pour l'étape 2. Créez un environnement virtuel avec l'outil de votre choix et activez-le.

2. Élaborer un flux de données, en **Python**, conçu pour récupérer quotidiennement les données de l'API.
*Pour lancer le serveur, déplacez-vous dans le dossier `src/moovitamix_fastapi` puis exécutez la commande `python -m uvicorn main:app`.*

3. Mettez en place quelques tests unitaires sur les composants de votre flux de données.
*Choisissez judicieusement des tests unitaires essentiels pour votre flux de données, sans exagérer leur nombre.*

4. Détaillez le schéma de la base de données que vous utiliseriez pour stocker les informations récupérées des trois sources de données mentionnées plus tôt. Quel système de base de données recommanderiez-vous pour répondre à ces besoins et pourquoi ?

5. Le client exprime le besoin de suivre la santé du pipeline de données dans son exécution quotidienne. Expliquez votre méthode de surveillance à ce sujet et les métriques clés.

   Félicitations, à ce stade les données sont ingérées quotidiennement grâce à votre pipeline de données ! Les scientifiques de données sollicitent votre collaboration pour la mise en place de l’architecture du système de recommandation. Votre expertise est sollicitée pour automatiser le calcul des recommandations et pour automatiser le réentraînement du modèle.

6. Dessinez et/ou expliquez comment vous procéderiez pour automatiser le calcul des recommandations.

7. Dessinez et/ou expliquez comment vous procéderiez pour automatiser le réentraînement du modèle de recommandation.

## Réponses :

### Étape 1 - Contexte et mise en route

Dans le contexte de ce test, nous allons implémenter une solution d'extraction et de préparation de données. L'objectif est de créer un data mart (une sous-division d’un data lake) permettant de mettre un ensemble de données à disposition des scientifiques de données et du modèle de recommandation de musique Moovitamix, facilitant ainsi son inférence et son réentraînement en production.

La première étape consiste à mettre en place l'environnement de travail.

- Après avoir forké le répertoire GitHub, clonez celui-ci sur votre environnement de travail via la commande :

```
// Cloner le répertoire
>> git clone https://github.com/vincentcommere/technical-test-data-engineer.git

// Upgrade pip
>> python -m pip install --upgrade pip

// Aller dans le répertoire
>> cd technical-test-data-engineer

// Créer Virtual Env
>> python -m venv venv

// Activer Virtual Env
>> . venv/bin/activate

// Vérifier si Virtual Env est créé et activé correctement
>> which python 
>> python --version

// Installer les packages
// Installer les packages supplémentaires (linting, import sorting)
>> pip install -r requirements.txt

// Vérifier installation des packages
>> pip list

// Mettre à jour le fichier requirements.txt
pip freeze > requirements.txt

```

### Étape 2 - Description de la Solution

#### Les flux de données ETL

Dans un objectif de non-redondance de code et de respect des principes de POO, la structure des classes est la suivante :

Classe Générique à toutes les sources de données :

- BaseETL : effectue des tests principaux vis-à-vis des sources de données (stabilité (schéma, colonnes, etc.), connectivité...) ainsi que les vérifications de base de chaque ensemble de données (doublons, NaN...).

Classe Spécifique à chacune des sources de données (hérite de BaseETL) :

- HistoryETL : Effectue les transformations nécessaires aux données du endpoint `/liste_history`.
- TracksETL : Effectue les transformations nécessaires aux données du endpoint `/tracks`.
- UsersETL : Effectue les transformations nécessaires aux données du endpoint `/users`.

NB : Des logs simples d'exécution ont été ajoutées dans un dossier `logs`.

NB0 : Des choix arbitraires ont été effectués dans la gestion des doublons et différents cas d'erreurs, il est nécessaire de s'assurer auprès du client de la validité de ces choix.

NB1 : Notez que les fonctions `extract()` et `load()` se trouvent dans la classe `BaseETL`, ce choix est justifié par le contexte de ce test. Les sources de données viennent du même serveur et sont du même type (API), le load est effectué sous forme de CSV.

NB2 : Les fonctions `__call__()` englobent le plus haut niveau d'abstraction des ETLs. Par souci de simplicité, celle-ci est également redéfinie dans `BaseETL`. Si nous souhaitons plus de précisions et de visibilité dans les étapes des ETLs, nous pourrions les redéfinir dans les classes Python spécifiques (`HistoryETL`, `TracksETL`...).


#### Choix de L'orchestration

Plusieurs choix s'offrent à nous en matière de 'scheduling' et d'orchestration des flux de données :

#### In-App Scheduling

**Pros :**
- **Grande flexibilité** : Permet une personnalisation importante, adaptée aux besoins spécifiques de l'application.

**Cons :**
- **Limites de scalabilité** : Si les flux de données deviennent complexes, la solution peut devenir difficile à maintenir.

#### Cron Job

**Pros :**
- **Simplicité** : Facile à mettre en place pour des tâches basiques et des horaires simples.
- **Indépendance** : Fonctionne sur n'importe quel environnement supportant cron (Unix/Linux), sans nécessiter de dépendances supplémentaires.

**Cons :**
- **Manque de visibilité** : Pas de tableau de bord pour suivre les exécutions, ce qui rend le débogage plus difficile.
- **Dépendance au système** : Fonctionne uniquement dans des environnements compatibles Unix/Linux, et est peu adaptable pour des workflows complexes.

#### Toolkit (Airflow, Luigi, etc.)

**Pros :**
- **Bonne visibilité et monitoring** : Permet de visualiser les flux de travail, les dépendances, et les erreurs d'exécution en temps réel.
- **Scalabilité** : Ces outils sont conçus pour gérer des workflows complexes et s'adapter à des besoins croissants.

**Cons :**
- **Coût de maintenance** : Ces outils nécessitent des efforts continus de maintenance et de configuration pour fonctionner de manière optimale.



### Étape 3 - Les Tests de la Solution

Dans le contexte de ce test de recrutement, le choix des tests unitaires a été porté sur les transformations effectuées par :

- HistoryETL : test de structure `extract()` et `transform()`
- TracksETL : test de structure `extract()` et `transform()`
- UsersETL : test de structure `extract()` et `transform()`

### Utilisation de la Solution

Un fichier `Makefile` a été ajouté afin de permettre à l'utilisateur de lancer simplement les commandes nécessaires pour :

- lister l'arborescence du répertoire,
- lancer les tests unitaires ainsi que le test de coverage,
- lancer et arrêter l'architecture micro-services.

````
// run coverage
>>> make cov

// run test
>>> make pytest

// run formating checks
>>> make format-check

// run formating corections
>>> make format-apply

// set architecture up
>>> make up

// set architecture down
>>> make down

// visualiser lárboresence du repo
>>> make tree
````

Pour s'assurer de la bonnne exécution des ETLs un volume est monté entre le container gentETL et data/. Ainsi les ETLs ecrirons des csv visible dans le dossier data.

### Limitations de la Solution

- **Code** : les checks et tests de stabilité et de qualité des données on volontairement ete simplifié. Dans un context clients il est bon de s'assurer des règles à suivre vis-a-vis des cas marginaux comme les doublons par exemple.
- **Dockerfile** : Dockerfile simple, pas prêt pour la production, absence de layer d'authentification.
- **Tests unitaires et couverture** > 40%
- **Orchestration** : Utilisation des cron jobs dans un container à des fins de simplicité et de démonstration de compétences système et microservices.

### Bonus et Extra

- **Architecture** : Utilisation de Docker Compose à des fins de démonstration, mais non conseillé en production car c'est une architecture microservices single machine.
- **CI/CD**  : Quelques exemples de fichiers de configuration du pipeline CI/CD à des fins de checks de linting, de tests unitaires et d'intégration. (./.github/)
- **Airflow Dags files** : Un ensemble d'exemples de DAGs Airflow simplifiés a également été fourni à des fins de démonstration de compétences. (./src/dags/)

## Questions (étapes 4 à 7)

### Étape 4

L’utilisation d’une base de données relationnelle comme **PostgreSQL** est privilégiée dans ce contexte en raison de la structure et des relations complexes entre les données provenant des trois sources. Les informations récupérées incluent des liens étroits entre les utilisateurs (user_id), les transactions (track_id) et les historiques d'écoute (user_id + track_id). PostgreSQL permet de gérer efficacement ces relations via des clés étrangères et des jointures, assurant ainsi l'intégrité des données. Dans une base NoSQL, ces relations seraient moins directes et nécessiteraient soit une duplication de données, soit une gestion plus complexe au niveau de l’application, ce qui augmenterait le risque d'incohérences et de difficultés de mise à jour. Les capacités de PostgreSQL en matière de requêtes complexes et d'agrégations surpassent celles des bases NoSQL.

### Étape 5

Pour surveiller la santé du pipeline de données dans son exécution quotidienne, plusieurs solutions s'offrent à nous.

Si nous avons utilisé un outil tel qu'Airflow ou Luigi, ceux-ci intègrent des interfaces utilisateurs claires permettant de visualiser l'exécution de chaque étape du flux, offrant même la flexibilité sur le niveau d'abstraction de chaque étape (combien d'étapes ETL souhaitons-nous visualiser ?).

Dans le cas où nous voudrions historiser les mesures de surveillance afin de développer notre propre dashboard (Prometheus, Grafana, Tableau, PowerBI, Kibana...), ce tableau de bord pourrait afficher les taux de succès, les erreurs, les performances en temps réel, et les statistiques de conformité des données. Les rapports quotidiens ou hebdomadaires peuvent aussi être envoyés par e-mail pour un suivi régulier, avec des résumés des métriques clés et des éventuelles anomalies.

Je recommanderais alors les métriques suivantes :

#### a) Stabilité et Qualité des Données

- **Taux de succès des flux** : Mesurer le pourcentage de jobs ou de tâches réussis dans le pipeline. Un taux de succès proche de 100 % indique une exécution saine.
- **Données manquantes ou nulles** : Surveiller les enregistrements avec des valeurs manquantes ou nulles dans les étapes critiques du pipeline, ce qui pourrait signaler des problèmes dans l'extraction ou la transformation.
- **Validation de schéma** : Vérifier que les données respectent le schéma attendu.

#### b) Performance et Temps d’Exécution

- **Temps d'exécution par étape** : Suivre le temps d'exécution de chaque étape ou tâche clé du pipeline. Si une étape prend plus de temps que d’habitude, cela peut indiquer une saturation des ressources ou des problèmes dans le code.
- **Temps total d’exécution du pipeline** : Mesurer le temps total d’exécution du pipeline chaque jour. Des augmentations soudaines peuvent révéler des goulots d'étranglement.
- **Utilisation des ressources** : Monitorer l’utilisation des CPU, de la mémoire, et des entrées/sorties de disques. Des ressources saturées peuvent ralentir le pipeline ou provoquer des échecs.
- **Nombre de redémarrages** : Si le pipeline est configuré pour redémarrer les tâches en cas d’échec, suivre le nombre de redémarrages est crucial pour identifier les processus instables ou sujets aux erreurs.
- **Volume de données traitées** : Suivre le volume de données traité chaque jour, pour s'assurer que la quantité attendue de données est bien reçue et traitée. Toute variation inhabituelle peut signaler un problème en amont.

### Étape 6

Une fois la mise à jour quotidienne effectuée, je programmerais mon orchestrateur afin qu'il exécute l'Inference Job :

Étapes de l'Inference Job :

- **Data Extraction** : extraction des sources de données à jour depuis le data mart IA.
- **Data Preparation** : jointure et création de champs calculés potentiels nécessaires à l'inférence.
- **Data Processing** : Normalisation / Scaling, toutes préparations liées au modèle ML utilisé pour la recommandation.
- **Inference** : Inférence du modèle sur les nouvelles données.
- **Evaluation** : Évaluation de la performance du modèle.
- **Load** : Écriture des résultats (inférence et évaluation) en base de données.

### Étape 7

**NB** - Image 'schema-simple-archi.png', elle représente un schéma d'architecture microservices dans une logique dite d'active learning.

Tout d'abord, admettons que :

En gris :
- nous utilisons FastAPI sous forme de microservice ;
- nous utilisons un autre microservice PostgreSQL comme data mart IA ;
- nous utilisons également un modèle Registry afin d'historiser les versions du modèle de recommandation (MLFlow...).

En vert : 
nous avons ensuite trois agents effectuant des opérations avec les données (ETLs, Inference, Entrainement), chacun dans un microservice différent.

En bleu : 
- le dashboard de monitoring de performance (ETLs, Inference, réentraînement...).
- l'application logicielle finale utilisant les recommandations (Moovitamix).

Pour automatiser le réentraînement, je commencerais par appliquer un seuil de réentraînement sur la performance de l'inference Job. Si l'inférence dépasse le seuil, alors j'activerais l'agent d'entraînement afin qu'il réentraîne le modèle, qu'il compare les performances du nouveau modèle à celui en production, et remplace ou non le modèle de production par le nouveau dans le modèle Registry.

![Schema Simplifié Architecture Active Learning](/technical-test-data-engineer/docs/schema-simple-archi.jpg)



### Annexe :

````
.
├── Changelog.md                 # Historique des modifications du projet, documentant les mises à jour et corrections de version.
├── README.md                    # Documentation de base du projet, incluant les instructions d'installation, de configuration, et d'utilisation.
├── data                         # Dossier pour stocker les données brutes ou temporaires utilisées par les ETLs.
├── docker-compose.yaml          # Fichier de configuration pour Docker Compose, orchestrant les services dans un environnement de conteneur.
├── docs                         # Dossier pour la documentation supplémentaire du projet.
│   ├── ANSWERS.md               # Document pour répondre à des questions techniques ou des tests, souvent lié au projet.
│   └── schema-simple-archi.jpg  # Schéma de l'architecture simplifiée, en image pour visualiser les composants du système.
├── micro-services               # Dossier contenant les microservices du projet.
│   ├── agentETL                 # Microservice dédié à l'exécution des tâches ETL.
│   │   ├── Dockerfile           # Fichier de configuration pour construire l'image Docker de l'agent ETL.
│   │   ├── crontab              # Fichier de configuration des tâches cron pour planifier les ETLs.
│   │   ├── requirements.txt     # Liste des dépendances Python pour le microservice agent ETL.
│   │   └── src                  # Code source de l'agent ETL.
│   │       ├── __init__.py      # Indicateur que le dossier `src` est un module Python.
│   │       └── etls             # Sous-dossier pour les scripts ETL spécifiques.
│   │           ├── __init__.py  # Indicateur que le dossier `etls` est un module Python.
│   │           ├── etl_base.py  # Script définissant la classe de base pour les ETLs, incluant des méthodes communes.
│   │           ├── etl_listen_history.py  # Script ETL pour traiter les données d'historique d'écoute.
│   │           ├── etl_tracks.py          # Script ETL pour traiter les données des pistes.
│   │           ├── etl_users.py           # Script ETL pour traiter les données des utilisateurs.
│   │           └── utils.py               # Fonctions utilitaires utilisées par les scripts ETL.
│   └── fastAPI                  # Microservice pour l'API FastAPI.
│       ├── Dockerfile           # Fichier de configuration pour construire l'image Docker du microservice FastAPI.
│       └── requirements.txt     # Liste des dépendances Python pour le microservice FastAPI.
├── requirements.txt             # Liste globale des dépendances Python pour l'ensemble du projet.
├── setup.cfg                    # Fichier de configuration pour le packaging et les réglages du projet (par ex., pour linting, imports).
├── src                          # Code source principal du projet.
│   ├── __init__.py              # Indicateur que le dossier `src` est un module Python.
│   ├── dags                     # Dossier contenant les DAGs Airflow pour l'orchestration des ETLs.
│   │   ├── __init__.py          # Indicateur que le dossier `dags` est un module Python.
│   │   ├── history_etl_dag.py   # DAG Airflow pour orchestrer le flux de données de l'historique d'écoute.
│   │   ├── tracks_etl_dag.py    # DAG Airflow pour orchestrer le flux de données des pistes.
│   │   └── users_etl_dag.py     # DAG Airflow pour orchestrer le flux de données des utilisateurs.
│   ├── etls                     # Dossier pour les scripts ETL.
│   │   ├── __init__.py          # Indicateur que le dossier `etls` est un module Python.
│   │   ├── etl_base.py          # Script définissant la classe de base pour les ETLs, incluant des méthodes communes.
│   │   ├── etl_listen_history.py # Script ETL pour traiter les données d'historique d'écoute.
│   │   ├── etl_tracks.py         # Script ETL pour traiter les données des pistes.
│   │   ├── etl_users.py          # Script ETL pour traiter les données des utilisateurs.
│   │   └── utils.py              # Fonctions utilitaires utilisées par les scripts ETL.
│   └── moovitamix_fastapi        # Application FastAPI pour exposer des endpoints liés aux données Moovitamix.
│       ├── __init__.py           # Indicateur que le dossier `moovitamix_fastapi` est un module Python.
│       ├── classes_out.py        # Définitions de classes pour la sortie des données via l'API.
│       ├── generate_fake_data.py # Script pour générer des données factices pour tester l'API.
│       └── main.py               # Point d'entrée de l'API FastAPI.
└── test                          # Dossier contenant les tests unitaires du projet.
    ├── __init__.py               # Indicateur que le dossier `test` est un module Python.
    ├── test_classes_out.py       # Test unitaire pour le module `classes_out.py`.
    ├── test_etl_base.py          # Test unitaire pour le module `etl_base.py`.
    ├── test_etl_listen_history.py # Test unitaire pour le script `etl_listen_history.py`.
    ├── test_etl_tracks.py         # Test unitaire pour le script `etl_tracks.py`.
    └── test_etl_users.py          # Test unitaire pour le script `etl_users.py`.
````