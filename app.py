from flask import Flask, jsonify, request
from flask_cors import CORS 
from datetime import datetime

import random
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://cwmxi-frontend-cynf.vercel.app"}}, supports_credentials=True)


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

# Function to select players
def select_players():
    selected_batsmen = random.sample(players["batsmen"], 3)
    selected_bowlers = random.sample(players["bowlers"], 3)
    return selected_batsmen, selected_bowlers

@app.route("/start-game", methods=["GET"])
def start_game():
    team1 = Team("Team 1")
    team2 = Team("Team 2")

    for team in [team1, team2]:
        batsmen, bowlers = select_players()
        for name in batsmen:
            team.add_batsman(Player(name))
        for name in bowlers:
            team.add_bowler(Player(name))

    return jsonify({
        "team1": {
            "batsmen": [p.name for p in team1.batsmen],
            "bowlers": [p.name for p in team1.bowlers]
        },
        "team2": {
            "batsmen": [p.name for p in team2.batsmen],
            "bowlers": [p.name for p in team2.bowlers]
        }
    })

# @app.route("/simulate-game", methods=["GET"])
# def simulate_game():
#     team1 = Team("Team 1")
#     team2 = Team("Team 2")
    
#     # Simulate the game for both teams
#     for team in [team1, team2]:
#         # Update runs for each batsman
#         for player in team.batsmen:
#             player.update_runs(random.randint(0, 100))
#         # Update wickets for each bowler
#         for player in team.bowlers:
#             player.update_wickets(random.randint(0, 5))
#         # Update team points based on the players' performance
#         team.update_points()
    
#     # Prepare the response data
#     response_data = {
#         "team1": {
#             "total_points": team1.total_points
#         },
#         "team2": {
#             "total_points": team2.total_points
#         },
#         "difference": abs(team1.total_points - team2.total_points)
#     }

#     # Print the response data to the console
#     print("Response Data:", response_data)

#     # Return the response as JSON
#     return jsonify(response_data)


@app.route("/todays-match", methods=["GET"])
def todays_match():
    # Get today's date in the same format as the match data
    today_date = datetime.now().strftime("%Y-%m-%d")

    print(f'Today Date {today_date}')

    # Filter out matches that are happening today
    todays_matches = [
        {
            "teams": match["teams"],
            "venue": match["venue"]
        }
        for match in matches_info['match_data'] if match["date"] == today_date
    ]

    # If there is a match today, return it
    if todays_matches:
        return jsonify(todays_matches), 200
    else:
        return jsonify({"message": "No match scheduled for today"}), 404

@app.route('/get_team_squad', methods=['POST'])
def get_team_squad():
    # Get the squad name from the POST request

    print("Incoming squad request:", request.headers)

    data = request.get_json()  # Parse the incoming JSON request
    squad_name = data.get("squad_name")  # Extract the squad name

    squad_info = teams_info['teamsInfo']

    squad_players = []
    for squad in squad_info:
        if squad['teamName'] == squad_name:
            squad_players = squad['players']

    print(f'Squad Players {squad_players}')

    if squad_players:
        # Return the squad details for the requested team
        return jsonify({"team_name": squad_name, "squad": squad_players}), 200
    else:
        # If team is not found, return an error message
        return jsonify({"error": "Team not found"}), 404

if __name__ == "__main__":

    # File path to your local JSON file
    file_path = 'teams_info.json'  # Replace with your actual file path if different
    match_data_path = 'matches_data.json'

    # Open and read the JSON file
    with open(file_path, 'r') as file:
        teams_info = json.load(file)

    with open(match_data_path, 'r') as match_file:
        matches_info = json.load(match_file)

    # Access the parsed data
    print(teams_info)
    #print(matches_info)

    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    app.run(host="0.0.0.0", port=port)
