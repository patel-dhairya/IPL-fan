import pandas as pd
import matplotlib.pyplot as plt

"""Comment out following lines only if you want to create a new database
You will need to understand how web scrapping work if you want to customise data from website.
Please look at script.py file in scrapper directory if you want to change how to scrap data.
"""
# from database import player_csv_create
# player_csv_create.csv_write()

player_data = pd.read_csv("player-data.csv")

# Information-1
# Is player positions structure same across all teams?
print("Information-1")
print("How does playing positions of player look like across all teams? Is it same for all teams?")
playing_positions = player_data.groupby(["Team", "Position"]).size().unstack()
ax = playing_positions.plot(kind="bar", stacked = True, color=["red", "blue", "green", "yellow", "cyan"],
                            edgecolor="black")
ax.set_xlabel("Team")
ax.set_ylabel("Number of players")
ax.set_title("Player positions across all teams")
plt.show()
print("Conclusion for Question-1")
print("No. It looks like there is no common structure for positions. No two teams have same structure for team."
      "The reason could be each team have different star player in different position")

