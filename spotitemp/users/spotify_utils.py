from collections import Counter
from .script import Spotify_data, weather_data
from mistralai import Mistral
import os
from dotenv import load_dotenv
import requests
from .models import UserProfile
from datetime import datetime, timedelta, timezone

load_dotenv()
MistralKey= os.getenv("MISTRAL_KEY")
MistralAgent=os.getenv("MISTRAL_AGENT")
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scopes = "user-read-email user-top-read"

def refresh_spotify_token(user):
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        print("Profil utilisateur introuvable.")
        return None

    refresh_token = profile.refresh_token

    if not refresh_token:
        return None  # Pas de refresh token dispo

    response = requests.post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    })

    if response.status_code != 200:
        print("Échec du rafraîchissement du token Spotify :", response.text)
        return None

    data = response.json()
    access_token = data.get('access_token')
    expires_in = data.get('expires_in')

    profile.access_token = access_token
    profile.save()

    return access_token


def get_users_top_items(user):
    access_token = get_valid_spotify_token(user)
    if not access_token:
        print("Token Spotify invalide ou absent")
        return None

    url = "https://api.spotify.com/v1/me/top/artists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "time_range": "medium_term",
        "limit": 20,
        "offset": 0
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Erreur lors de la récupération des artistes :", response.json())
        return None

    return response.json()

def get_valid_spotify_token(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("Profil utilisateur introuvable.")
        return None

    refresh_token = profile.refresh_token
    if not refresh_token:
        print("Pas de refresh token disponible.")
        return None

    response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    })

    if response.status_code != 200:
        print("Échec du rafraîchissement du token :", response.text)
        return None

    data = response.json()
    access_token = data.get("access_token")

    if access_token:
        profile.access_token = access_token
        profile.save()
        return access_token

    return None

def recup_artist(user):
    print("Récupération des artistes préférés...")
    top = get_users_top_items(user)

    if top is None:
        print("Aucun top artiste récupéré, token peut être invalide ou expiré.")
        return {}

    genres = []

    for idx, artist in enumerate(top["items"], 1):
        if artist['genres']:
            genres.extend(artist['genres'])
        print(f"{idx}. {artist['name']} (Genres: {', '.join(artist['genres'])})")

    diction_genres_raw = Counter(genres)
    total_genres = sum(diction_genres_raw.values())
    diction_genres = {
        genre: round((count / total_genres) * 100, 2)
        for genre, count in diction_genres_raw.items()
    }
    return diction_genres



def recommendation(user):
    rep=[]
    meteo=weather_data.weather()
    dictionnaire_des_genres=recup_artist(user)
    client=Mistral(api_key=MistralKey)
    content =f"voici les genres en pourcentages: {dictionnaire_des_genres} , {meteo}"
    response =client.agents.complete(
        agent_id=MistralAgent,
        messages=[{"role":"user","content":content}]
    )
    rep.append(response.choices[0].message.content.strip())
    return rep
