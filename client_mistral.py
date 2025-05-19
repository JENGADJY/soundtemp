from mistralai import Mistral
from dotenv import load_dotenv 
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from Spotify_data import diction_genres
from weather_data import weather

load_dotenv()

MistralKey= os.getenv("MISTRAL_KEY")
MistralAgent=os.getenv("MISTRAL_AGENT")

client=Mistral(api_key=MistralKey)
content =f"voici les genres en pourcentages: {diction_genres} , {weather}"
response =client.agents.complete(
    agent_id=MistralAgent,
    messages=[{"role":"user","content":content}]
)
print(print(response.choices[0].message.content.strip()))