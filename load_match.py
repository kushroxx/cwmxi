import requests
import json
import os
from datetime import date

# Constants
API_KEY = "5f556563a900af1db9a030733da1a6fd42d94ada701cd181c30879d1dea00743"
API_URL = "https://apiv2.api-cricket.com/cricket/"
LEAGUE_KEY = "745"
CACHE_FILE = "todays_match.json"

def fetch_from_api(today):
    print("🔄 Fetching from API...")
    params = {
        "method": "get_events",
        "APIkey": API_KEY,
        "date_start": today,
        "date_stop": today,
        "league_key": LEAGUE_KEY
    }

    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == 1 and data["result"]:
            with open(CACHE_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return data
    return None

def load_or_fetch():
    #today = date.today().isoformat()
    today = "2025-04-10"

    # Check if cache exists and is for today's date
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cached_data = json.load(f)
            if cached_data["result"]:
                event_date = cached_data["result"][0]["event_date_start"]
                if event_date == today:
                    print("✅ Loaded from cache")
                    return cached_data

    # Else, fetch new data
    return fetch_from_api(today)