import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import seaborn as sns

player_data = pd.read_csv("database/player_data.csv")


def research_question1(pd_data):
    print("Question - 1")
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


research_question1(player_data)
# research_question2(player_data)
