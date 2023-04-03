import csv
import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def team_db_create() -> None:
    """
    Create team table in ipl database
    :return: None
    """
    ipl_db = sqlite3.connect("ipl.db")
    ipl_db.execute('''
        CREATE TABLE teams (
            short_name TEXT PRIMARY KEY,
            team_name TEXT NOT NULL,
            home_stadium TEXT NOT NULL
        )
    ''')

    insert_team = "INSERT INTO teams (team_name, short_name, home_stadium) VALUES (?, ?, ?)"
    ipl_db.execute(insert_team, ("Gujarat Titans", "GT", "Narendra Modi Stadium"))
    ipl_db.execute(insert_team, ("Chennai Super Kings", "CSK", "MA Chidambaram Stadium"))
    ipl_db.execute(insert_team, ("Delhi Capitals", "DC", "Arun Jaitley Stadium"))
    ipl_db.execute(insert_team, ("Punjab Kings", "PBKS", "Punjab Cricket Association IS Bindra Stadium"))
    ipl_db.execute(insert_team, ("Kolkata Knight Riders", "KKR", "Eden Gardens"))
    ipl_db.execute(insert_team, ("Mumbai Indians", "MI", "Wankhede Stadium"))
    ipl_db.execute(insert_team, ("Rajasthan Royals", "RR", "Barsapara Cricket Stadium"))
    ipl_db.execute(insert_team, ("Royal Challengers Bangalore", "RCB", "M.Chinnaswamy Stadium"))
    ipl_db.execute(insert_team, ("Sunrisers Hyderabad", "SRH", "Rajiv Gandhi International Stadium"))
    ipl_db.execute(insert_team, ("Lucknow Super Giants", "LSG", "Atal Bihari Vajpayee Ekana Cricket Stadium"))

    ipl_db.commit()
    ipl_db.close()


def player_db_create() -> None:
    """
    Create a table of players in ipl database.
    Attributes:
    -----------
    player_name : str
        The name of the player.
    age : int
        The age of the player.
    position : str
        The role of the player in the team (e.g. batsman, bowler, all-rounder).
    batting_hande : str
        The batting style of the player (e.g. right-handed, left-handed).
    bowling_hand : str
        The hand with which the player bowls (e.g. right, left).
    bowling_style : str
        The bowling style of the player (e.g. fast, spin).
    team : str
        The name of the team the player belongs to.
    home_country : str
        The home country of player
    :return: None
    """
    ipl_db = sqlite3.connect("ipl.db")
    ipl_db.execute('''
     CREATE TABLE players (
        player_name TEXT PRIMARY KEY,
        age INTEGER NOT NULL,
        position TEXT NOT NULL,
        batting_hand TEXT NOT NULL,
        bowling_hand TEXT NOT NULL,
        bowling_type TEXT NOT NULL,
        team TEXT NOT NULL,
        home_country TEXT NOT NULL,
        FOREIGN KEY (team) REFERENCES teams (short_name)
        )
    ''')
    with open("player-data.csv", "r") as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip header
        for row in csv_data:
            ipl_db.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row[:-1])

    ipl_db.commit()
    ipl_db.close()


def match_db_create() -> None:
    ipl_db = sqlite3.connect("ipl.db")
    ipl_db.execute('''
    CREATE TABLE matches (
        match_id INTEGER PRIMARY KEY,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        toss_win TEXT NOT NULL,
        toss_win_field_first INTEGER NOT NULL CHECK (toss_win_field_first IN (0, 1)),
        winner TEXT NOT NULL,
        man_of_the_match TEXT NOT NULL,
        night_match INTEGER NOT NULL CHECK (night_match IN (0, 1)),
        score_inning1 TEXT NOT NULL,
        score_inning2 TEXT NOT NULL,
        score_inning1_highest_score INTEGER NOT NULL,
        score_inning1_highest_scorer TEXT NOT NULL ,
        score_inning1_best_bowler TEXT NOT NULL,
        score_inning1_best_bowling TEXT NOT NULL,
        score_inning2_highest_score INTEGER NOT NULL,
        score_inning2_highest_scorer TEXT NOT NULL ,
        score_inning2_best_bowler TEXT NOT NULL,
        score_inning2_best_bowling TEXT NOT NULL,
        

        FOREIGN KEY (home_team) REFERENCES teams (short_name),
        FOREIGN KEY (away_team) REFERENCES teams (short_name),
        FOREIGN KEY (toss_win) REFERENCES teams (short_name),
        FOREIGN KEY (winner) REFERENCES teams (short_name),
        FOREIGN KEY (man_of_the_match) REFERENCES players (player_name),
        FOREIGN KEY (score_inning1_highest_scorer) REFERENCES players (player_name),
        FOREIGN KEY (score_inning1_best_bowler) REFERENCES players (player_name),
        FOREIGN KEY (score_inning2_highest_scorer) REFERENCES players (player_name),
        FOREIGN KEY (score_inning2_best_bowler) REFERENCES players (player_name)
        )
    ''')
    ipl_db.commit()
    ipl_db.close()


# team_db_write()
# player_db_create()
# match_db_create()