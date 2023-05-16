"""
This script creates sqlite3 database called ipl to store data.

Author: Dhairya Patel,
Create Date: Unknown,
Update Date: May 16, 2023
"""


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
            "Team ID" INTEGER PRIMARY KEY AUTOINCREMENT,
            Team TEXT NOT NULL,
            "Short Name" TEXT NOT NULL,
            "Home Stadium" TEXT NOT NULL
        )
    ''')

    # Add teams to teams table
    insert_team = "INSERT INTO teams (Team, \"Short Name\", \"Home Stadium\") VALUES (?, ?, ?)"
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
    # Full Name : str
    #     Full name of player
    # Age : str
    #     The age of the player when the data on player was last update on website
    # General Role : str
    #     The general role of the player in the team (e.g. batsman, bowler, all-rounder).
    # Specific Role : str
    #     The specialized role of the player if exist such as top order batter or batting all-rounder
    # Batting Hand : str
    #     The batting style of the player (e.g. right-handed, left-handed).
    # Bowling hand : str
    #     The hand with which the player balls (e.g. right, left).
    # Bowling Style : str
    #     The bowling style of the player (e.g. fast, spin).
    # Team : str
    #     The name of the team the player belongs to.
    # Home Country : str
    #     The home country of player
    ipl_cursor.execute('''
     CREATE TABLE IF NOT EXISTS players (
         "Player ID" INTEGER PRIMARY KEY AUTOINCREMENT,
         Name TEXT NOT NULL,
         "Full Name" TEXT NOT NULL,
         Age TEXT CHECK(Age LIKE '%y %d' AND CAST(SUBSTR(Age, INSTR(Age, ' ') + 1, LENGTH(Age) - INSTR(Age, ' ')) AS 
         INTEGER) BETWEEN 1 AND 364),
         "General Role" TEXT NOT NULL,
         "Specific Role" TEXT NOT NULL,
         "Batting Hand" TEXT NOT NULL,
         "Bowling Hand" TEXT NOT NULL,
         "Bowling Type" TEXT NOT NULL,
         Team TEXT NOT NULL,
         "Home Country" TEXT NOT NULL,
         FOREIGN KEY (Team) REFERENCES teams ("Short Name")
         )
    ''')

    # Convert player-data in csv file to sql query format and add it to players table
    with open("player_data.csv", "r") as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip header

        # Modify some data of csv file to add it to sql database
        for row in csv_data:
            name, full_name, age, batting_style, bowling_style, role, country, team = row
            batting_hand = "Right" if "right" in batting_style.lower() else "Left"

            # I would like one column which suggest one general role between bowler, batsman, all-rounder and
            # wicketkeeper rather than specific role such as batting all-rounder or top order batter
            if "batter" in role.lower():
                if "wicketkeeper" in role.lower():
                    general_role = "Wicketkeeper"
                else:
                    general_role = "Batter"
            elif "allrounder" in role.lower():
                general_role = "Allrounder"
            else:
                general_role = "Bowler"

            # I would also like a specific column which gives information about bowling hand of bowler if player
            # has ever bowled
            # General cricket fact - Leg-break bowlers are generally right arm wrist spinner
            if "left" in bowling_style.lower():
                bowling_hand = "Left"
            elif "right" in bowling_style.lower() or "legbreak" in bowling_style.lower():
                bowling_hand = "Right"
            else:
                bowling_hand = "None"

            add_query = '''
            INSERT INTO players (Name, "Full Name", Age, "General Role", "Specific Role", "Batting Hand", "Bowling Hand"
            , "Bowling Type", Team, "Home Country") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            ipl_cursor.execute(add_query, (name, full_name, age, general_role, role, batting_hand, bowling_hand,
                                           bowling_style, team, country))

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
    # Stadium : str
    #   Name of stadium where match took place
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
    # Powerplay score(i1) : int
    #   Score of team batting first in first six overs
    # Powerplay score(i2) : int
    #   Score of team batting second in first six overs
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
        "Match ID" INTEGER PRIMARY KEY,
        "Home Team" TEXT NOT NULL,
        "Away Team" TEXT NOT NULL,
        Stadium TEXT NOT NULL,
        "Toss Win" TEXT NOT NULL,
        "Field First" INTEGER NOT NULL CHECK ("Field First" IN (0, 1)),
        Winner TEXT NOT NULL,
        "Man of the match" TEXT NOT NULL,
        "Match time" INTEGER NOT NULL CHECK ("Match time" IN (0, 1)),
        "Score(i1)" TEXT NOT NULL DEFAULT '0/0' CHECK("Score(i1)" LIKE '%/%' AND "Score(i1)" GLOB '[0-9]*/[0-9]*'),
        "Score(i2)" TEXT NOT NULL DEFAULT '0/0' CHECK("Score(i2)" LIKE '%/%' AND "Score(i2)" GLOB '[0-9]*/[0-9]*'),
        "Powerplay score(i1)" TEXT NOT NULL DEFAULT '0/0' CHECK("Powerplay score(i1)" LIKE '%/%' AND
        "Powerplay score(i1)" GLOB '[0-9]*/[0-9]*'),
        "Powerplay score(i2)" TEXT NOT NULL DEFAULT '0/0' CHECK("Powerplay score(i2)" LIKE '%/%' AND
        "Powerplay score(i2)" GLOB '[0-9]*/[0-9]*'),
        "High score(i1)" INTEGER NOT NULL,
        "High scorer(i1)" TEXT NOT NULL ,
        "Best bowler(i1)" TEXT NOT NULL,
        "Best bowling(i1)" TEXT NOT NULL DEFAULT '0/0' CHECK("Best bowling(i1)" LIKE '%/%' AND "Best bowling(i1)" GLOB 
        '[0-9]*/[0-9]*'),
        "High score(i2)" INTEGER NOT NULL,
        "High scorer(i2)" TEXT NOT NULL ,
        "Best bowler(i2)" TEXT NOT NULL ,
        "Best bowling(i2)" TEXT NOT NULL DEFAULT '0/0' CHECK("Best bowling(i2)" LIKE '%/%' AND "Best bowling(i2)" GLOB 
        '[0-9]*/[0-9]*'),
        

        FOREIGN KEY ("Home Team") REFERENCES teams ("Short Name"),
        FOREIGN KEY ("Away Team") REFERENCES teams ("Short Name"),
        FOREIGN KEY ("Toss Win") REFERENCES teams ("Short Name"),
        FOREIGN KEY (Winner) REFERENCES teams ("Short Name"),
        FOREIGN KEY ("Man of the match") REFERENCES players (Name),
        FOREIGN KEY ("High scorer(i1)") REFERENCES players (Name),
        FOREIGN KEY ("Best bowler(i1)") REFERENCES players (Name),
        FOREIGN KEY ("High scorer(i2)") REFERENCES players (Name),
        FOREIGN KEY ("Best bowler(i2)") REFERENCES players (Name)
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
    # Match Played (bat): int
    #     The total number of matches player got opportunity to bat
    # Runs (bat) : int
    #     The total number of runs scored by the player
    # Balls (bat) : int
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
    # Out (lbw) : int
    #     The total number of times the player was out by lbw
    # Catches (field) : int
    #     The total number of catches taken by the player in the field
    # Run outs (field) : int
    #     The total number of run outs achieved by the player in the field
    # Stumping (field) : int
    #     The total number of times the player has stumped out a batsman in the field
    # Match Played (ball) : int
    #     The total number of matches where player was part of bowling attack
    # Balls (field) : int
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
    # Wicket-lbw : int
    #     The total number of wickets taken by the player through lbw
    # Best Figure : str
    #     The best figure captured by player in single match
    # Five Wickets : int
    #     Number of times player has taken 5 wickets or more in single match

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Player Stats Summary" (
        "Player ID" INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        "Match Played (bat)" INTEGER NOT NULL DEFAULT 0,
        "Runs (bat)" INTEGER NOT NULL DEFAULT 0,
        "Balls (bat)" INTEGER NOT NULL DEFAULT 0,
        "4s" INTEGER NOT NULL DEFAULT 0,
        "6s" INTEGER NOT NULL DEFAULT 0,
        "Half Centuries" INTEGER NOT NULL DEFAULT 0,
        "Centuries" INTEGER NOT NULL DEFAULT 0,
        "Duck outs" INTEGER NOT NULL DEFAULT 0,
        "Highest Score" INTEGER NOT NULL DEFAULT 0,
        NO INTEGER NOT NULL DEFAULT 0,
        "Out (catch)" INTEGER NOT NULL DEFAULT 0,
        "Out (run out)" INTEGER NOT NULL DEFAULT 0,
        "Out (stumped)" INTEGER NOT NULL DEFAULT 0,
        "Out (bowled)" INTEGER NOT NULL DEFAULT 0,
        "Out (lbw)" INTEGER NOT NULL DEFAULT 0,
        "Catches (field)" INTEGER NOT NULL DEFAULT 0,
        "Run outs (field)" INTEGER NOT NULL DEFAULT 0,
        "Stumping (field)" INTEGER NOT NULL DEFAULT 0,
        "Match Played (ball)" INTEGER NOT NULL DEFAULT 0,
        "Balls (field)" INTEGER NOT NULL DEFAULT 0,
        "Runs Conceded" INTEGER NOT NULL DEFAULT 0,
        Wickets INTEGER NOT NULL DEFAULT 0,
        "Wicket-catch" INTEGER NOT NULL DEFAULT 0,
        "Wicket-bowled" INTEGER NOT NULL DEFAULT 0,
        "Wicket-stumped" INTEGER NOT NULL DEFAULT 0,
        "Wicket-lbw" INTEGER NOT NULL DEFAULT 0,
        "Best Figure" TEXT NOT NULL DEFAULT '0/0'
        )
    ''')

    # Copy the name of player from original player database
    ipl_cursor.execute('''
        INSERT INTO "Player Stats Summary" ("Player ID", Name)
        SELECT "Player Id", Name
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
    # Balls : int
    #     The total number of balls faced by the player in this match
    # 4s : int
    #     The total number of 4s scored by the player in this match
    # 6s : int
    #     The total number of 6s scored by the player in this match
    # Not out : int
    #     Shows weather player was not out while batting in this match. 0 for out and 1 for not out.
    # Out type : str
    #     Shows how player got out in this match if player batted in this match.
    #     Options are catch out, lbw, stumped, run out, bowled
    # Wicket bowling style : str
    #     Shows if player got out then what was the bowling style if player got out except by run out
    # Wicket bowler : str
    #     Shows which bowler was responsible if player got out by bowled, stumped or caught. None if player was not out
    #     or got run out
    # Fielder : str
    #     Show which fielder was responsible for player dismissal if player got caught, stumped or run out. None if
    #     player was not out or got bowled
    # Man of the match : int
    #     1 if performance of player received man of the match award

    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Batting Performance" (
        "Player ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        "Match ID" INTEGER NOT NULL,
        Opponent TEXT NOT NULL,
        Runs INTEGER NOT NULL DEFAULT 0,
        Balls INTEGER NOT NULL DEFAULT 0,
        "4s" INTEGER NOT NULL DEFAULT 0,
        "6s" INTEGER NOT NULL DEFAULT 0,
        "Not out" INTEGER NOT NULL DEFAULT 0 CHECK ("Not out" IN (0, 1)),
        "Out type" TEXT DEFAULT 'None',
        "Wicket bowling style" TEXT DEFAULT 'None',
        "Wicket bowler" TEXT DEFAULT 'None',
        Fielder TEXT DEFAULT 'None',
        "Man of the match" INTEGER NOT NULL CHECK ("Man of the match" IN (0, 1)),
        
        FOREIGN KEY (Name) REFERENCES players (Name), 
        FOREIGN KEY ("Match ID") REFERENCES matches ("Match ID"),
        FOREIGN KEY (Opponent) REFERENCES teams ("Short Name"),
        FOREIGN KEY ("Wicket bowler") REFERENCES players (Name), 
        FOREIGN KEY (Fielder) REFERENCES players (Name)
        )
    ''')

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def player_bowl_stat_db_create() -> None:
    """
        Create a table of statistics of players in ipl database
        This table will show player's individual performance/stat regarding bowling against each opponent
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
    # Balls : int
    #     The total number of balls bowled by the player in this match
    # Runs conceded : int
    #     The total number of runs given by the player while bowling in this match
    # Wickets : int
    #     The total number of wickets taken by the player in this match
    # Maiden over : int
    #     The total number of maiden overs thrown by bowler (maiden over = 0 runs in over)
    # Dot ball : int
    #     The total number of dot balls thrown by bowler (dot ball = 0 run conceded)
    # 4s conceded : int
    #     Number of boundaries conceded by bowler
    # 6s conceded : int
    #     Number of sixes conceded by bowler
    # Wides : int
    #     Number of wides thrown by bowler
    # No balls : int
    #     Number of no balls thrown by bowler
    # Wicket-catch : int
    #     The total number of wickets taken by the bowler through catches in this match
    # Wicket-bowled : int
    #     The total number of wickets taken by the bowler by hitting the wicket with a ball in this match
    # Wicket-stumped : int
    #     The total number of wickets taken by the bowler through stump out in this match
    # Wicket-lbw : int
    #     The total number of wickets taken by bowler through lbw in this match
    # Field-catch : int
    #     The total number of catches taken by the player in the field in this match
    # Field-runout : int
    #     The total number of run outs player was associated with in this match
    # Field-stumping : int
    #     The total number of times the player has stumped out a batsman in this match
    # Man of the match : int
    #     1 if performance of player received man of the match award

    # Create table
    ipl_cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Bowling Performance" (
        "Player ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        "Match ID" INTEGER NOT NULL,
        Opponent TEXT NOT NULL,
        Balls INTEGER NOT NULL DEFAULT 0,
        "Runs conceded" INTEGER NOT NULL DEFAULT 0,
        Wickets INTEGER NOT NULL DEFAULT 0,
        "Maiden over" INTEGER NOT NULL DEFAULT 0,
        "Dot ball" INTEGER NOT NULL DEFAULT 0,
        "4s conceded" INTEGER NOT NULL DEFAULT 0,
        "6s conceded" INTEGER NOT NULL DEFAULT 0,
        Wides INTEGER NOT NULL DEFAULT 0,
        "No balls" INTEGER NOT NULL DEFAULT 0,
        "Wicket-catch" INTEGER NOT NULL DEFAULT 0,
        "Wicket-bowled" INTEGER NOT NULL DEFAULT 0,
        "Wicket-stumped" INTEGER NOT NULL DEFAULT 0,
        "Wicket-lbw" INTEGER NOT NULL DEFAULT 0,
        "Field-catch" INTEGER NOT NULL DEFAULT 0,
        "Field-runout" INTEGER NOT NULL DEFAULT 0,
        "Field-stumping" INTEGER NOT NULL DEFAULT 0,
        "Man of the match" INTEGER NOT NULL CHECK ("Man of the match" IN (0, 1)),
        
        FOREIGN KEY (Name) REFERENCES players (Name), 
        FOREIGN KEY ("Match ID") REFERENCES matches ("Match ID"),
        FOREIGN KEY (Opponent) REFERENCES teams ("Short Name")
        )
    ''')

    # Close the connection
    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


"""
Comment out following code to create tables
"""

team_db_create()
player_db_create()
match_db_create()
player_total_stats_db_create()
player_bat_stat_db_create()
player_bowl_stat_db_create()
