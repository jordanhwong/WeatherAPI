import os
import requests

from flask import Flask, jsonify

from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
print (API_KEY)

    
@app.route('/weather/<location>', methods=['GET'])
def get_weather(location):

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code