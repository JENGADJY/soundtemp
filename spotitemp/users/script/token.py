import os
import base64
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback"  # doit être déclaré sur Spotify Dev Dashboard
scopes = "user-top-read"

def get_authorization_url(client_id, redirect_uri, scopes):
    return (
        f"https://accounts.spotify.com/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
    )

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

def main():
    if not client_id or not client_secret:
        print("  Les identifiants SPOTIFY_CLIENT et SPOTIFY_CLIENT_SECRET sont manquants dans le fichier .env")
        return

    auth_url = get_authorization_url(client_id, redirect_uri, scopes)
    print(" Ouvre ce lien dans ton navigateur pour autoriser l'application :")
    print(auth_url)
    print()

    code = input(" Colle ici le code obtenu dans l'URL de redirection : ").strip()

    try:
        token_data = get_user_token(code, client_id, client_secret, redirect_uri)
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]

        print("\n Token obtenu avec succès !")
        print("Access Token :", access_token[:40], "...")
        print("Refresh Token :", refresh_token[:40], "...")


        with open("spotify_tokens.env", "w") as f:
            f.write(f"REFRESH_TOKEN={refresh_token}\n")
        print(" Refresh token sauvegardé dans spotify_tokens.env")

    except requests.exceptions.HTTPError as e:
        print(" Erreur HTTP :", e)
        print(" Réponse Spotify :", e.response.json())

if __name__ == "__main__":
    main()
