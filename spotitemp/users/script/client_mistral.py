from mistralai import Mistral
from dotenv import load_dotenv 
import os
import sys
from .Spotify_data import recup_artist
from .weather_data import weather

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

MistralKey= os.getenv("MISTRAL_KEY")
MistralAgent=os.getenv("MISTRAL_AGENT")
def recommendation(weather):
    rep=[]
    dictionnaire_des_genres=recup_artist()
    client=Mistral(api_key=MistralKey)
    content =f"voici les genres en pourcentages: {dictionnaire_des_genres} , {weather}"
    response =client.agents.complete(
        agent_id=MistralAgent,
        messages=[{"role":"user","content":content}]
    )
    rep.append(response.choices[0].message.content.strip())
    return rep

recommendation(weather)