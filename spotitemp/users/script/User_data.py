from dotenv import load_dotenv, dotenv_values
import requests
import base64
import os
from collections import Counter
import subprocess

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
#veuillez demarrer le replit qui heberge ce site
redirect_uri = "https://94dec92d-c760-4a77-a82a-26aa6a6123eb-00-4vps2voh1hnd.picard.replit.dev/callback"
scopes = "user-top-read"


