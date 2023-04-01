from dataclasses import dataclass
from datetime import datetime
from team import Team
from player import Player

@dataclass
class Match:
    def __init__(self, date: str, evening_match: bool, home_team: Team, away_team: Team):
        self.date = datetime.strptime(date, '%d/%m/%Y')
        self.noon_match = evening_match
        self.home_team = home_team
        self.away_team = away_team
        self.winner = None
        self.toss = None
        self.toss_win_decision = None
        self.score_inning1 = 0
        self.score_inning1_bowls = 0
        self.score_inning1_wickets = 0
        self.score_inning1_highest_run = None
        self.score_inning1_highest_wicket = None
        self.score_inning2 = 0
        self.score_inning2_bowls = 0
        self.score_inning2_wickets = 0
        self.score_inning2_highest_run = None
        self.score_inning2_highest_wicket = None
        self.stadium = home_team.home_stadium
        self.man_of_match = None

    def add_result(self, toss: Team, decision: Team, score1: int, wicket1: int, high_score_1: int, high_wicket_1: int
                   , score2:int, wicket2: int, high_score_2, high_wicket_2, winner):
        self.toss = toss
        self.toss_win_decision = decision
        self.score_inning1 = score1
        self.score_inning1_wickets = wicket1
