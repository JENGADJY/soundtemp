from dotenv import load_dotenv, dotenv_values
import requests
import base64
import os
import subprocess

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scopes = "user-top-read"


code = ""


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


# config = dotenv_values("spotify_tokens.env")
# refresh_token = config.get("REFRESH_TOKEN")

# def launch_main_script():
#     print(" Aucune clé trouvée. Lancement de main.py pour obtenir un code...")
#     subprocess.run(["python3", "users\\script\\token.py"], check=True)

#     config = dotenv_values("spotify_tokens.env")
#     return config.get("REFRESH_TOKEN")

# if refresh_token:
#     print(" Utilisation du refresh_token existant")
#     access_token = refresh_access_token(refresh_token, client_id, client_secret)

# elif code:
#     print(" Première connexion : récupération d'un nouveau refresh_token...")
#     try:
#         user_token_data = get_user_token(code, client_id, client_secret, REDIRECT_URI)
#         access_token = user_token_data["access_token"]
#         refresh_token = user_token_data["refresh_token"]
#         with open("spotify_tokens.env", "w") as f:
#             f.write(f"REFRESH_TOKEN={refresh_token}\n")
#     except requests.exceptions.HTTPError as e:
#         print(" Erreur avec le code existant. Lancement de main.py pour en obtenir un nouveau...")
#         refresh_token = launch_main_script()
#         if not refresh_token:
#             raise ValueError(" Impossible d'obtenir un refresh_token depuis main.py.")
#         access_token = refresh_access_token(refresh_token, client_id, client_secret)

# else:
#     refresh_token = launch_main_script()
#     if not refresh_token:
#         raise ValueError(" Impossible d'obtenir un refresh_token depuis main.py.")
#     access_token = refresh_access_token(refresh_token, client_id, client_secret)
#     raise ValueError(" Aucun code ni refresh_token disponible.")









