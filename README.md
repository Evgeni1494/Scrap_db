# Scraper les données IMDB

Ce brief a été réalisé dans le cadre de la formation Développeuse en Intelligence Artificielle avec l'Ecole Microsoft IA by Simplon. 

Il avait pour objectif de valider les compétences : 
- Qualifier les données grâce à des outils d’analyse et de visualisation de données en vue de vérifier leur adéquation avec le projet ;
- Concevoir une base de données analytique avec l’approche orientée requêtes en vue de la mise à disposition des données pour un traitement analytique ou d’intelligence artificielle ;
- Programmer l’import de données initiales nécessaires au projet en base de données, afin de les rendre exploitables par un tiers, dans un langage de programmation adapté et à partir de la stratégie de nettoyage des données préalablement définie ;
- Préparer les données disponibles depuis la base de données analytique en vue de leur utilisation par les algorithmes d’intelligence artificielle ;
- Développer les requêtes et les composants d'accès aux données dans un langage adapté afin de persister et mettre à jour les données issues de l’application en base de données ;
- Développer le back-end de l’application d’intelligence artificielle dans le respect des spécifications fonctionnelles et des bonnes pratiques du domaine. ;
- Développer le front-end de l’ application d’intelligence artificielle à partir de maquettes et du parcours utilisateur⋅rice, dans le respect des objectifs visés et des bonnes pratiques du domaine.

## Organisation 

Le dossier scraping_imdb contient :
- le dossier spiders  : dans lequel les fichiers a250crawl.py et films_spider.py contiennent respectivement les spiders pour les séries et pour les films ;
- le dockerfile qui permet le déploiement de l'application streamlit ;
- items.py : qui contient le modèle pour le scraping des films ; 
- pipelines.py : qui contient les deux pipelines pour extraire les données du site imdb et les transmettre à la base de données atlas ; 
- requêtes.ipynb : qui contient la réponse aux questions MongoDb ;
- requirements.txt : qui permet d'installer les packages nécessaires à l'exécution du projet ; 
- settings.py : les réglages du projet scrapy ; 
- streamlit_app.py : le script de l'application streamit. 

## Utilisation 

Pour exécuter le projet, il est nécessaire d'installer les packages présents dans le requirements.txt. 
Pour vous connecter à une base de données, vous devez la créer sur atlas puis récupérer l'URI dans "connect". 
Créez un .env pour y stocker votre atlas_key.
Pour visualiser le streamlit, vous pouvez exécuter streamlit run streamlit_app.py 
