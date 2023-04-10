import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

"""Comment out following lines only if you want to create a new database
You will need to understand how web scrapping work if you want to customise data from website.
Please look at script.py file in scrapper directory if you want to change how to scrap data.
"""
# from database import player_csv_create
# player_csv_create.csv_write()

player_data = pd.read_csv("database/player-data.csv")


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


def research_question2(p_data: pd.DataFrame):
    print("Question - 2")
    print("""As we know most of the time each person has one dominant hand. Very few people are ambidextrous. So, 
    I would like to check weather this is also true in case of cricket.I would like to check if there is significant 
    evidence that person use same hand from left and right for batting and bowling in cricket? """)
    print()
    print("Answer - 2")
    print("""One can check this with help of chi-squared test. One can use a chi-squared test to determine whether 
    there is a significant association between two categorical variables. This test will help us understand the 
    strength of the association between batting and bowling hand and whether it is statistically significant. 
    """)

    data = p_data.copy()
    data = data[data['Bowling-Hand'] != 'None']

    # Create a contingency table
    contingency_table = pd.crosstab(data["Batting-Hand"], data["Bowling-Hand"])

    # Perform the chi-squared test
    chi2, p_value, degree_of_freedom, expected_frequencies = chi2_contingency(contingency_table)

    # Print the results
    print("Chi-squared statistic = {:.2f}".format(chi2))
    print("P-value = {:.4f}".format(p_value))
    print("Degrees of freedom = {}".format(degree_of_freedom))
    print("Expected frequencies =\n{}".format(expected_frequencies))

    print("""
Final Observation - 
  > The chi-squared statistic is a measure of how much the observed frequencies deviate from the expected 
    frequencies under the null hypothesis of independence. In this case, the chi-squared statistic is quite large, 
    indicating that there is a significant difference between the observed and expected frequencies, and therefore there
    may be a relationship between the batting-hand and bowling-hand being tested.
  > The p-value is a measure of the strength of evidence against the null hypothesis. A p-value of 0.0000 indicates 
    extremely strong evidence against the null hypothesis, meaning that the relationship between the two variables is 
    likely not due to chance.
  > In summary, the results suggest that there is a significant relationship between the batting-hand and bowling-hand 
    being tested, and the relationship is not due to chance. Our observation in question was correct that dominant hand
    also effects cricketers.""")


# research_question1(player_data)
# research_question2(player_data)
