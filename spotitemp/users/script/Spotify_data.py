from dotenv import load_dotenv, dotenv_values
import requests
import base64
import os
from collections import Counter
import subprocess

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback"
scopes = "user-top-read"


code = ""

def get_user_token(code, client_id, client_secret, redirect_uri):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def refresh_access_token(refresh_token, client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_users_top_items(access_token):
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
    response.raise_for_status()
    return response.json()


config = dotenv_values("spotify_tokens.env")
refresh_token = config.get("REFRESH_TOKEN")

def launch_main_script():
    print(" Aucune clé trouvée. Lancement de main.py pour obtenir un code...")
    subprocess.run(["python3", "users\\script\\token.py"], check=True)

    config = dotenv_values("spotify_tokens.env")
    return config.get("REFRESH_TOKEN")

if refresh_token:
    print(" Utilisation du refresh_token existant")
    access_token = refresh_access_token(refresh_token, client_id, client_secret)

elif code:
    print(" Première connexion : récupération d'un nouveau refresh_token...")
    try:
        user_token_data = get_user_token(code, client_id, client_secret, redirect_uri)
        access_token = user_token_data["access_token"]
        refresh_token = user_token_data["refresh_token"]
        with open("spotify_tokens.env", "w") as f:
            f.write(f"REFRESH_TOKEN={refresh_token}\n")
    except requests.exceptions.HTTPError as e:
        print(" Erreur avec le code existant. Lancement de main.py pour en obtenir un nouveau...")
        refresh_token = launch_main_script()
        if not refresh_token:
            raise ValueError(" Impossible d'obtenir un refresh_token depuis main.py.")
        access_token = refresh_access_token(refresh_token, client_id, client_secret)

else:
    refresh_token = launch_main_script()
    if not refresh_token:
        raise ValueError(" Impossible d'obtenir un refresh_token depuis main.py.")
    access_token = refresh_access_token(refresh_token, client_id, client_secret)
    raise ValueError(" Aucun code ni refresh_token disponible.")

print(" Récupération des artistes préférés...")
top = get_users_top_items(access_token)
genres = []

#for idx, artist in enumerate(top["items"], 1):
#    if artist['genres']:
#        genres.extend(artist['genres'])
#    print(f"{idx}. {artist['name']} (Genres: {', '.join(artist['genres'])})")

diction_genres_raw = Counter(genres)
total_genres = sum(diction_genres_raw.values())


diction_genres = {
    genre: round((count / total_genres) * 100, 2)
    for genre, count in diction_genres_raw.items()
}
    #print(diction_genres)





