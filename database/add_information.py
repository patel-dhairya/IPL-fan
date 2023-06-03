from database_table_add import add_match, add_player_bat_data, add_player_bowl_data, add_player_field_data
from scrapper.player_match_performance_scrap import get_bowling_performance, get_batting_performance
import asyncio
import aiohttp


# Match-1
# def match1() -> str:
#     """
#     Match-1 was played between CSK and GT in home ground of GT, Narendra Modi stadium. It was opening match of IPL 2023.
#     GT won this match in thrilling way.
#     """
#     # Add match
#     add_match(1, "GT", "CSK", "Narendra Modi Stadium", "GT", True, "GT", "Rashid Khan", True, "178/7", "182/5",
#               "51/2", "65/1", 92, "Ruturaj Gaikwad", "Rashid Khan", "26/2", 63, "Shubman Gill", "Rajvardhan Hangargekar"
#               , "36/3")
#
#     # Add player performance
#     # Inning-1 => CSK BAT and GT Field
#     # CSK BAT
#     add_player_bat_data("Devon Conway", 1, "GT", 1, 6, 0, 0, False, "bowled", "Mohammed Shami", "None", False)
#     add_player_bat_data("Ruturaj Gaikwad", 1, " GT", 92, 50, 4, 9, False, "catch", "Alzarri Joseph", "Shubman Gill",
#                         False)
#     add_player_bat_data("Moeen Ali", 1, "GT", 23, 17, 4, 1, False, "catch", "Rashid Khan", "Wriddhiman Saha", False)
#     add_player_bat_data("Ben Stokes", 1, "GT", 7, 6, 1, 0, False, "catch", "Rashid Khan", "Wriddhiman Saha", False)
#     add_player_bat_data("Ambati Rayudu", 1, "GT", 12, 12, 0, 1, False, "bowled", "Joshua Little", "None", False)
#     add_player_bat_data("Shivam Dube", 1, "GT", 19, 18, 0, 1, False, "catch", "Mohammed Shami", "Rashid Khan", False)
#     add_player_bat_data("Ravindra Jadeja", 1, "GT", 1, 2, 0, 0, False, "catch", "Alzarri Joseph", "Vijay Shankar", False
#                         )
#     add_player_bat_data("MS Dhoni", 1, "GT", 14, 7, 1, 1, True, "None", "None", "None", motm=False)
#     add_player_bat_data("Mitchell Santner", 1, "GT", 1, 3, 0, 0, True, "None", "None", "None", motm=False)
#
#     # GT Field
#     add_player_bowl_data("Mohammed Shami", 1, "CSK", 24, 29, 2, 0, 13, 2, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, False)
#     add_player_bowl_data("Hardik Pandya", 1, "CSK", 18, 28, 0, 0, 6, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, False)
#     add_player_bowl_data("Joshua Little", 1, "CSK", 24, 41, 1, 0, 10, 4, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, False)
#     add_player_bowl_data("Rashid Khan", 1, "CSK", 24, 26, 2, 0, 10, 2, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0, True)
#     add_player_bowl_data("Alzarri Joseph", 1, "CSK", 24, 33, 2, 0, 8, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, False)
#     add_player_bowl_data("Yash Dayal", 1, "CSK", 6, 14, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, False)
#     add_player_bowl_data("Shubman Gill", 1, "CSK", field_catch=1)
#     add_player_bowl_data("Wriddhiman Saha", 1, "CSK", field_catch=2)
#     add_player_bowl_data("Vijay Shankar", 1, "CSK", field_catch=1)
#
#     # Inning-1 => GT BAT and CSK Field
#     # GT BAT
#     add_player_bat_data("Wriddhiman Saha", 1, "CSK", 25, 16, 2, 2, False, "catch", "Rajvardhan Hangargekar",
#                         "Shivam Dube", False)
#     add_player_bat_data("Shubman Gill", 1, "CSK", 63, 36, 6, 3, False, "catch", "Tushar Deshpande", "Ruturaj Gaikwad",
#                         False)
#     add_player_bat_data("Sai Sudharsan", 1, "CSK", 22, 17, 3, 0, False, "catch", "Rajvardhan Hangargekar", "MS Dhoni",
#                         False)
#     add_player_bat_data("Hardik Pandya", 1, "CSK", 8, 11, 0, 0, False, "bowled", "Ravindra Jadeja", "None", False)
#     add_player_bat_data("Vijay Shankar", 1, "CSK", 27, 21, 2, 1, False, "catch", "Rajvardhan Hangargekar",
#                         "Mitchell Santner")
#     add_player_bat_data("Rahul Tewatia", 1, "CSK", 15, 14, 1, 1, True, "None")
#     add_player_bat_data("Rashid Khan", 1, "CSK", 10, 3, 1, 1, True, "None", motm=True)
#
#     # CSK Field
#     add_player_bowl_data("Deepak Chahar", 1, "GT", 24, 29, 0, 0, 9, 1, 2)
#     add_player_bowl_data("Tushar Deshpande", 1, "GT", 20, 51, 1, 0, 5, 4, 1, 1, 1, 1)
#     add_player_bowl_data("Rajvardhan Hangargekar", 1, "GT", 24, 36, 3, 0, 10, 4, 1, 3, 1, 3)
#     add_player_bowl_data("Mitchell Santner", 1, "GT", 24, 32, 0, 0, 7, 5, field_catch=1)
#     add_player_bowl_data("Ravindra Jadeja", 1, "GT", 24, 28, 1, 0, 9, 1, 1, 0, 0, 0, 1)
#     add_player_bowl_data("Shivam Dube", 1, "GT", field_catch=1)
#     add_player_bowl_data("Ruturaj Gaikwad", 1, "GT", field_catch=1)
#     add_player_bowl_data("MS Dhoni", 1, "GT", field_catch=1)
#
#     return "Data added successfully for match-1"


