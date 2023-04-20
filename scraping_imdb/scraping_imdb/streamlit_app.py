import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os


# Récupération de la clé Atlas dans le .env
load_dotenv()
ATLAS_KEY = os.getenv("ATLAS_KEY")

# se connecter à la base de données MongoDB
client = MongoClient(ATLAS_KEY)
db = client["IMDBscrap"]
collection = db["films"]

# Menu latéral pour choisir ce qu'on souhaite visualiser 
menu = ["Réponses aux questions", "Moteur de recherche"]
choix = st.sidebar.selectbox("Sélectionner une page", menu)

# Partie du streamlit qui affiche les réponses aux questions
if choix == "Réponses aux questions":
    
    st.title("Réponses aux questions")
    
    # Question 1 : Quel est le film le plus long ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 1 : Quel est le film le plus long ?</h3>", unsafe_allow_html=True)
    result = collection.find_one(sort=[("duree",-1)])
    st.write("Le film le plus long est '{}' avec une durée de {} minutes.".format(result["titre"], result["duree"]))


    # Question 2 : Quels sont les 5 films les mieux notés ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 2 : Quels sont les 5 films les mieux notés ?</h3>", unsafe_allow_html=True)
    top_rated_movies = collection.find(sort=[("score", -1)], limit=5)
    st.write("Les 5 films les mieux notés sont :")
    for i, movie in enumerate(top_rated_movies):
        st.write("{}. {} avec une note de {}".format(i+1, movie["titre"], movie["score"]))


    # Question 3 : Dans combien de films a joué Morgan Freeman ? Tom Cruise ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 3 : Dans combien de films a joué Morgan Freeman ? Tom Cruise ?</h3>", unsafe_allow_html=True)
    morgan_freeman_count = collection.count_documents({"acteurs_principaux": "Morgan Freeman"})
    tom_cruise_count = collection.count_documents({"acteurs_principaux": "Tom Cruise"})
    st.write("Morgan Freeman a joué dans {} films.".format(morgan_freeman_count))
    st.write("Tom Cruise a joué dans {} films.".format(tom_cruise_count))


    # Question 4 : Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 4 : Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?</h3>",unsafe_allow_html=True)
    # Les 3 meilleurs films d'horreur
    horror_results = collection.find({"genre": {"$regex": "Horror"}}, sort=[("score",-1)], limit=3)
    st.markdown("<h4 style='text-align: left; color: black;'>Les 3 meilleurs films d'horreur sont :</h4>",unsafe_allow_html=True)
    for result in horror_results:
        st.write(result['titre'], result['score'])
        
        
    # Les 3 meilleurs films dramatiques
    st.markdown("<h4 style='text-align: left; color: black;'>Les 3 meilleurs films dramatiques sont :</h4>",unsafe_allow_html=True)
    drama_results = collection.find({"genre": {"$regex": "Drama"}}, sort=[("score",-1)], limit=3)
    for result in drama_results:
        st.write(result['titre'], result['score'])
        
        
    # Les 3 meilleurs films comiques
    st.markdown("<h4 style='text-align: left; color: black;'>Les 3 meilleurs films comiques :</h4>",unsafe_allow_html=True)
    comedy_results = collection.find({"genre": {"$regex": "Comedy"}}, sort=[("score",-1)], limit=3)
    for result in comedy_results:
        st.write(result['titre'], result['score'])
        
        
    # Question 5 : Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 5 : Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?</h3>",unsafe_allow_html=True)
    # Trouver les 100 films les mieux notés
    results = collection.find({}, sort=[("score",-1)], limit=100)

    # Compter le nombre de films américains et français
    num_us_films = 0
    num_fr_films = 0
    for result in results:
        if "United States" in result['pays']:
            num_us_films += 1
        elif "France" in result['pays']:
            num_fr_films += 1

    # Calculer les pourcentages
    total_films = 100
    us_percentage = (num_us_films / total_films) * 100
    fr_percentage = (num_fr_films / total_films) * 100

    # Afficher les résultats
    st.markdown("<h5 style='text-align: left; color: black;'>Parmi les 100 films les mieux notés :</h5>",unsafe_allow_html=True)
    st.write("{:.2f}% sont américains.".format(us_percentage))
    st.write("{:.2f}% sont français.".format(fr_percentage))
        

    # Question 6 : Quel est la durée moyenne d’un film en fonction du genre ?
    st.markdown("<h3 style='text-align: left; color: black;'>Question 6 : Quel est la durée moyenne d’un film en fonction du genre ?</h3>", unsafe_allow_html=True)

    # Création de la liste des genres
    genres = collection.distinct("genre")

    # Ajout du sélecteur de genre
    selected_genre = st.selectbox("Sélectionnez un genre :", genres)

    # Pipeline de requête MongoDB pour calculer la durée moyenne des films du genre sélectionné
    pipeline = [
        {"$unwind": "$genre"},
        {"$match": {"genre": selected_genre}},
        {"$group": {"_id": "$genre", "avg_duration": {"$avg": "$duree"}}}
    ]

    # Exécution de la requête et affichage des résultats
    results = collection.aggregate(pipeline)
    for result in results:
        st.write("Le genre {} a une durée moyenne de {:.2f} minutes.".format(result["_id"], result["avg_duration"]))
        
        
    # QUESTION 7 : En fonction du genre, afficher la liste des films les plus longs.
    st.markdown("<h3 style='text-align: left; color: black;'>Question 7 : En fonction du genre, afficher la liste des films les plus longs.</h3>", unsafe_allow_html=True)
    # Création de la liste des genres
    genres2 = collection.distinct('genre')

    # Ajout du sélecteur de genre
    selected_genre = st.selectbox("Sélectionnez un genre :", genres,key="selected_genre")

    # Pipeline de requête MongoDB pour obtenir la liste des films les plus longs du genre sélectionné
    pipeline = [
        {"$unwind": "$genre"},
        {"$match": {"genre": selected_genre}},
        {"$sort": {"duree": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "titre": 1, "duree": 1}}
    ]

    # Exécution de la requête et affichage des résultats
    results = collection.aggregate(pipeline)

    st.write("Les 10 films les plus longs du genre {} sont :".format(selected_genre))
    for result in results:
        st.write("- {} ({:.0f} minutes)".format(result["titre"], result["duree"])) 
    
    
    # QUESTION 8 : En fonction du genre, quel est le coût de tournage d'une minute de film ? 
    # st.markdown("<h3 style='text-align: left; color: black;'>Question 8 : En fonction du genre, quel est le coût de tournage d’une minute de film ?</h3>", unsafe_allow_html=True)
    # # Création de la liste des genres
    # genres = collection.distinct("genre")

    # # Ajout du sélecteur de genre
    # selected_genre = st.selectbox("Sélectionnez un genre :", genres)

    # # Pipeline de requête MongoDB pour obtenir le coût de tournage par minute du genre sélectionné
    # pipeline = [
    #     {"$unwind": "$genre"},
    #     {"$match": {"genre": selected_genre}},
    #     {"$project": {"_id": 0, "titre": 1, "duree": 1, "cout": 1, "cout_par_minute": {"$divide": ["$cout", "$duree"]}}}
    # ]

    # # Exécution de la requête et affichage des résultats
    # results = collection.aggregate(pipeline)

    # st.write("Le coût de tournage par minute du genre {} est :".format(selected_genre))
    # for result in results:
    #     st.write("- {} : ${:.2f}".format(result["titre"], result["cout_par_minute"]))
    
    
    # QUESTION 9 : Quels sont les séries les mieux notées ? 
    st.markdown("<h3 style='text-align: left; color: black;'>Question 9 : Quels sont les séries les mieux notées ?</h3>", unsafe_allow_html=True)
    
    collection = db["series"]
    # Création du selecteur avec des choix allant de 10 en 10 jusqu'à 250
    n_choices = list(range(5, 251, 5))
    n = st.selectbox("Sélectionnez un nombre de séries à afficher :", n_choices)

    # Pipeline de requête MongoDB pour obtenir les séries les mieux notées
    pipeline = [
        {"$sort": {"Score": -1}},
        {"$limit": n},
        {"$project": {"_id": 0, "Title": 1, "Score": 1}}
    ]

    # Exécution de la requête et affichage des résultats
    results = collection.aggregate(pipeline)

    st.write("Les {} séries les mieux notées sont :".format(n))
    for result in results:
        st.write("- {} (score : {})".format(result["Title"], result["Score"]))



