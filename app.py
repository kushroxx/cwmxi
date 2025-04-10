from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from datetime import datetime, date

from load_match import load_or_fetch, fetch_from_api
from models.match import Match
import pytz

import random
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins temporarily

# Sample players
players = {
    "batsmen": ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6"],
    "bowlers": ["Bowler1", "Bowler2", "Bowler3", "Bowler4", "Bowler5", "Bowler6"]
}

# Points System
RUN_POINTS = 10
WICKET_POINTS = 100

teams_info = []
matches_info = []
match_data = []
current_match = None

class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.wickets = 0
        self.points = 0

    def update_runs(self, runs):
        self.runs += runs
        self.points += runs * RUN_POINTS

    def update_wickets(self, wickets):
        self.wickets += wickets
        self.points += wickets * WICKET_POINTS

class Team:
    def __init__(self, name):
        self.name = name
        self.batsmen = []
        self.bowlers = []
        self.total_points = 0

    def add_batsman(self, batsman):
        self.batsmen.append(batsman)

    def add_bowler(self, bowler):
        self.bowlers.append(bowler)

    def update_points(self):
        self.total_points = sum(p.points for p in self.batsmen + self.bowlers)

RESULTS_FILE = "results_history.json"

def store_historical_data(selected_data: dict, player1_results, player2_results):
    # Load existing results
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            match_results = json.load(f)
    else:
        match_results = {}

    if current_match.status == "Finished":
        print("Match is finished. Calculating points.")
        player1_total = sum(p["points"] for p in player1_results)
        player2_total = sum(p["points"] for p in player2_results)

        print(f"Player 1 total points: {player1_total}")
        print(f"Player 2 total points: {player2_total}")

        match_id = current_match.event_key
        home_team = current_match.home_team['name']
        away_team = current_match.away_team['name']
        match_desc = f"{home_team} vs {away_team}"
        match_date = current_match.date

        # If this match_id is not already stored, add it
        if match_id not in match_results:
            match_results[match_id] = {
                "players": [
                    [selected_data["player1_name"], player1_total],
                    [selected_data["player2_name"], player2_total]
                ],
                "match_desc": match_desc,
                "match_date": match_date,
            }
            # Save updated results to file
            with open(RESULTS_FILE, "w") as f:
                json.dump(match_results, f, indent=4)

            print(f"Results saved for match {match_id}.")
        else:
            print(f"Results for match {match_id} already exist. Skipping save.")

def get_player_points(selected_data: dict, scorecard) -> dict:
    def calculate_points(player_info, scorecard):
        name = player_info["name"]
        role = player_info["role"]
        team_name = player_info["team"]

        print(f"Calculating points for {name} with role {role}")
        #scorecard.print_scorecard()

        if current_match.status == "Upcoming":
            print(f"Match is upcoming. No points to calculate for {name}.")

        if role == "Batsman":

            if current_match.status == "Upcoming":
                runs = 0
            else:
                runs = scorecard.get_runs(name, team_name)
            print(f"Player {name} scored {runs}")
            return {
                "name": name,
                "role": role,
                "runs": runs or 0,
                "points": (runs or 0) * 10
            }
        elif role == "Bowler":
            if current_match.status == "Upcoming":
                wickets = 0
            else:
                wickets = scorecard.get_wickets(name, team_name)
            print(f"Player {name} took {wickets}")
            return {
                "name": name,
                "role": role,
                "wickets": wickets or 0,
                "points": (wickets or 0) * 100
            }

        return {"name": name, "role": role, "points": 0}
    
    #print("Selected data for points calculation:", selected_data)
    print(f"************START*******************")
    #scorecard.print_scorecard()
    print(f"************END*******************")

    # ✅ PASS scorecard properly here:
    player1_results = [calculate_points(p, scorecard) for p in selected_data["player1_team"]]
    player2_results = [calculate_points(p, scorecard) for p in selected_data["player2_team"]]

    store_historical_data(selected_data, player1_results, player2_results)

    return {
        "player1_name": selected_data["player1_name"],
        "player2_name": selected_data["player2_name"],
        "player1_points": player1_results,
        "player2_points": player2_results
    }


@app.route("/todays-match", methods=["GET"])
def todays_match():
    if not current_match:
        return jsonify({"message": "No match data available"}), 500

    # Check if selected_players.json exists
    if os.path.exists("selected_players.json"):
        status = "selected"
    else:
        status = "not selected"

    return jsonify({
        "match": current_match.to_dict(),
        "status": status
    }), 200

@app.route('/get_team_squad', methods=['GET'])
def get_team_squad():
    squad_name = request.args.get("squad_name")

    if not current_match:
        return jsonify({"error": "Match data unavailable"}), 500

    squad, logo = current_match.get_squad(squad_name)

    if not squad:
        return jsonify({"error": "Team not found"}), 404

    #squad_players = [p["player"] for p in squad]
    return jsonify({
        "team_name": squad_name,
        "squad": squad,
        "team_logo": logo
    }), 200

@app.route("/get_points", methods=["GET"])
def get_points():
    try:
        # Load selected players from local JSON file
        with open("selected_players.json", "r") as f:
            selected_players = json.load(f)

        print("Selected players loaded:", selected_players)

        print(" Refetching data")
        today = date.today().isoformat()
        match_data = fetch_from_api(today)
        current_match = Match(match_data['result'][0])

        # Compute points using current match's scorecard
        result = get_player_points(selected_players, current_match.get_scorecard())

        print("Points calculated:", result)

        return jsonify(result)
    except FileNotFoundError:
        return jsonify({"error": "selected_players.json not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

SAVE_FILE = "selected_players.json"

@app.route('/save_selected_players', methods=['POST'])
def save_selected_players():
    data = request.get_json()

    print("Incoming POST save request:", request.headers)
    print(f"Data: {data}")

    if not data or not all(k in data for k in ["player1_name", "player2_name", "player1_team", "player2_team"]):
        return jsonify({"status": "error", "message": "Invalid data structure"}), 400

    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "success", "message": "Selections saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_saved_players', methods=['GET'])
def get_saved_players():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"status": "error", "message": "No saved file"}), 404

@app.route("/get_match_history", methods=["GET"])
def get_match_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            results = json.load(f)
        return jsonify(results)
    else:
        return jsonify({"error": "No match results found"}), 404

if __name__ == "__main__":

    # File path to your local JSON file
    file_path = 'teams_info.json'  # Replace with your actual file path if different
    match_data_path = 'matches_data.json'

    # Open and read the JSON file
    with open(file_path, 'r') as file:
        teams_info = json.load(file)

    with open(match_data_path, 'r') as match_file:
        matches_info = json.load(match_file)

    # Usage
    match_data = load_or_fetch()

    print("🔄 Loading match data...")
    print("Match data:", match_data['result'][0])

    if match_data:
        current_match = Match(match_data['result'][0])
        print("🏏 Match initialized:", current_match.home_team["name"], "vs", current_match.away_team["name"])
    else:
        print("⚠️ No match found or API failed.")

    #get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist).strftime("%H:%M")
    print("Current time:", current_time_ist)
    print("Match time:", current_match.event_time)
    if current_match.status == "Upcoming" and current_match.event_time < current_time_ist:
        print(" Refetching Data")
        today = date.today().isoformat()
        match_data = fetch_from_api(today)
        current_match = Match(match_data['result'][0])

    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    app.run(host="0.0.0.0", port=port)
