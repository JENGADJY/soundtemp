from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.getenv("WEATHER_API")
ville = "Paris"

if not API_KEY:
    print(" Clé API introuvable dans le fichier .env")
    exit()


url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={ville}"

response = requests.get(url)
weather =[]
if response.status_code == 200:
    data = response.json()
    if "current" in data:
        temperature = data["current"]["temperature"]
        description = data["current"]["weather_descriptions"][0]
        print(f"Meteo à {ville} : {temperature}°C, {description}")
    else:
        print(" Erreur dans la réponse : ", data.get("error", {}))
else:
    print(f" Erreur HTTP : {response.status_code}")

weather.append(ville)
weather.append(temperature)
weather.append(description)
print(weather)