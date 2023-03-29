import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def csv_write() -> None:
    from teams import team_generator

    player_datas = team_generator.teams()
    with open("player-data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Age", "Position", "Batting-Hand", "Bowling-Hand", "Bowling-Type", "Team", "Country",
                         "Captain"])
        for player_data in player_datas:
            row = list(player_data.__dict__.values())
            writer.writerow(row)
