from dotenv import load_dotenv, dotenv_values
import requests
import base64
import os
from collections import Counter

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback"
scopes = "user-top-read"


code = "AQAGy15qSNM7QZNSEMjt3gz-C-C_8WUPnnSPQ1X2UNSb_B_U339jx92wMp9VpNBfNqICQiCJaMELIcuSsPwH9l_kHWiu4WJCikVwdTjLbmEfIG2rcFiDfFVi4t8tsiBQWNKSDYjSW5Ult14ed-vIaosgK_bK1y13GawlYWD2R5Zv3pTmx5ueESbh1NwxkUFHw5gZFA7Gm7Z5kCVm02ajnnbIXAOpngLYMkCrqmGJv7-kYXwK_98RbzxOxh9YBtIeD9uWY0igfZjR9g"

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

if __name__ == "__main__":
    config = dotenv_values("spotify_tokens.env")
    refresh_token = config.get("REFRESH_TOKEN")

    if refresh_token:
        print(" Utilisation du refresh_token existant")
        access_token = refresh_access_token(refresh_token, client_id, client_secret)
    elif code:
        print(" Première connexion : récupération d'un nouveau refresh_token...")
        user_token_data = get_user_token(code, client_id, client_secret, redirect_uri)
        access_token = user_token_data["access_token"]
        refresh_token = user_token_data["refresh_token"]

        
        with open("spotify_tokens.env", "w") as f:
            f.write(f"REFRESH_TOKEN={refresh_token}\n")
    else:
        raise ValueError(" Aucun code ni refresh_token disponible.")

    print(" Récupération des artistes préférés...")
    top = get_users_top_items(access_token)
    genres = []

    for idx, artist in enumerate(top["items"], 1):
        if artist['genres']:
            genres.extend(artist['genres'])
        print(f"{idx}. {artist['name']} (Genres: {', '.join(artist['genres'])})")

    diction_genres = Counter(genres)

    # Affichage du résultat
    print("\nGenres cumuls :")
    for genre, count in diction_genres.items():
        print(f"{genre}: {count*100/20}")  
    
    print(diction_genres)

    def get_response(self, json_str: str) -> str:
        """Envoie une requête à l'API Mistral et retourne la réponse."""
        response = self.client.agents.complete(
            agent_id="ag:753184c9:20250311:untitled-agent:e063ae99",
            messages=[{"role": "user", "content": json_str}]
        )
        return response.choices[0].message.content.strip()
    
