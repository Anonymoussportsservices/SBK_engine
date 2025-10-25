# odds_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

def get_sports():
    url = f"{BASE_URL}/sports"
    response = requests.get(url, params={"apiKey": API_KEY})
    response.raise_for_status()
    return response.json()

def get_odds(sport_key: str, regions: str = "us", odds_format: str = "decimal"):
    url = f"{BASE_URL}/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "oddsFormat": odds_format
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