async def match_data(match_id: int, home_team: str, away_team: str, stadium: str, toss_winner: str, toss_decision: str,
                     night_match: bool, match_winner: str, man_of_the_match: str, batting_url: str, bowling_url: str,
                     i1: str, i2: str) -> str:
    """

    :param match_id:
    :param home_team:
    :param away_team:
    :param stadium:
    :param toss_winner:
    :param toss_decision:
    :param night_match:
    :param match_winner:
    :param man_of_the_match:
    :param batting_url:
    :param bowling_url:
    :param i1:
    :param i2:
    :return:
    """

    def dismissal_information(dismissal_reason) -> str | list | None:
        """
        Parses the dismissal reason and returns relevant information about the dismissal.

        Args:
            dismissal_reason (str): The dismissal reason provided as a string.

        Returns: str | list | None: Information about the dismissal. Returns a string if the player is not out or
        retired out. Returns a list with the dismissal type and relevant player names otherwise. The structure of the
        list depends on the dismissal type.

        """

        if dismissal_reason == "not out":
            return "not out"

        if dismissal_reason == "retired out":
            return "retired out"

        # Check if player was caught out
        if dismissal_reason[0] == "c":
            # Extracting the player names
            fielder, bowler = dismissal_reason[2:].split(' b')
            return ["catch", fielder.strip(), bowler.strip()]

        # Check if player was stump out
        elif dismissal_reason[:2] == "st":
            wicket_keeper, bowler = dismissal_reason[3:].split(' b')
            return ["stump-out", wicket_keeper.strip(), bowler.strip()]

        # Check if player was out by lbw
        elif dismissal_reason[:3] == "lbw":
            bowler = dismissal_reason.split(' b')[1].strip()
            return ["lbw", bowler.strip()]

        # Check if player was run out
        elif "run out" in dismissal_reason:
            # Run out is in the format of "run out (Tim David / Ishan Kishan)" This function only focuses on the
            # primary contributor to the run out if there is more than one fielder involved
            fielders = dismissal_reason[dismissal_reason.index('(') + 1: dismissal_reason.index(')')].split('/')
            return ["run out", fielders[-1].strip()]

        # Default case if dismissal reason does not match any known patterns
        return None

    teams = [home_team, away_team]

    async with aiohttp.ClientSession() as session:
        bowling_task = asyncio.create_task(get_bowling_performance(bowling_url, teams, session))
        batting_task = asyncio.create_task(get_batting_performance(batting_url, i1, i2, teams, session))
        await asyncio.gather(bowling_task, batting_task)

        bowling_performances = await bowling_task
        batting_performances = await batting_task

    highest_score_inning1 = ("name", 0)
    highest_score_inning2 = ("name", 0)
    fielding_wickets = {}
    for batting_performance in batting_performances:
        name = batting_performance
        runs, balls, fours, sixes, dismissal, playing_team, opponent_team = batting_performances[name]

        # find the high scorer player for both teams
        if home_team == playing_team:
            if not highest_score_inning1[1] > runs:
                highest_score_inning1 = (name, runs)
        elif away_team == playing_team:
            if not highest_score_inning2[1] > runs:
                highest_score_inning2 = (name, runs)

        add_player_bat_data(name, match_id, opponent_team, runs, balls, fours, sixes,
                            True if dismissal is "not out" else False,
                            motm=True if man_of_the_match is name else False)

    print(bowling_performances)
    print(batting_performances)
    return "Done"


