from dotenv import load_dotenv

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

params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scopes
}
auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
print("Connecte-toi ici :", auth_url)


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Connexion russie ! Vous pouvez fermer cette page.</h1>")
        else:
            self.send_response(400)
            self.end_headers()

def run_server():
    httpd = HTTPServer(('localhost', 8888), SpotifyAuthHandler)
    httpd.handle_request()  

if __name__ == "__main__":
    print(" Ouverture de la page de connexion Spotify...")
    webbrowser.open(auth_url)


    server_thread = threading.Thread(target=run_server)
    server_thread.start()