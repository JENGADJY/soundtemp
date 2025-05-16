from mistralai import Mistral
from dotenv import load_dotenv 
import os


from enter import diction_genres

load_dotenv()

MistralKey= os.getenv("MISTRAL_KEY")
MistralAgent=os.getenv("MISTRAL_AGENT")

client=Mistral(api_key=MistralKey)

content ="voici les genres en pourcentages:"+ diction_genres ,
response =client.agents.complete(
    agent_id=MistralAgent,
    message=[{"role":"user","content":content}]
)
print(response_text=response.choices[0].messages.content.strip())