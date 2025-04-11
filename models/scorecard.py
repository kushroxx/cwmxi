from dataclasses import dataclass
from typing import Optional, List, Dict
from rapidfuzz.fuzz import partial_ratio


@dataclass
class PlayerPerformance:
    innings: str
    player: str
    type: str  # "Batsman" or "Bowler"
    status: str
    R: Optional[str]  # Runs
    B: Optional[str]  # Balls faced
    Min: Optional[str]  # Minutes batted
    fours: Optional[str]  # Number of 4s
    sixes: Optional[str]  # Number of 6s
    O: Optional[str]  # Overs bowled
    M: Optional[str]  # Maidens
    W: Optional[str]  # Wickets
    SR: Optional[str]  # Strike Rate
    ER: Optional[str]  # Economy Rate


def is_same_player(name1, name2):
    return partial_ratio(name1.lower(), name2.lower()) > 80

class Scorecard:
    def __init__(self, scorecard: Dict[str, List[PlayerPerformance]]):
        self.scorecard = scorecard  # dict of innings → list of PlayerPerformance

    def get_runs(self, player_name: str, team_name: str) -> Optional[int]:
        print(f"🔍 Searching for RUNS for player: {player_name}")
        
        for innings_name, performances in self.scorecard.items():
            print(f"📋 Innings: {innings_name}")
            if innings_name.strip().lower() == team_name.strip().lower():
                for p in performances:
                    #print(f"  ➤ Checking performance: {p.player} - Runs: {p.R}")
                    p_name = p.player.strip().lower()
                    input_name = player_name.strip().lower()
                    if p_name == input_name or is_same_player(input_name, p_name) and p.R is not None:
                        try:
                            return int(p.R)
                        except ValueError:
                            print(f"⚠️ Could not convert runs '{p.R}' to int for player {p.player}")
                            return None
        
        print(f"❌ No runs found for {player_name}")
        return None

    def get_wickets(self, player_name: str, team_name: str) -> Optional[int]:
        print(f"🔍 Searching for WICKETS for player: {player_name}")
        
        for innings_name, performances in self.scorecard.items():
            print(f"📋 Innings: {innings_name}")
            if innings_name.strip().lower() != team_name.strip().lower():
                for p in performances:
                    print(f"  ➤ Checking performance: {p.player} - Wickets: {p.W}")
                    p_name = p.player.strip().lower()
                    input_name = player_name.strip().lower()
                    if p_name == input_name or is_same_player(input_name, p_name) and p.W is not None:
                        try:
                            return int(p.W)
                        except ValueError:
                            print(f"⚠️ Could not convert runs '{p.W}' to int for player {p.player}")
                            return None
        
        print(f"❌ No wickets found for {player_name}")
        return None
    
    def print_scorecard(self):
        for innings, performances in self.scorecard.items():
            print(f"Innings: {innings}")
            for performance in performances:
                print(f"  Performance: {performance}")


def parse_scorecard(data: dict) -> Scorecard:
    scorecard_dict: Dict[str, List[PlayerPerformance]] = {}

    for innings_name, performances in data.get("scorecard", {}).items():
        clean_innings_name = innings_name.replace(" 1 INN", "").replace(" 2 INN", "")
        scorecard_dict[clean_innings_name] = []
        for p in performances:
            scorecard_dict[clean_innings_name].append(PlayerPerformance(
                innings=p.get("innings", clean_innings_name),
                player=p.get("player"),
                type=p.get("type"),
                status=p.get("status"),
                R=p.get("R"),
                B=p.get("B"),
                Min=p.get("Min"),
                fours=p.get("4s"),
                sixes=p.get("6s"),
                O=p.get("O"),
                M=p.get("M"),
                W=p.get("W"),
                SR=p.get("SR"),
                ER=p.get("ER"),
            ))

    return Scorecard(scorecard=scorecard_dict)
