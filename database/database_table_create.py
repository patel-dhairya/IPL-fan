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
            Team ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Team TEXT NOT NULL,
            "Short Name" TEXT NOT NULL,
            "Home Stadium" TEXT NOT NULL
        )
    ''')

    # Add teams to teams table
    insert_team = "INSERT INTO teams (Team, 'Short Name', 'Home Stadium') VALUES (?, ?, ?)"
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
    # Name : str
    #     The name of the player.
    # Age : int
    #     The age of the player.
    # Position : str
    #     The role of the player in the team (e.g. batsman, bowler, all-rounder).
    # Batting Hand : str
    #     The batting style of the player (e.g. right-handed, left-handed).
    # Bowling hand : str
    #     The hand with which the player bowls (e.g. right, left).
    # Bowling Style : str
    #     The bowling style of the player (e.g. fast, spin).
    # Team : str
    #     The name of the team the player belongs to.
    # Home Country : str
    #     The home country of player
    ipl_cursor.execute('''
     CREATE TABLE IF NOT EXISTS players (
        'Player ID' INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Age INTEGER NOT NULL,
        Position TEXT NOT NULL,
        'Batting Hand' TEXT NOT NULL,
        'Bowling Hand' TEXT NOT NULL,
        'Bowling Type' TEXT NOT NULL,
        Team TEXT NOT NULL,
        'Home Country' TEXT NOT NULL,
        
        FOREIGN KEY (Team) REFERENCES teams (Short Name)
        )
    ''')

    # Convert player-data in csv file to sql query format and add it to players table
    with open("player-data.csv", "r") as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip header
        for row in csv_data:
            ipl_cursor.execute("INSERT INTO players (Name, Age, Position, 'Batting Hand', 'Bowling Hand', "
                               "'Bowling Type', Team, 'Home Country') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row[:-1])

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
    # Home Team : str
    #   Home team in the match
    # Away Team : str
    #   Away team in the match
    # Toss Win : str
    #   Name of team that won toss
    # Field First : int/bool
    #   0 if winner of toss decided to bat first else 1
    # Winner : str
    #   Name of team that won match
    # Man of the match : str
    #   Name of player that won man of the match award
    # Match time : int/bool
    #   0 if match was played in afternoon else 1
    # Score(i1) : str
    #   Runs scored by team batting first in format of runs/wickets. (Ex. 205/2)
    # Score(i2) : str
    #   Runs scored by team batting second in format of runs/wickets
    # High score(i1) : int
    #   Runs of player who scored the highest run in team batting first
    # High scorer(i1) : str
    #   Name of player who scored the highest run in first batting team
    # Best bowler(i1) : str
    #   Name of player who bowled best in first inning
    # Best bowling(i1) : str
    #   Bowling figure of player who bowled best in first inning in format of runs/wickets
    # High score(i2) : int
    #   Runs of player who scored the highest run in team batting second
    # High scorer(i2) : str
    #   Name of player who scored the highest run in second batting team
    # Best bowler(i2) : str
    #   Name of player who bowled best in second inning
    # Best bowling(i2) : str
    #   Bowling figure of player who bowled best in second inning in format of runs/wickets

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        'Match ID' INTEGER PRIMARY KEY,
        'Home Team' TEXT NOT NULL,
        'Away Team' TEXT NOT NULL,
        'Toss Win' TEXT NOT NULL,
        'Field First' INTEGER NOT NULL CHECK (Field First IN (0, 1)),
        Winner TEXT NOT NULL,
        'Man of the match' TEXT NOT NULL,
        'Match time' INTEGER NOT NULL CHECK (Match time IN (0, 1)),
        Score(i1) TEXT NOT NULL DEFAULT '0/0' CHECK(Score(i1) LIKE '%/%' AND Score(i1) GLOB '[0-9]*/[0-9]*'),
        Score(i2) TEXT NOT NULL DEFAULT '0/0' CHECK(Score(i2) LIKE '%/%' AND Score(i2) GLOB '[0-9]*/[0-9]*'),
        'High score(i1)' INTEGER NOT NULL,
        'High scorer(i1)' TEXT NOT NULL ,
        'Best bowler(i1)' TEXT NOT NULL,
        'Best bowling(i1)' TEXT NOT NULL DEFAULT '0/0' CHECK(Best bowling(i1) LIKE '%/%' AND Best bowling(i1) GLOB 
        '[0-9]*/[0-9]*'),
        'High score(i2)' INTEGER NOT NULL,
        'High scorer(i2)' TEXT NOT NULL ,
        'Best bowler(i2)' TEXT NOT NULL ,
        'Best bowling(i2)' TEXT NOT NULL DEFAULT '0/0' CHECK(Best bowling(i2) LIKE '%/%' AND Best bowling(i2) GLOB 
        '[0-9]*/[0-9]*'),
        

        FOREIGN KEY ('Home Team') REFERENCES teams ('Short Name'),
        FOREIGN KEY ('Away Team') REFERENCES teams ('Short Name'),
        FOREIGN KEY ('Toss Win') REFERENCES teams ('Short Name'),
        FOREIGN KEY (Winner) REFERENCES teams ('Short Name'),
        FOREIGN KEY ('Man of the match') REFERENCES players (Name),
        FOREIGN KEY ('High scorer(i1)') REFERENCES players (Name),
        FOREIGN KEY ('Best bowler(i1)') REFERENCES players (Name),
        FOREIGN KEY ('High scorer(i2)') REFERENCES players (Name),
        FOREIGN KEY ('Best bowler(i2)') REFERENCES players (Name)
        )
    ''')
    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def player_total_stats_db_create() -> None:
    """
    Create a table of statistics of players in ipl database
    This table will show total statistics/performance of player (total runs, total wickets taken in and so on)
    :return: None
    """

    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Rows information
    # -----------
    # Name : str
    #   The name of the player.
    # Match Played : int
    #     The total number of matches played by the player
    # Runs (bat) : int
    #     The total number of runs scored by the player
    # Bowls (bat) : int
    #     The total number of balls faced by the player while batting
    # 4s : int
    #     The total number of 4s scored by the player
    # 6s : int
    #     The total number of 6s scored by the player
    # Half Centuries : int
    #     The total number of half centuries scored by the player (50+ runs in an innings)
    # Centuries : int
    #     The total number of centuries scored by the player (100+ runs in an innings)
    # Duck outs : int
    #     The total number of innings the player was out without scoring any runs (scored 0 runs)
    # Highest Score : int
    #     The highest score the player has achieved in any innings
    # NO : int
    #     Number of times player stayed not out while batting and playing more than 0 ball
    # Out (catch) : int
    #     The total number of times the player was out by catch
    # Out (run out) : int
    #     The total number of times the player was run out
    # Out (stumped) : int
    #     The total number of times the player was stumped out
    # Out (bowled) : int
    #     The total number of times the player was bowled out
    # Catches (field) : int
    #     The total number of catches taken by the player in the field
    # Run outs (field) : int
    #     The total number of run outs achieved by the player in the field
    # Stumping (field) : int
    #     The total number of times the player has stumped out a batsman in the field
    # Bowls (ball) : int
    #     The total number of balls bowled by the player
    # Runs Conceded : int
    #     The total number of runs given by the player while bowling
    # Wickets : int
    #     The total number of wickets taken by the player
    # Wicket-catch : int
    #     The total number of wickets taken by the player through catches
    # Wicket-bowled : int
    #     The total number of wickets taken by the player by hitting the wicket with a ball
    # Wicket-stumped : int
    #     The total number of wickets taken by the player through stump out
    # Best Figure : str
    #     The best figure captured by player in single match
    # Five Wickets : int
    #     Number of times player has taken 5 wickets or more in single match

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'Player Stats Summary' (
        'Player ID' INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        'Match Played' INTEGER NOT NULL DEFAULT 0,
        'Runs (bat)' INTEGER NOT NULL DEFAULT 0,
        'Bowls (bat)' INTEGER NOT NULL DEFAULT 0,
        4s INTEGER NOT NULL DEFAULT 0,
        6s INTEGER NOT NULL DEFAULT 0,
        'Half Centuries' INTEGER NOT NULL DEFAULT 0,
        'Centuries' INTEGER NOT NULL DEFAULT 0,
        'Duck outs' INTEGER NOT NULL DEFAULT 0,
        'Highest Score' INTEGER NOT NULL DEFAULT 0,
        NO INTEGER NOT NULL DEFAULT 0,
        'Out (catch)' INTEGER NOT NULL DEFAULT 0,
        'Out (run out)' INTEGER NOT NULL DEFAULT 0,
        'Out (stumped)' INTEGER NOT NULL DEFAULT 0,
        'Out (bowled)' INTEGER NOT NULL DEFAULT 0,
        'Catches (field)' INTEGER NOT NULL DEFAULT 0,
        'Run outs (field)' INTEGER NOT NULL DEFAULT 0,
        'Stumping (field)' INTEGER NOT NULL DEFAULT 0,
        'Bowls (ball)' INTEGER NOT NULL DEFAULT 0,
        'Runs Conceded' INTEGER NOT NULL DEFAULT 0,
        Wickets INTEGER NOT NULL DEFAULT 0,
        'Wicket-catch' INTEGER NOT NULL DEFAULT 0,
        'Wicket-bowled' INTEGER NOT NULL DEFAULT 0,
        'Wicket-stumped' INTEGER NOT NULL DEFAULT 0,
        'Best Figure' TEXT NOT NULL DEFAULT '0/0' CHECK('Best Figure' LIKE '%/%' AND 'Best Figure' GLOB '[0-9]*/[0-9]*')
        ,
        'Five Wickets' INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Copy the name of player from original player database
    ipl_cursor.execute('''
        INSERT INTO player_stat_summary ('Player ID', Name)
        SELECT 'Player Id', Name
        FROM players
    ''')

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def player_bat_stat_db_create() -> None:
    """
    Create a table of statistics of players in ipl database
    This table will show player's individual performance/stat regarding batting against each opponent
    :return: None
    """

    # Create a connection to the database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    # Rows information
    # -----------
    # Name : str
    #   The name of the player.
    # Match ID : int
    #   The id of match for player's performance
    # Opponent : str
    #   Opponent team in this match
    # Runs : int
    #     The number of runs scored by the player
    # Bowls : int
    #     The total number of balls faced by the player in this match
    # 4s : int
    #     The total number of 4s scored by the player in this match
    # 6s : int
    #     The total number of 6s scored by the player in this match
    # batting_not_out : int
    #     Shows weather player was not out while batting in this match
    # out_type : str
    #     Shows how player got out in this match if player batted in this match
    # field_catch : int
    #     The total number of catches taken by the player in the field in this match
    # field_run_out : int
    #     The total number of run outs player was associated with in this match
    # field_stumping : int
    #     The total number of times the player has stumped out a batsman in this match
    # bowling_bowls : int
    #     The total number of balls bowled by the player in this match
    # bowling_runs : int
    #     The total number of runs given by the player while bowling in this match
    # bowling_wickets : int
    #     The total number of wickets taken by the player in this match
    # man_of_the_match : int
    #     1 if performance of player received man of the match award

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stat_individual (
        player_id INTEGER PRIMARY KEY,
        player_name TEXT NOT NULL,
        match_id INTEGER NOT NULL,
        opponent_team TEXT NOT NULL,
        batting_runs INTEGER NOT NULL DEFAULT 0,
        batting_bowls INTEGER NOT NULL DEFAULT 0,
        batting_boundary INTEGER NOT NULL DEFAULT 0,
        batting_six INTEGER NOT NULL DEFAULT 0,
        batting_not_out INTEGER NOT NULL DEFAULT 0,
        out_type TEXT NOT NULL DEFAULT 'Not Applicable',
        field_catch INTEGER NOT NULL DEFAULT 0,
        field_run_out INTEGER NOT NULL DEFAULT 0,
        field_stumping INTEGER NOT NULL DEFAULT 0,
        bowling_bowls INTEGER NOT NULL DEFAULT 0,
        bowling_runs INTEGER NOT NULL DEFAULT 0,
        bowling_wickets INTEGER NOT NULL DEFAULT 0,
        man_of_the_match INTEGER NOT NULL CHECK (man_of_the_match IN (0, 1)),
        
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (opponent_team) REFERENCES teams (short_name)
        )
    ''')

    # # Copy the name of player from original player database
    # ipl_cursor.execute('''
    #     INSERT INTO player_stat (player_id, player_name)
    #     SELECT player_id, player_name
    #     FROM players
    # ''')

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


team_db_create()
player_db_create()
match_db_create()
player_total_stats_db_create()
player_match_stat_db_create()
