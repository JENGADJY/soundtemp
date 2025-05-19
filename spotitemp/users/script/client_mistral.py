from mistralai import Mistral
from dotenv import load_dotenv 
import os
import sys
from .Spotify_data import diction_genres
from .weather_data import weather

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

MistralKey= os.getenv("MISTRAL_KEY")
MistralAgent=os.getenv("MISTRAL_AGENT")
rep=[]
def reco(diction_genres,weather):

    client=Mistral(api_key=MistralKey)
    content =f"voici les genres en pourcentages: {diction_genres} , {weather}"
    response =client.agents.complete(
        agent_id=MistralAgent,
        messages=[{"role":"user","content":content}]
    )
    rep.append(response.choices[0].message.content.strip())
    return rep

reco(diction_genres,weather)