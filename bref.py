from dotenv import load_dotenv
import os
import urllib.parse
import webbrowser
import time
import requests
from bs4 import BeautifulSoup

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback" 
scopes = "user-top-read"

params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scopes
}
auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"

print(" Connecte-toi ici :", auth_url)
webbrowser.open(auth_url)

# On attnd un peu que l'utilisateur accepte
print(" Attente de la redirection (ouvre le lien dans le navigateur)...")
time.sleep(10)

# Récupération du code dans la page HTML Replit
try:
    response = requests.get(redirect_uri)
    soup = BeautifulSoup(response.text, "html.parser")
    code_tag = soup.find("code")
    if code_tag:
        code = code_tag.text.strip()
        print(" Code récupéré automatiquement :", code)
    else:
        print(" Aucune balise <code> trouvée dans la page HTML.")
except Exception as e:
    print(" Erreur lors de la requête :", e)