if choix == "Moteur de recherche" :
    
    st.title("Moteur de recherche de films")

    # liste déroulante pour sélectionner le type de recherche
    type_recherche = st.selectbox("Choisissez le type de recherche:", ["Titre", "Acteur", "Genre"])

    terme_recherche = st.text_input("Entrez le terme de recherche:")
            

    # élément de saisie numérique pour filtrer la durée des films
    duree_max = st.number_input("Durée maximale en minutes:", value=120)

    # élément de saisie numérique pour filtrer la note des films
    note_min = st.number_input("Note minimale:", value=7.0, min_value=0.0, max_value=10.0, step=0.1)


    # bouton pour lancer la recherche
    if st.button("Rechercher"):
        # recherche des films correspondants dans la collection MongoDB en fonction du type de recherche choisi et du filtre de durée
        if type_recherche == "Titre":
            resultats = collection.find({"titre": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})
            nb_resultats = collection.count_documents({"titre": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})

        elif type_recherche == "Acteur":
            resultats = collection.find({"acteurs_principaux": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})
            nb_resultats = collection.count_documents({"acteurs_principaux": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})

        if type_recherche == "Genre":
            resultats = collection.find({"genre": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})
            nb_resultats = collection.count_documents({"genre": {"$regex": terme_recherche, "$options": "i"}, "duree": {"$lt": duree_max}, "score": {"$gt": str(note_min)}})

    
        # affichage du nombre de résultats
        st.write(f"<div style='text-align:center;'>Nombre de résultats trouvés : {nb_resultats}</div>", unsafe_allow_html=True)
        st.write("<br>",unsafe_allow_html=True)
        
        # affichage des résultats
        results_found = False
        for resultat in resultats:
            results_found = True
            
            st.write("<h3 style='text-align: center;'>", resultat["titre"],"</h3>", unsafe_allow_html=True)
            st.write('<br>',unsafe_allow_html=True)

            
            col1, col2,col3 = st.columns(3)
            with col1:
                st.image(resultat["image_url"])
            with col2:
                st.write("Genre(s) : ")
                for genre in resultat['genre']:
                    st.write("-", genre)
            with col3:  
                st.write("Année de sortie :", resultat["annee"])
                st.write("Durée :", resultat["duree"], "minutes")
                st.write("Score :", resultat["score"], "/10")
                st.write("<br>", unsafe_allow_html=True)

        
        if not results_found:
            st.write("Aucun résultat trouvé.")
        
