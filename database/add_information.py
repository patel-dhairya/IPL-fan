from collections import defaultdict

import database.database_table_create
from database.double_names import change_name
from database_table_add import add_match, add_player_bat_data, add_player_bowl_data, add_player_field_data
from scrapper.player_match_performance_scrap import get_bowling_performance, get_batting_performance
import asyncio
import aiohttp


async def match_data(match_id: int, home_team: str, away_team: str, stadium: str, toss_winner: str, toss_decision: str,
                     night_match: bool, match_winner: str, score_inning1: str, score_powerplay_inning1: str,
                     score_inning2: str, score_powerplay_inning2: str, man_of_the_match: str, batting_url: str,
                     bowling_url: str, scoreboard1_tag: str, scoreboard2_tag: str) -> str:
    """
    :param match_id: Unique match id representing each match starting from 1
    :param home_team: Home team in the match
    :param away_team: Away team in the match
    :param stadium: Name of stadium where match took place
    :param toss_winner: Name of team that won toss
    :param toss_decision: bat if winner of toss decided to bat first else field
    :param night_match: False if match was played in afternoon else True
    :param match_winner: Name of team that won match
    :param score_inning1: Runs scored by team batting first in format of runs/wickets.
    :param score_powerplay_inning1: Score of team batting first in first six overs
    :param score_inning2: Runs scored by team batting second in format of runs/wickets
    :param score_powerplay_inning2: Score of team batting second in first six overs
    :param man_of_the_match: Name of player that won man of the match award
    :param batting_url: URL representing webpage of NDTV sports with scoreboard of this match
    :param bowling_url: URL representing webpage of espn cricinfo with scoreboard of this match
    :param scoreboard1_tag: HTML attribute class name for scoreboard1 on ndtv website
    :param scoreboard2_tag: HTML attribute class name for scoreboard2 on ndtv website
    :return: String suggesting data for match added successfully
    """

    def dismissal_information(dismissal_reason) -> list | None:
        """
        Parses the dismissal reason and returns relevant information about the dismissal.

        Args:
            dismissal_reason (str): The dismissal reason provided as a string.

        Returns: list | None: Information about the dismissal. Returns a list with the dismissal type and relevant
        player names otherwise. The structure of the list depends on the dismissal type.

        """

        if dismissal_reason == "not out":
            return ["not out"]

        if dismissal_reason == "retired out":
            return ["retired out"]

        # Check if player was caught out
        if dismissal_reason[0] == "c":
            # Extracting the player names
            fielder, bowler = dismissal_reason[2:].split(' b')
            return ["catch", fielder.strip(), bowler.strip()]

        # Check if player was stump out
        elif dismissal_reason[:2] == "st":
            wicket_keeper, bowler = dismissal_reason[3:].split(' b')
            return ["stumped", wicket_keeper.strip(), bowler.strip()]

        # Check if player was out by lbw
        elif dismissal_reason[:3] == "lbw":
            bowler = dismissal_reason.split(' b')[1].strip()
            return ["lbw", bowler.strip()]

        # Check if player was bowled by bowler
        elif dismissal_reason[0] == "b":
            bowler = dismissal_reason.split("b ")[1]
            return ["bowled", bowler.strip()]

        # Check if player was run out
        elif "run-out" in dismissal_reason:
            # Run out is in the format of "run out (Tim David / Ishan Kishan)" This function only focuses on the
            # primary contributor to the run out if there is more than one fielder involved
            fielders = dismissal_reason[dismissal_reason.index('(') + 1: dismissal_reason.index(')')].split('/')
            return ["run-out", fielders[-1].strip()]

        # Default case if dismissal reason does not match any known patterns
        return None

    teams = [home_team, away_team]

    async with aiohttp.ClientSession() as session:
        bowling_task = asyncio.create_task(get_bowling_performance(bowling_url, teams, session))
        batting_task = asyncio.create_task(get_batting_performance(batting_url, scoreboard1_tag, scoreboard2_tag,
                                                                   teams, session))
        await asyncio.gather(bowling_task, batting_task)

        bowling_performances = await bowling_task
        batting_performances = await batting_task

    highest_score_home_team = ("name", 0)
    highest_score_away_team = ("name", 0)

    # Batting and Fielding Performance

    # Dictionaries to store information about all the fielders/wicket keeper who were part of either catch, stumping out
    # or run out
    # I used default dict so in future when I need this dictionary with int and if player do not exist then it can
    # return 0
    fielder_catch = defaultdict(int)
    fielder_run_out = defaultdict(int)
    wicketkeeper_stump_out = defaultdict(int)
    bowler_catch = defaultdict(int)
    bowler_stump_out = defaultdict(int)
    bowler_lbw = defaultdict(int)
    bowler_bowled = defaultdict(int)
    fielder_opponent_team = {}
    for batting_performance in batting_performances:
        name = change_name(batting_performance)
        runs, balls, fours, sixes, dismissal, playing_team, opponent_team = batting_performances[name]

        # check if player got duck out
        if runs == "":
            runs = 0
        runs, balls, fours, sixes = int(runs), int(balls), int(fours), int(sixes)
        dismissal_type = dismissal_information(dismissal)
        wicket_type, wicket_taken_bowler, wicket_taken_fielder = dismissal_type[0], "None", "None"
        if wicket_type == "catch":
            fielder_catch[dismissal_type[1]] += 1
            bowler_catch[dismissal_type[2]] += 1
            fielder_opponent_team[dismissal_type[1]] = playing_team
            wicket_taken_bowler, wicket_taken_fielder = dismissal_type[2], dismissal_type[1]
        elif dismissal_type[0] == "stumped":
            wicketkeeper_stump_out[dismissal_type[1]] += 1
            bowler_stump_out[dismissal_type[2]] += 1
            fielder_opponent_team[dismissal_type[1]] = playing_team
            wicket_taken_bowler, wicket_taken_fielder = dismissal_type[2], dismissal_type[1]
        elif dismissal_type[0] == "run-out":
            fielder_run_out[dismissal_type[1]] += 1
            fielder_opponent_team[dismissal_type[1]] = playing_team
            wicket_taken_fielder = dismissal_type[1]
        # player was lbw
        elif dismissal_type[0] == "lbw":
            bowler_lbw[dismissal_type[1]] += 1
            wicket_taken_bowler = dismissal_type[1]
        elif dismissal_type[0] == "bowled":
            bowler_bowled[dismissal_type[1]] += 1
            wicket_taken_bowler = dismissal_type[1]
        else:
            pass
        wicket_taken_bowler = change_name(wicket_taken_bowler)
        wicket_taken_fielder = change_name(wicket_taken_fielder)

        # find the high scorer player for both teams
        if home_team == playing_team:
            if not int(highest_score_home_team[1]) > runs:
                highest_score_home_team = (name, runs)
        elif away_team == playing_team:
            if not int(highest_score_away_team[1]) > runs:
                highest_score_away_team = (name, runs)

        add_player_bat_data(name, match_id, opponent_team, runs, balls, fours, sixes,
                            True if dismissal == "not out" else False,
                            wicket_type, wicket_taken_bowler, wicket_taken_fielder,
                            motm=True if man_of_the_match == name else False)

    # Add fielding data for run out, catch and stump out
    fielding_combination = {fielder: (fielder_catch.get(fielder, 0), wicketkeeper_stump_out.get(fielder, 0),
                                      fielder_run_out.get(fielder, 0)) for fielder in set(fielder_catch) |
                            set(wicketkeeper_stump_out) | set(fielder_run_out)}

    for fielder in fielding_combination:
        name = change_name(fielder)
        catches, stump_outs, run_outs = fielding_combination[fielder][0], fielding_combination[fielder][1], \
            fielding_combination[fielder][2]
        add_player_field_data(name, match_id, fielder_opponent_team[name], catches, run_outs, stump_outs)

    # Add bowling data

    # Here index 0 represents name of player, index 1 represents runs given away by player which is set default to 150
    # as it is nearly impossible to give away 150 runs in 4 overs and index 2 represents wickets taken by player
    highest_wicket_home_team = ("name", 150, 0)
    highest_wicket_away_team = ("name", 150, 0)

    for bowling_performance in bowling_performances:
        name = change_name(bowling_performance)
        player_overs, maiden, runs, wickets, economy, dot, boundary, six, wide, no_balls, player_team, opponent = \
            bowling_performances[bowling_performance]
        maiden, runs, wickets, dot, boundary, six, wide, no_balls = int(maiden), int(runs), int(wickets), int(dot), \
            int(boundary), int(six), int(wide), int(no_balls)
        if player_team == home_team:
            if int(highest_wicket_home_team[2]) < wickets:
                highest_wicket_home_team = (name, runs, wickets)
            elif highest_wicket_home_team[2] == wickets:
                if int(highest_wicket_home_team[1]) > runs:
                    highest_wicket_home_team = (name, runs, wickets)

        elif player_team == away_team:
            if int(highest_wicket_away_team[2]) < wickets:
                highest_wicket_away_team = (name, runs, wickets)
            elif int(highest_wicket_away_team[2]) == wickets:
                if int(highest_wicket_away_team[1]) > runs:
                    highest_wicket_away_team = (name, runs, wickets)

        add_player_bowl_data(name, match_id, opponent,
                             (lambda total_overs: int(float(total_overs)) * 6 + int(
                                 (float(total_overs) - int(float(total_overs))) * 10) * 6 // 10)(player_overs),
                             runs, wickets, maiden, dot, boundary, six, wide, no_balls, bowler_catch[name],
                             bowler_bowled[name], bowler_stump_out[name], bowler_lbw[name],
                             motm=True if man_of_the_match == name else False
                             )

    # Add information to match table
    if toss_decision == "bat":
        inning1_batting_team = toss_winner
    else:
        def other_elements(ls: list, given_element: str) -> str:
            """
            Returns the other element from a list of two elements. Assume that ls always has two elements
            :param ls: given list
            :param given_element: chosen element
            :return: returns element other than chosen elements from given list.
            """
            return ls[1] if given_element == ls[0] else ls[0]

        inning1_batting_team = other_elements(teams, toss_winner)

    inning1_highest_scorer, inning1_highest_score = highest_score_home_team if inning1_batting_team == home_team \
        else highest_score_away_team
    inning2_highest_scorer, inning2_highest_score = highest_score_home_team if inning1_batting_team == away_team \
        else highest_score_away_team
    inning1_best_bowler = highest_wicket_home_team[0] if inning1_batting_team == away_team else \
        highest_wicket_away_team[0]
    inning1_best_bowling = '/'.join(str(x) for x in highest_wicket_home_team[1:3]) if inning1_batting_team == away_team \
        else '/'.join(str(x) for x in highest_wicket_away_team[1:3])

    inning2_best_bowler = highest_wicket_home_team[0] if inning1_batting_team == home_team else \
        highest_wicket_away_team[0]
    inning2_best_bowling = '/'.join(str(x) for x in highest_wicket_home_team[1:3]) if inning1_batting_team == home_team \
        else '/'.join(str(x) for x in highest_wicket_away_team[1:3])

    add_match(match_id, home_team, away_team, stadium, toss_winner, True if toss_decision == "field" else False,
              match_winner, man_of_the_match, night_match, score_inning1, score_inning2, score_powerplay_inning1,
              score_powerplay_inning2, inning1_highest_score, inning1_highest_scorer, inning1_best_bowler,
              inning1_best_bowling, inning2_highest_score, inning2_highest_scorer, inning2_best_bowler,
              inning2_best_bowling)

    return f"Data successfully added for match id - {match_id} between {home_team} and {away_team}."


def match1():
    asyncio.run(match_data(1, "GT", "CSK", "Narendra Modi Stadium", "GT", "field", True, "GT", "182/5", "65/1",
                           "178/7", "51/2", "Rashid Khan", "https://sports.ndtv.com/cricket/gt-vs-csk-scorecard-live"
                                                           "-cricket-score-ipl-2023-match-1-ahmck03312023219154",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-chennai-super-kings-1st-match-1359475/full-scorecard", "tbody_1108", "tbody_2955"))


def match2():
    asyncio.run(match_data(2, "PBKS", "KKR", "Punjab Cricket Association IS Bindra Stadium", "KKR", "field", False,
                           "PBKS", "191/5", "56/1", "146/7", "46/3", "Arshdeep Singh",
                           "https://sports.ndtv.com/cricket/pbks-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-2"
                           "-kpkr04012023219155",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs"
                           "-kolkata-knight-riders-2nd-match-1359476/full-scorecard", "tbody_1107", "tbody_1106"))


def match3():
    asyncio.run(match_data(3, "LSG", "DC", "Atal Bihari Vajpayee Ekana Cricket Stadium", "DC", "field", True, "LSG",
                           "193/6", "30/1", "143/9", "47/2", "Mark Wood",
                           "https://sports.ndtv.com/cricket/lsg-vs-dc-scorecard-live-cricket-score-ipl-2023-match-3"
                           "-lkodd04012023219156",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super"
                           "-giants-vs-delhi-capitals-3rd-match-1359477/full-scorecard",
                           "tbody_2954", "tbody_1109"))


def match4():
    asyncio.run(match_data(4, "SRH", "RR", "Rajiv Gandhi International Stadium", "SRH", "field", False, "RR", "203/5",
                           "85/1", "131/8", "30/2", "Jos Buttler",
                           "https://sports.ndtv.com/cricket/srh-vs-rr-scorecard-live-cricket-score-ipl-2023-match-4"
                           "-shrr04022023219157",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers"
                           "-hyderabad-vs-rajasthan-royals-4th-match-1359478/full-scorecard",
                           "tbody_1110", "tbody_1379"
                           ))

def match5():
    asyncio.run(match_data(5, "RCB", "MI", "MA Chidambaram Stadium", "RCB", "field", True, "RCB", "171/7", "29/3",
                           "172/2", "53/0", "Faf du Plessis",
                           "https://sports.ndtv.com/cricket/rcb-vs-mi-scorecard-live-cricket-score-ipl-2023-match-5"
                           "-bcmi04022023219158",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers"
                           "-bangalore-vs-mumbai-indians-5th-match-1359479/full-scorecard",
                           "tbody_1111", "tbody_1105"))


# database.database_table_create.create_database()
# match1()
# match2()
# match3()
# match4()
# match5()

def match73():
    asyncio.run(match_data(73, "GT", "MI", "Narendra Modi Stadium", "MI", "field", True, "GT", "233/3", "50/0", "171/10",
                           "72/3", "Shubman Gill",
                           "https://sports.ndtv.com/cricket/gt-vs-mi-scorecard-live-cricket-score-ipl-2023-qualifier-2"
                           "-ahmmi05262023225989",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-mumbai-indians-qualifier-2-1370352/full-scorecard",
                           'tbody_2955', 'tbody_1111'))

# match73()
