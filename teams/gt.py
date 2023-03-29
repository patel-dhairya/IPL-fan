import sys
import os
import asyncio


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# name: str
#     age: int
#     role: str
#     batting_style: str
#     bowling_hand: str
#     bowling_style: str
#     team: Team
#     captain: bool = False
#     overseas: bool = False

def create_team():
    from scrapper import script
    from models import team, player
    gt_team = []
    # gt = team.Team("Gujarat Titans", "GT", "Narendra Modi Stadium")
    # gt_team.append(player.Player("Abhinav Manohar", 28, "Batsman", "Right", "Right", "Leg-break", gt))
    # gt_team.append(player.Player("David Miller", 33, "Batsman", "Left", "Right", "Off-break", gt))
    # gt_team.append(player.Player("Sai Sudharsan", 21, "Batsman", "Left", "Right", "Leg-break", gt))
    data = asyncio.run(script.main())
    dic = {"Age": data[0][0], "Place": data[0][1], "Position": data[0][2], "Side": data[0][3]}
    print(dic)


create_team()
