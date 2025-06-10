import os
import requests
import redis

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)

exp_time = 60 * 60 * 24  # 24 hours

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

try:
    r = redis.Redis(
    host='redis-17625.c289.us-west-1-2.ec2.redns.redis-cloud.com',
    port=17625,
    decode_responses=True,
    username="default",
    password=REDIS_PASSWORD,
    )
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


    
@app.route('/<location>')
def get_weather(location):
    
    try:
        cached_data = r.get(location)
        if cached_data:
            print(f"Cache hit for location: {location}")
            return jsonify({"source": "cache", "data": cached_data})
    except redis.RedisError as e:
        print(f"Error fetching from Redis: {e}")

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        r.setex(location, time=exp_time, value=response.text)
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code
    
if __name__ == '__main__':
    app.run(debug=True)