# temp_i1 = 'tbody_2955'
# temp_i2 = 'tbody_1111'
# asyncio.run(match_data(73, "GT", "MI", "Narendra Modi Stadium", "MI", "field", True, "GT", "Shubman Gill",
#                        "https://sports.ndtv.com/cricket/gt-vs-mi-scorecard-live-cricket-score-ipl-2023-qualifier-2"
#                        "-ahmmi05262023225989",
#                        "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
#                        "-mumbai-indians-qualifier-2-1370352/full-scorecard",
#                        temp_i1, temp_i2))

# def semifinal3() -> str:
#     """
#     Semifinal 3 match was played between MI and GT. MI won 2nd semi-final match against LSG whereas GT lost 1st
#     semi-final against CSK. Winner would face CSK in ipl 2023 final
#     :return: str : Confirmation that match data successfully added to tables
#     """
#     man_of_the_match = "Shubman Gill"
#     add_match(73, "GT", "MI", "Narendra Modi Stadium", "MI", True, "GT", man_of_the_match, True, "233/3", "171", "50/0"
#               , "72/3", 129, man_of_the_match, "Jason Behrendorff", "28/0", 61, "Suryakumar Yadav", "Mohit Sharma",
#               "10/5")
#
#     bowling_performances = get_bowling_performance("https://www.espncricinfo.com/series/indian-premier-league-2023"
#                                                    "-1345038/gujarat-titans-vs-mumbai-indians-qualifier-2-1370352"
#                                                    "/full-scorecard")
#     batting_performances = get_batting_performance("https://sports.ndtv.com/cricket/gt-vs-mi-scorecard-live-cricket"
#                                                    "-score-ipl-2023-qualifier-2-ahmmi05262023225989", 'tbody_2955',
#                                                    'tbody_1111')
#     # Add data for bowling performance
#     for bowler in bowling_performances:
#         bowler_name = bowler
#         bowler_performance = bowling_performances[bowler]
#         bowler_team = find_team(bowler_name)
#         add_player_bowl_data(bowler_name, 73, )
#
#     print(bowling_performances)
#     print(batting_performances)
#     return "Done"


# semifinal3()

# Already added
# print(match1())
# test_url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-kolkata-knight" \
#            "-riders-2nd-match-1359476/full-scorecard"
# bat, bowl = get_info(test_url)
# print(bat)
# print(bowl)
