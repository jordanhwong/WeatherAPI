import os
import requests


from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

if dotenv_path:
    load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
print (API_KEY)

url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Milpitas?key=" + API_KEY
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
    response.raise_for_status()