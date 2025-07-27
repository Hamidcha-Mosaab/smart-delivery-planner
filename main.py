# 📦 Projet : Optimisation de livraison intelligente avec Machine Learning

import random
import sqlite3
import requests
import geopy.distance
from dotenv import load_dotenv
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import joblib
from textblob import TextBlob

# Charger les clés API
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENROUTE_API_KEY = os.getenv("OPENROUTE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Connexion à la base SQLite
conn = sqlite3.connect('livraison.db')
cursor = conn.cursor()

# Création de la table d'historique
cursor.execute('''
CREATE TABLE IF NOT EXISTS historique_livraisons (
    lieu TEXT PRIMARY KEY,
    commentaire TEXT,
    traffic TEXT,
    route_rurale BOOLEAN
)''')
conn.commit()

def ajouter_historique(lieu, commentaire, traffic, route_rurale):
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO historique_livraisons (lieu, commentaire, traffic, route_rurale)
            VALUES (?, ?, ?, ?)
        ''', (lieu, commentaire, traffic, route_rurale))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur ajout historique : {e}")

def load_historique():
    try:
        cursor.execute('SELECT * FROM historique_livraisons')
        rows = cursor.fetchall()
        return {row[0]: {'commentaire': row[1], 'traffic': row[2], 'route_rurale': bool(row[3])} for row in rows}
    except sqlite3.Error as e:
        print(f"Erreur chargement historique : {e}")
        return {}

def entrainer_modele_traffic():
    historique = load_historique()
    data = []
    for lieu, infos in historique.items():
        lat, lon = map(float, lieu.split(','))
        data.append({
            'lat': lat,
            'lon': lon,
            'commentaire': infos['commentaire'],
            'traffic': infos['traffic'],
            'route_rurale': infos['route_rurale']
        })
    df = pd.DataFrame(data)
    if df.empty:
        return
    df['traffic'] = LabelEncoder().fit_transform(df['traffic'])
    X = df[['lat', 'lon', 'route_rurale']]
    y = df['traffic']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, 'modele_traffic.joblib')

def predire_traffic_ml(coord, route_rurale):
    try:
        model = joblib.load("modele_traffic.joblib")
        lat, lon = coord
        prediction = model.predict([[lat, lon, int(route_rurale)]])[0]
        return ["bas", "moyen", "élevé"][prediction]
    except:
        return "moyen"

def est_route_rurale(coord):
    query = f"""
    [out:json];
    way(around:500,{coord[0]},{coord[1]})["highway"~"unclassified|tertiary|residential|track"];
    out;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": query}).json()
    return len(response.get("elements", [])) > 0

def obtenir_conditions_meteo(coord):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={coord[0]}&lon={coord[1]}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if "weather" in response:
        return response["weather"][0]["description"], response["main"]["temp"]
    return "Inconnu", 0

def calculer_penalites(client, historique):
    penalites = 0
    if client in historique:
        if historique[client]['traffic'] == "élevé":
            penalites += 5
        if historique[client]['route_rurale']:
            penalites += 2
    return penalites

def clusteriser_clients(livraisons):
    coords = list(livraisons.values())
    model = KMeans(n_clusters=min(2, len(coords)))
    labels = model.fit_predict(coords)
    clustered = {}
    for label, (client, coord) in zip(labels, livraisons.items()):
        clustered.setdefault(label, {})[client] = coord
    return clustered

def calculer_distance_api(coord1, coord2):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={OPENROUTE_API_KEY}&start={coord1[1]},{coord1[0]}&end={coord2[1]},{coord2[0]}"
    response = requests.get(url).json()
    return response.get("routes", [{}])[0].get("summary", {}).get("distance", float('inf')) / 1000

def sentiment_commentaire(commentaire):
    score = TextBlob(commentaire).sentiment.polarity
    if score > 0.1:
        return "positif"
    elif score < -0.1:
        return "négatif"
    else:
        return "neutre"

def trouver_meilleur_client(livraisons, lieu_actuel, historique):
    meilleur, meilleure_dist = None, float('inf')
    for client, position in livraisons.items():
        dist = calculer_distance_api(lieu_actuel, position) + calculer_penalites(client, historique)
        if dist < meilleure_dist:
            meilleure_dist, meilleur = dist, client
    return meilleur

def optimiser_itineraire(livraisons, lieu_actuel, historique):
    itineraire = []
    while livraisons:
        meilleur = trouver_meilleur_client(livraisons, lieu_actuel, historique)
        if meilleur:
            itineraire.append(meilleur)
            lieu_actuel = livraisons[meilleur]
            del livraisons[meilleur]
        else:
            break
    return itineraire

def obtenir_position_client():
    return (random.uniform(48.8566, 48.8569), random.uniform(2.3522, 2.3525))

def livraison_journaliere():
    entrainer_modele_traffic()
    position_livreur = (48.8566, 2.3522)
    livraisons = {
        f"Client {i+1}": obtenir_position_client() for i in range(5)
    }
    historique = load_historique()
    clusters = clusteriser_clients(livraisons)
    for cluster, clients in clusters.items():
        print(f"\n✨ Cluster {cluster} :")
        itineraire = optimiser_itineraire(clients, position_livreur, historique)
        print("Itinéraire optimisé :", itineraire)
        for client in itineraire:
            print(f"\n✉ Livraison à {client}")
            coord = livraisons[client]
            meteo, temp = obtenir_conditions_meteo(coord)
            print(f"Météo : {meteo}, Température : {temp}°C")
            commentaire = input(f"Commentaire pour {client} : ")
            route_rurale = est_route_rurale(coord)
            traffic = predire_traffic_ml(coord, route_rurale)
            humeur = sentiment_commentaire(commentaire)
            print(f"Analyse du commentaire : {humeur}")
            ajouter_historique(f"{coord[0]},{coord[1]}", commentaire, traffic, route_rurale)

if __name__ == "__main__":
    livraison_journaliere()

conn.close()