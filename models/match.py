# models/match.py

from models.scorecard import parse_scorecard
from models.lineup import Lineups

from datetime import datetime, timedelta

def add_hours_to_time(time_str, hours_to_add):
    # Parse the input time string into a datetime object
    original_time = datetime.strptime(time_str, "%H:%M")
    
    # Add the hours using timedelta
    new_time = original_time + timedelta(hours=hours_to_add)
    
    # Format back to "HH:MM"
    return new_time.strftime("%H:%M")

class Match:
    def __init__(self, match_data):
        self.event_key = match_data.get("event_key")
        self.date = match_data.get("event_date_start")
        self.venue = match_data.get("event_stadium")
        self.event_time = match_data.get("event_time")

        self.event_time = add_hours_to_time(self.event_time, 3) if self.event_time else None

        print(f"📅 Event date: {self.date}")
        print(f"🕒 Event time: {self.event_time}")
        
        self.home_team = {
            "name": match_data.get("event_home_team"),
            "key": match_data.get("home_team_key"),
            "logo": match_data.get("event_home_team_logo"),
            "final_score": match_data.get("event_home_final_result"),
            "rr": match_data.get("event_home_rr")
        }
        
        self.away_team = {
            "name": match_data.get("event_away_team"),
            "key": match_data.get("away_team_key"),
            "logo": match_data.get("event_away_team_logo"),
            "final_score": match_data.get("event_away_final_result"),
            "rr": match_data.get("event_away_rr")
        }
        
        self.status = match_data.get("event_status")
        self.status_info = match_data.get("event_status_info")
        self.toss = match_data.get("event_toss")
        self.man_of_the_match = match_data.get("event_man_of_match")

        print("📦 Raw scorecard data:", match_data.get("scorecard", {}))


        # Initialize scorecard and lineups
        if self.status == "":
            self.status = "Upcoming"
            self.scorecard = ""
        else:
            self.scorecard = parse_scorecard(match_data)
            print(f"✅ Scorecard parsed with innings: {list(self.scorecard.scorecard.keys())}")

        self.lineups = {
            self.home_team["name"]: Lineups.from_dict(match_data["lineups"]["home_team"]),
            self.away_team["name"]: Lineups.from_dict(match_data["lineups"]["away_team"])
        }

    def get_status(self):
        return self.status

    def get_squad(self, team_name):
        if team_name in self.lineups:
            team_lineup = self.lineups[team_name]
            starting_lineups = [p.name for p in team_lineup.starting_lineups]
            logo = (
                self.home_team["logo"] if team_name == self.home_team["name"]
                else self.away_team["logo"]
            )
            return starting_lineups, logo
        return [], None
    
    def get_scorecard(self):
        return self.scorecard

    def to_dict(self):
        return {
            "teams": [self.home_team["name"], self.away_team["name"]],
            "venue": self.venue,
            "status": self.status,
            "team1_logo": self.home_team["logo"],
            "team2_logo": self.away_team["logo"]
        }
