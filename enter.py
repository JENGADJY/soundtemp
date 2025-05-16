from dotenv import load_dotenv
import requests
import base64
import os
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback"
scopes = "user-top-read"



# changer a chaque demarrage
code = "AQD63gNNM8MqpbhA_fyk_2ETNL4IO9WlOitdLe5X8-GRTG1PKDUJ1VUwcZ7S11YcQZjczaypu9P_hw69MCyzVq7jquCUgIiBZ-0V2vyjRtQKYLkDKKVx6SKdwL60nOEXwgE6TEU1EhGdIkSj1UO-F5DkubM3kaWp7XhR-pcOPk-LR1m7sSfbRt8xdMZcNAatgT3PRNqQ1bLiMSump-6-emQSV2MHZeGhoL0F2awpq6veD4Oqp6OodXQzVxMCe-kmgIzPzowkYy2O9A"




def get_user_token(code, client_id, client_secret, redirect_uri):
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def get_users_top_items(access_token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "time_range": "medium_term",
        "limit": 10,
        "offset": 0
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if code != None:


        print("Code reçu, récupération du token utilisateur...")
        user_token_data = get_user_token(code, client_id, client_secret, redirect_uri)
        access_token = user_token_data["access_token"]

        print(" Récupération des artistes préférés...")
        top = get_users_top_items(access_token)
        k=[]

        for idx, artist in enumerate(top["items"], 1):
            if artist['genres'] !=[]:
                k.append(artist['genres'])
            print(f"{idx}. {artist['name']} (Genres: {', '.join(artist['genres'])})")
            print(k)
        
        code = None

