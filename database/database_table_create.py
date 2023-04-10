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
    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Create teams table with team id, short name, team name and home stadium of team
    # Rows information:
    # -----------
    # team_id : int
    #   Auto incrementing team id for primary key of table
    # short_name : str
    #   Short name of team
    # team_name : str
    #   Name of team
    # home_stadium : str
    #   Name of home stadium of team
    ipl_cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_name TEXT NOT NULL,
            team_name TEXT NOT NULL,
            home_stadium TEXT NOT NULL
        )
    ''')

    # Add teams to teams table
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

    # Save the changes
    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def player_db_create() -> None:
    """
    Create a table of players in ipl database.
    :return: None
    """

    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Rows information:
    # -----------
    # player_name : str
    #     The name of the player.
    # age : int
    #     The age of the player.
    # position : str
    #     The role of the player in the team (e.g. batsman, bowler, all-rounder).
    # batting_hande : str
    #     The batting style of the player (e.g. right-handed, left-handed).
    # bowling_hand : str
    #     The hand with which the player bowls (e.g. right, left).
    # bowling_style : str
    #     The bowling style of the player (e.g. fast, spin).
    # team : str
    #     The name of the team the player belongs to.
    # home_country : str
    #     The home country of player
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

    # Convert player-data in csv file to sql query format and add it to players table
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
    """
    Create a table of matches played in ipl database.
    :return: None
    """

    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Rows information
    # -----------
    # home_team : str
    #   Home team in the match
    # away_team : str
    #   Away team in the match
    # toss_win : str
    #   Name of team that won toss
    # toss_win_field_first : int/bool
    #   0 if winner of toss decided to bat first else 1
    # winner : str
    #   Name of team that won match
    # man_of_the_match : str
    #   Name of player that won man of the match award
    # night_match : int/bool
    #   0 if match was played in afternoon else 1
    # score_inning1 : str
    #   Runs scored by team batting first in format of runs/wickets. (Ex. 205/2)
    # score_inning2 : str
    #   Runs scored by team batting second in format of runs/wickets
    # score_inning1_highest_score : int
    #   Runs of player who scored the highest run in team batting first
    # score_inning1_highest_scorer : str
    #   Name of player who scored the highest run in first batting team
    # score_inning1_best_bowler : str
    #   Name of player who bowled best in first inning
    # score_inning1_best_bowling : str
    #   Bowling figure of player who bowled best in first inning in format of runs/wickets
    # score_inning2_highest_score : int
    #   Runs of player who scored the highest run in team batting second
    # score_inning2_highest_scorer : str
    #   Name of player who scored the highest run in second batting team
    # score_inning2_best_bowler : str
    #   Name of player who bowled best in second inning
    # score_inning2_best_bowling : str
    #   Bowling figure of player who bowled best in second inning in format of runs/wickets

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
        score_inning1 TEXT NOT NULL DEFAULT '0/0' CHECK(score_inning1 LIKE '%/%' AND score_inning1 GLOB '[0-9]*/[0-9]*')
        ,
        score_inning2 TEXT NOT NULL DEFAULT '0/0' CHECK(score_inning1 LIKE '%/%' AND score_inning1 GLOB '[0-9]*/[0-9]*')
        ,
        score_inning1_highest_score INTEGER NOT NULL,
        score_inning1_highest_scorer TEXT NOT NULL ,
        score_inning1_best_bowler TEXT NOT NULL,
        score_inning1_best_bowling TEXT NOT NULL DEFAULT '0/0' CHECK(score_inning1 LIKE '%/%' AND score_inning1 GLOB 
        '[0-9]*/[0-9]*'),
        score_inning2_highest_score INTEGER NOT NULL,
        score_inning2_highest_scorer TEXT NOT NULL ,
        score_inning2_best_bowler TEXT NOT NULL ,
        score_inning2_best_bowling TEXT NOT NULL DEFAULT '0/0' CHECK(score_inning1 LIKE '%/%' AND score_inning1 GLOB 
        '[0-9]*/[0-9]*'),
        

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
    """
    Create a table of statistics of players in ipl database
    :return: None
    """

    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Rows information
    # -----------
    # player_name : str
    #   The name of the player.
    # match_played : int
    #     The total number of matches played by the player
    # batting_runs_scored : int
    #     The total number of runs scored by the player
    # batting_bowls_played : int
    #     The total number of balls faced by the player while batting
    # batting_boundary : int
    #     The total number of 4s scored by the player
    # batting_six : int
    #     The total number of 6s scored by the player
    # batting_half_century : int
    #     The total number of half centuries scored by the player (50+ runs in an innings)
    # batting_century : int
    #     The total number of centuries scored by the player (100+ runs in an innings)
    # batting_duck_out : int
    #     The total number of innings the player was out without scoring any runs
    # highest_score : int
    #     The highest score the player has achieved in any innings
    # batting_not_out : int
    #     Number of times player stayed not out while batting and playing more than 0 ball
    # out_catch : int
    #     The total number of times the player was out caught
    # out_run_out : int
    #     The total number of times the player was run out
    # out_stumped : int
    #     The total number of times the player was stumped out
    # out_bowled : int
    #     The total number of times the player was bowled out
    # field_catch : int
    #     The total number of catches taken by the player in the field
    # field_run_out : int
    #     The total number of run outs achieved by the player in the field
    # field_stumping : int
    #     The total number of times the player has stumped out a batsman in the field
    # bowling_bowls : int
    #     The total number of balls bowled by the player
    # bowling_runs : int
    #     The total number of runs given by the player while bowling
    # bowling_wickets : int
    #     The total number of wickets taken by the player
    # bowling_wicket_catch : int
    #     The total number of wickets taken by the player through catches
    # bowling_wicket_bowled : int
    #     The total number of wickets taken by the player by hitting the wicket with a ball
    # bowling_wicket_stump : int
    #     The total number of wickets taken by the player through stump out
    # bowling_best_figures : str
    #     The best figure captured by player in single match
    # bowling_five_wickets : int
    #     Number of times player has taken 5 wickets or more in single match

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stat (
        player_id INTEGER PRIMARY KEY,
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
        batting_not_out INTEGER NOT NULL DEFAULT 0,
        out_catch INTEGER NOT NULL DEFAULT 0,
        out_run_out INTEGER NOT NULL DEFAULT 0,
        out_stumped INTEGER NOT NULL DEFAULT 0,
        out_bowled INTEGER NOT NULL DEFAULT 0,
        field_catch INTEGER NOT NULL DEFAULT 0,
        field_run_out INTEGER NOT NULL DEFAULT 0,
        field_stumping INTEGER NOT NULL DEFAULT 0,
        bowling_bowls INTEGER NOT NULL DEFAULT 0,
        bowling_runs INTEGER NOT NULL DEFAULT 0,
        bowling_wickets INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_catch INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_bowled INTEGER NOT NULL DEFAULT 0,
        bowling_wicket_stump INTEGER NOT NULL DEFAULT 0,
        bowling_best_figure TEXT NOT NULL DEFAULT '0/0' CHECK(bowling_best_figure LIKE '%/%' AND 
        bowling_best_figure GLOB '[0-9]*/[0-9]*'),
        bowling_five_wickets INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Copy the name of player from original player database
    ipl_cursor.execute('''
        INSERT INTO player_stat (player_id, player_name)
        SELECT player_id, player_name
        FROM players
    ''')

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


# team_db_create()
# player_db_create()
# match_db_create()
# player_stat_db_create()