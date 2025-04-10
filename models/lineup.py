from dataclasses import dataclass
from typing import List

@dataclass
class Player:
    name: str

@dataclass
class TeamLineup:
    starting_lineups: List[Player]

class Lineups:
    @staticmethod
    def from_dict(data: dict) -> TeamLineup:
        return TeamLineup(
            starting_lineups=[Player(name=p["player"]) for p in data.get("starting_lineups", [])]
        )

