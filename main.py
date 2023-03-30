import pandas as pd
import matplotlib.pyplot as plt

"""Comment out following lines only if you want to create a new database
You will need to understand how web scrapping work if you want to customise data from website.
Please look at script.py file in scrapper directory if you want to change how to scrap data.
"""
# from database import player_csv_create
# player_csv_create.csv_write()

player_data = pd.read_csv("player-data.csv")


def research_question1(pd_data):
    print("Question - 1")
    print("""Is player positions structure same across all teams? What I like to know is if all teams favour same ratio 
    for different roles such as batsman, bowler, wicketkeeper and so on.""")
    print("Answer - 1")
    print("First, let us look at frequency table of player roles and team")

    frequency_table = pd_data.pivot_table(values='Name', index=['Team'], columns=['Position'], aggfunc=len,
                                          fill_value=0, margins=True)

    print("Frequency Table")
    print(frequency_table)

    print("From the frequency table, we can clearly see that not all teams are following same ratio between their roles"
          )

    print("Now, let us look at stacked bar chart for better understanding")
    playing_positions = player_data.groupby(["Team", "Position"]).size().unstack()
    ax = playing_positions.plot(kind="bar", stacked=True, color=["red", "blue", "green", "yellow", "cyan"],
                                edgecolor="black")
    ax.set_xlabel("Team")
    ax.set_ylabel("Number of players")
    ax.set_title("Player positions across all teams")
    plt.show()
    print("Conclusion for Question-1")
    print("No. It looks like there is no common structure for positions. No two teams have same structure for team."
          "The reason could be each team have different star player in different position, if one team has 2 star "
          "bowlers, they are less likely to add more back up bowlers to their team")


# research_question1(player_data)
