import csv
import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def db_team_write() -> None:
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
    with open("C:/Users/dpat5/Desktop/PycharmProjects/IPL-fan/player-data.csv", "r") as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip header
        for row in csv_data:
            ipl_db.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row[:-1])

    ipl_db.commit()
    ipl_db.close()
    # match_table = ipl_db.execute('''
    # CREATE TABLE matches (
    #     match_id INTEGER PRIMARY KEY,
    #     home_team TEXT NOT NULL,
    #     away_team TEXT NOT NULL,
    #     winner TEXT NOT NULL,
    #     man_of_the_match TEXT NOT NULL,
    #     night_match INTEGER NOT NULL CHECK (my_bool IN (0, 1)),
    #
    #
    #     FOREIGN KEY (home_team) REFERENCES teams (short_name),
    #     FOREIGN KEY (away_team) REFERENCES teams (short_name),
    #     FOREIGN KEY (winner) REFERENCES teams (short_name),
    #     FOREIGN KEY (man_of_the_match) REFERENCES players (player_name)
    # ''')

    # with open("player-data.csv", "w", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Name", "Age", "Position", "Batting-Hand", "Bowling-Hand", "Bowling-Type", "Team", "Country",
    #                      "Captain"])
    #     for player_data in player_datas:
    #         row = list(player_data.__dict__.values())
    #         writer.writerow(row)


# db_team_write()
# player_db_create()
