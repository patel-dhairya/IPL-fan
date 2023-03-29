import sys
import os
import asyncio
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
age_regex = re.compile(r'\((\d+) years\)')


def create_team(url, team_name) -> list:
    from scrapper import script
    from models import player
    new_team = []
    gt = team_name
    data = asyncio.run(script.main(url))
    for player_data in data:
        player_age = int(age_regex.search(player_data[0]).group(1))
        player_position = player_data[2].strip()
        player_batting = player_data[3].strip().split()[0]
        if not player_position == "WK-Batsman" and ("Right" in player_data[4] or "Left" in player_data[4]):
            player_bowling_hand = player_data[4].strip().split("-")[0]
            player_bowling_type = player_data[4].strip().split()[1]
        else:
            player_bowling_hand, player_bowling_type = "None", "None"
        player_country = player_data[-2]
        player_name = player_data[-1]
        new_team.append(player.Player(player_name, player_age, player_position, player_batting, player_bowling_hand,
                                      player_bowling_type, gt, country=player_country))

    return new_team
