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
    ipl_cursor = ipl_db.cursor()
    ipl_cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_name TEXT NOT NULL,
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
    ipl_cursor.close()
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
    ipl_cursor = ipl_db.cursor()
    ipl_cursor.execute('''
     CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
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
            ipl_cursor.execute("INSERT INTO players (player_name, age, position, batting_hand, bowling_hand, "
                               "bowling_type, team, home_country) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row[:-1])

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def match_db_create() -> None:
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()
    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
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
    ipl_cursor.close()
    ipl_db.close()


def player_stat_db_create() -> None:
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()
    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stat (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        match_played INTEGER NOT NULL DEFAULT 0,
        batting_runs_scored INTEGER NOT NULL DEFAULT 0,
        batting_bowls_played INTEGER NOT NULL DEFAULT 0,
        batting_boundary INTEGER NOT NULL DEFAULT 0,
        batting_six INTEGER NOT NULL DEFAULT 0,
        batting_half_century INTEGER NOT NULL DEFAULT 0,
        batting_century INTEGER NOT NULL DEFAULT 0,
        batting_duck_out INTEGER NOT NULL DEFAULT 0,
        highest_score INTEGER NOT NULL DEFAULT 0,
        batting_not_out INTEGER NOT NULL DEFAULT 0
        out_catch INTEGER NOT NULL DEFAULT 0,
        out_run_out INTEGER NOT NULL DEFAULT 0,
        out_stumped INTEGER NOT NULL DEFAULT 0,
        out_bowled INTEGER NOT NULL DEFAULT 0,
        field_catch INTEGER NOT NULL DEFAULT 0,
        field_run_out INTEGER NOT NULL DEFAULT 0,
        field_stumping INTEGER NOT NULL DEFAULT 0,
        field_catch_miss INTEGER NOT NULL DEFAULT 0,
        bowling_bowls INTEGER NOT NULL DEFAULT 0,
        bowling_runs INTEGER NOT NULL DEFAULT 0,
        bowling_wickets INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_catch INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_bowled INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_stump INTEGER NOT NULL DEFAULT 0,
        bowling_best_figure TEXT NOT NULL DEFAULT '0/0',
        bowling_five_wickets INTEGER NOT NULL DEFAULT 0,
    ''')
#
# def player_stat_db_add(player_name, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0, out_style=None,
#                        not_out=False, catch=0, run_out=0, catch_miss=0, stumping=0, bowling_bowl=0, bowling_run=0,
#                        wicket_taken=0, wicket_taken_catch=0, wicket_taken_bowled=0, wicket_taken_stump=0) -> None:
#     """
#         Adds data to the player's record for a match they played in
#
#         Parameters:
#         player_name (str): the name of player
#         batting_run (int): the number of runs scored by the player while batting
#         batting_bowl (int): the number of balls faced by the player while batting
#         batting_4 (int): the number of fours scored by the player while batting
#         batting_6 (int): the number of sixes scored by the player while batting
#         out_style (str): the way the player was dismissed (catch, run-out, stump, bowled) or None if not out
#         not_out (bool): True if the player was not out, False otherwise
#         catch (int): the number of catches taken by the player in the field
#         run_out (int): the number of run outs executed by the player in the field
#         catch_miss (int): the number of catches missed by the player in the field
#         stumping (int): the number of stumpings executed by the player in the field
#         bowling_bowl (int): the number of balls bowled by the player
#         bowling_run (int): the number of runs given away by the player while bowling
#         wicket_taken (int): the number of wickets taken by the player while bowling
#         wicket_taken_catch (int): the number of wickets taken by the player through catches
#         wicket_taken_bowled (int): the number of wickets taken by the player through bowleds
#         wicket_taken_stump (int): the number of wickets taken by the player through stumpings
#
#         Returns:
#         None
#         """
#     ipl_db = sqlite3.connect("ipl.db")

# team_db_write()
# player_db_create()
# match_db_create()
