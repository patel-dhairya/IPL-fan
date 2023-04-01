import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def db_write() -> None:
    from teams import team_generator

    player_datas = team_generator.teams()

    ipl_db = sqlite3.connect("database/ipl.db")
    team_table = ipl_db.execute('''
        CREATE TABLE teams (
            short_name TEXT PRIMARY KEY
            team_name TEXT NOT NULL,
            home_stadium TEXT NOT NULL
        )
    ''')

    player_table = ipl_db.execute('''
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

    match_table = ipl_db.execute('''
    CREATE TABLE matches (
        match_id INTEGER PRIMARY KEY,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        winner TEXT NOT NULL,    
        man_of_the_match TEXT NOT NULL,
        night_match INTEGER NOT NULL CHECK (my_bool IN (0, 1)),
        
        
        FOREIGN KEY (home_team) REFERENCES teams (short_name),
        FOREIGN KEY (away_team) REFERENCES teams (short_name),
        FOREIGN KEY (winner) REFERENCES teams (short_name),
        FOREIGN KEY (man_of_the_match) REFERENCES players (player_name)
    ''')

    player_table = ipl_db.execute("CREATE TABLE table_name")

    # with open("player-data.csv", "w", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Name", "Age", "Position", "Batting-Hand", "Bowling-Hand", "Bowling-Type", "Team", "Country",
    #                      "Captain"])
    #     for player_data in player_datas:
    #         row = list(player_data.__dict__.values())
    #         writer.writerow(row)
