import requests

API_KEY = "144860df72732f4b94bd117fa019ec18"
ville = "Paris"

url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric&lang=fr"
response = requests.get(url)

print(response.status_code)
print(response.text)
