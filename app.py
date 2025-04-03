from flask import Flask, jsonify, request
from flask_cors import CORS 

import random
import os

app = Flask(__name__)
CORS(app)

# Sample players
players = {
    "batsmen": ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6"],
    "bowlers": ["Bowler1", "Bowler2", "Bowler3", "Bowler4", "Bowler5", "Bowler6"]
}

# Points System
RUN_POINTS = 10
WICKET_POINTS = 100

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

@app.route("/simulate-game", methods=["GET"])
def simulate_game():
    team1 = Team("Team 1")
    team2 = Team("Team 2")
    
    # Simulate the game for both teams
    for team in [team1, team2]:
        # Update runs for each batsman
        for player in team.batsmen:
            player.update_runs(random.randint(0, 100))
        # Update wickets for each bowler
        for player in team.bowlers:
            player.update_wickets(random.randint(0, 5))
        # Update team points based on the players' performance
        team.update_points()
    
    # Prepare the response data
    response_data = {
        "team1": {
            "total_points": team1.total_points
        },
        "team2": {
            "total_points": team2.total_points
        },
        "difference": abs(team1.total_points - team2.total_points)
    }

    # Print the response data to the console
    print("Response Data:", response_data)

    # Return the response as JSON
    return jsonify(response_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    app.run(host="0.0.0.0", port=port)
