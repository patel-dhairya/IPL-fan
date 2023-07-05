import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import seaborn as sns
import sqlite3

player_data = pd.read_csv("database/player_data.csv")

conn = sqlite3.connect('database/ipl.db')
matches_datafile = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()


def research_question1(pd_data):
    print("Analysis - 1")
    print("Are player positions structured the same across all teams? What I would like to know is whether all teams"
          "have a similar ratio for different roles, such as batsmen, bowlers, wicketkeepers, and so on.")
    print("Answer - 1")
    print("First, let's examine a frequency table of player roles within teams.")

    frequency_table = pd_data.pivot_table(values='Name', index=['Team'], columns=['Role'], aggfunc=len,
                                          fill_value=0, margins=True)

    print("Frequency Table")
    print(frequency_table)
    print("From the frequency table, it is evident that teams do not follow the same ratio for their player roles."
          )

    print("Now, let's take a look at a stacked bar chart to gain a better understanding.")
    playing_positions = player_data.groupby(["Team", "Role"]).size().unstack()

    # Choose color palette for chart
    num_categories = len(playing_positions.columns)
    colors = sns.color_palette('Set3', num_categories)

    ax = playing_positions.plot(kind="bar", stacked=True, color=colors, edgecolor="black")
    ax.set_xlabel("Team")
    ax.set_ylabel("Number of players")
    ax.set_title("Player positions across all teams")
    plt.show()
    print("Conclusion for Question-1")
    print("It appears that there is no common structure for player positions among teams. Each team seems to have a "
          "unique arrangement based on their individual circumstances. One possible reason for this variation could "
          "be the presence of star players in different positions. For example, if a team has two exceptional "
          "bowlers, they may be less inclined to include additional backup bowlers in their team."
          "In addition to the influence of star players, it's worth noting that coaches sometimes exhibit a "
          "preference for certain player positions as well. They may have a strategic or tactical inclination towards "
          "emphasizing specific roles within the team composition. This further contributes to the diversity and "
          "variation in player positions across different teams.")


def research_question2(pd_data: pd.DataFrame):
    print("Analysis - 2")
    print("Powerplay. A important part of modern fast paced cricket. So, what is powerplay exactly? Well, based on "
          "wikipedia entry: In a powerplay, restrictions are applied on the fielding team, with only two fielders "
          "allowed outside the 30-yard circle for a set number of overs. In 20 overs match, first six overs are "
          "powerplay overs. It is good opportunity for batters to set tone for the inning. My question is "
          "does teams who utilises powerplay more efficiently wins the match? I would like to know correlation "
          "between a team's performance in the power play and their overall match outcomes")
    print("Answer - 2")

    print(pd_data.head(5))

    # First convert powerplay score to runs only. Powerplay scores are currently in format of runs/wickets
    inning1_pp_score = pd_data["Powerplay score(i1)"].split("/")[0].astype(int)
    inning2_pp_score = pd_data["Powerplay score(i2)"].split("/")[0].astype(int)
    run_difference = (inning1_pp_score - inning2_pp_score).tolist()

    # Now let's get the winning team data series
    winning_team = pd_data["Winner"]

    # Now let's create a new data-series which will store weather team that was in lead during powerplay won the match
    # or not
    inning1_teams = []
    inning2_teams = []
    for index, row in pd_data.iterrows():
        home_team, away_team = row["Home Team"], row["Away Team"]
        toss_winner, toss_decision = row["Toss Win"], row["Field First"]
        if toss_decision == 1:
            inning2_teams.append(toss_winner)
            if toss_winner == home_team:
                inning1_teams.append(away_team)
            else:
                inning1_teams.append(home_team)
        else:
            inning1_teams.append(toss_winner)
            if toss_winner == home_team:
                inning2_teams.append(away_team)
            else:
                inning2_teams.append(home_team)

    # Now create a new list which provide team that was ahead in powerplay
    powerplay_lead = []
    for index, run_diff in enumerate(run_difference):
        if run_diff >= 0:
            powerplay_lead.append(inning1_teams[index])
        else:
            powerplay_lead.append(inning2_teams[index])
    print(powerplay_lead)


    # def research_question2(p_data: pd.DataFrame):
#     print("Question - 2")
#     print("""As we know most of the time each person has one dominant hand. Very few people are ambidextrous. So,
#     I would like to check weather this is also true in case of cricket.I would like to check if there is significant
#     evidence that person use same hand from left and right for batting and bowling in cricket? """)
#     print()
#     print("Answer - 2")
#     print("""One can check this with help of chi-squared test. One can use a chi-squared test to determine whether
#     there is a significant association between two categorical variables. This test will help us understand the
#     strength of the association between batting and bowling hand and whether it is statistically significant.
#     """)
#
#     data = p_data.copy()
#     data = data[data['Bowling-Hand'] != 'None']
#
#     # Create a contingency table
#     contingency_table = pd.crosstab(data["Batting-Hand"], data["Bowling-Hand"])
#
#     # Perform the chi-squared test
#     chi2, p_value, degree_of_freedom, expected_frequencies = chi2_contingency(contingency_table)
#
#     # Print the results
#     print("Chi-squared statistic = {:.2f}".format(chi2))
#     print("P-value = {:.4f}".format(p_value))
#     print("Degrees of freedom = {}".format(degree_of_freedom))
#     print("Expected frequencies =\n{}".format(expected_frequencies))
#
#     print("""
# Final Observation -
#   > The chi-squared statistic is a measure of how much the observed frequencies deviate from the expected
#     frequencies under the null hypothesis of independence. In this case, the chi-squared statistic is quite large,
#     indicating that there is a significant difference between the observed and expected frequencies, and therefore there
#     may be a relationship between the batting-hand and bowling-hand being tested.
#   > The p-value is a measure of the strength of evidence against the null hypothesis. A p-value of 0.0000 indicates
#     extremely strong evidence against the null hypothesis, meaning that the relationship between the two variables is
#     likely not due to chance.
#   > In summary, the results suggest that there is a significant relationship between the batting-hand and bowling-hand
#     being tested, and the relationship is not due to chance. Our observation in question was correct that dominant hand
#     also effects cricketers.""")


# research_question1(player_data)
research_question2(matches_datafile)
