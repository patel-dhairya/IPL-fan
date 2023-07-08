import aiohttp
import asyncio
from collections import defaultdict


from database.double_names import change_name
from database_table_add import add_match, add_player_bat_data, add_player_bowl_data, add_player_field_data
from scrapper.player_match_performance_scrap import get_bowling_performance, get_batting_performance


# Scoreboard tbody tag name on ndtv website
SCOREBOARD_TAGS = {"CSK": "tbody_1108", "DC": "tbody_1109", "GT": "tbody_2955", "KKR": "tbody_1106",
                   "LSG": "tbody_2954",
                   "MI": "tbody_1111", "PBKS": "tbody_1107", "RCB": "tbody_1105", "RR": "tbody_1110",
                   "SRH": "tbody_1379"}


async def match_data(match_id: int, home_team: str, away_team: str, stadium: str, toss_winner: str, toss_decision: str,
                     night_match: bool, match_winner: str, score_inning1: str, score_powerplay_inning1: str,
                     score_inning2: str, score_powerplay_inning2: str, man_of_the_match: str, batting_url: str,
                     bowling_url: str) -> str:
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

        if "retired" in dismissal_reason:
            return ["retired out"]

        # Check if player was caught out
        if dismissal_reason[0] == "c":
            # Check if player got caught by the bowler
            if dismissal_reason.split(" ")[1] == "&":
                _, bowler = dismissal_reason.split(' b')
                return ["catch", bowler.strip(), bowler.strip()]
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
        elif "run out" in dismissal_reason:
            # Run out is in the format of "run out (Tim David / Ishan Kishan)" This function only focuses on the
            # primary contributor to the run out if there is more than one fielder involved
            fielders = dismissal_reason[dismissal_reason.index('(') + 1: dismissal_reason.index(')')].split('/')
            return ["run-out", fielders[-1].strip()]

        # Check if player got out because of hit wicket
        elif "hit wicket" in dismissal_reason:
            bowler = dismissal_reason.split("b ")[1]
            return ["hit-wicket", bowler.strip()]

        # Default case if dismissal reason does not match any known patterns
        return None

    teams = [home_team, away_team]

    scoreboard_selection = teams[:]
    scoreboard_selection.remove(toss_winner)

    # Determine scoreboard tags based on toss decision
    if toss_decision == "field":
        # If the toss winner chose to field, assign the scoreboard tags accordingly
        scoreboard1_tag, scoreboard2_tag = SCOREBOARD_TAGS[scoreboard_selection[0]], SCOREBOARD_TAGS[toss_winner]
    else:
        # If the toss winner chose to bat, assign the scoreboard tags accordingly
        scoreboard1_tag, scoreboard2_tag = SCOREBOARD_TAGS[toss_winner], SCOREBOARD_TAGS[scoreboard_selection[0]]

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
        # For easier analysis, hit wicket is also considered bowled in this database
        elif dismissal_type[0] == "bowled" or dismissal_type[0] == "hit-wicket":
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
        catches, stump_outs, run_outs = fielding_combination[fielder][0], fielding_combination[fielder][1], \
            fielding_combination[fielder][2]
        add_player_field_data(change_name(fielder), match_id, fielder_opponent_team[fielder], catches, run_outs,
                              stump_outs)

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

        add_player_bowl_data(
            name, match_id, opponent,
            (lambda t_overs: int(float(t_overs)) * 6 + round(10 * (float(t_overs) - int(float(t_overs)))))(
                player_overs),
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
            if not len(ls) == 2:
                raise ValueError
            return ls[1] if given_element == ls[0] else ls[0]

        inning1_batting_team = other_elements(teams, toss_winner)

    inning1_highest_scorer, inning1_highest_score = highest_score_home_team if inning1_batting_team == home_team \
        else highest_score_away_team
    inning2_highest_scorer, inning2_highest_score = highest_score_home_team if inning1_batting_team == away_team \
        else highest_score_away_team
    inning1_best_bowler = highest_wicket_home_team[0] if inning1_batting_team == away_team else \
        highest_wicket_away_team[0]
    inning1_best_bowling = '/'.join(str(x) for x in highest_wicket_home_team[1:3]) if inning1_batting_team == away_team\
        else '/'.join(str(x) for x in highest_wicket_away_team[1:3])

    inning2_best_bowler = highest_wicket_home_team[0] if inning1_batting_team == home_team else \
        highest_wicket_away_team[0]
    inning2_best_bowling = '/'.join(str(x) for x in highest_wicket_home_team[1:3]) if inning1_batting_team == home_team\
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
                           "-chennai-super-kings-1st-match-1359475/full-scorecard"))


def match2():
    asyncio.run(match_data(2, "PBKS", "KKR", "Punjab Cricket Association IS Bindra Stadium", "KKR", "field", False,
                           "PBKS", "191/5", "56/1", "146/7", "46/3", "Arshdeep Singh",
                           "https://sports.ndtv.com/cricket/pbks-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-2"
                           "-kpkr04012023219155",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs"
                           "-kolkata-knight-riders-2nd-match-1359476/full-scorecard"))


def match3():
    asyncio.run(match_data(3, "LSG", "DC", "Atal Bihari Vajpayee Ekana Cricket Stadium", "DC", "field", True, "LSG",
                           "193/6", "30/1", "143/9", "47/2", "Mark Wood",
                           "https://sports.ndtv.com/cricket/lsg-vs-dc-scorecard-live-cricket-score-ipl-2023-match-3"
                           "-lkodd04012023219156",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super"
                           "-giants-vs-delhi-capitals-3rd-match-1359477/full-scorecard", ))


def match4():
    asyncio.run(match_data(4, "SRH", "RR", "Rajiv Gandhi International Stadium", "SRH", "field", False, "RR", "203/5",
                           "85/1", "131/8", "30/2", "Jos Buttler",
                           "https://sports.ndtv.com/cricket/srh-vs-rr-scorecard-live-cricket-score-ipl-2023-match-4"
                           "-shrr04022023219157",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers"
                           "-hyderabad-vs-rajasthan-royals-4th-match-1359478/full-scorecard"))


def match5():
    asyncio.run(match_data(5, "RCB", "MI", "M.Chinnaswamy Stadium", "RCB", "field", True, "RCB", "171/7", "29/3",
                           "172/2", "53/0", "Faf du Plessis",
                           "https://sports.ndtv.com/cricket/rcb-vs-mi-scorecard-live-cricket-score-ipl-2023-match-5"
                           "-bcmi04022023219158",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers"
                           "-bangalore-vs-mumbai-indians-5th-match-1359479/full-scorecard"))


def match6():
    asyncio.run(match_data(6, "CSK", "LSG", "MA Chidambaram Stadium", "LSG", "field", True, "CSK", "217/7", "79/0",
                           "205/7", "80/1", "Moeen Ali",
                           "https://sports.ndtv.com/cricket/csk-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-6"
                           "-cklko04032023222174",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super"
                           "-kings-vs-lucknow-super-giants-6th-match-1359480/full-scorecard"))


def match7():
    asyncio.run(match_data(7, "DC", "GT", "Arun Jaitley Stadium", "GT", "field", True, "GT", "162/8", "52/2", "163/4",
                           "54/3", "Sai Sudharsan",
                           "https://sports.ndtv.com/cricket/dc-vs-gt-scorecard-live-cricket-score-ipl-2023-match-7"
                           "-ddahm04042023222176",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs"
                           "-gujarat-titans-7th-match-1359481/full-scorecard"))


def match8():
    asyncio.run(match_data(8, "RR", "PBKS", "Barsapara Cricket Stadium", "RR", "field", True, "PBKS", "197/4",
                           "63/0", "192/7", "57/3", "Nathan Ellis",
                           "https://sports.ndtv.com/cricket/rr-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-8"
                           "-rrkp04052023222177",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-punjab-kings-8th-match-1359482/full-scorecard"))


def match9():
    asyncio.run(
        match_data(
            9, "KKR", "RCB", "Eden Gardens", "RCB", "field", True, "KKR", "204/7", "47/2", "123/10", "50/2",
            "Shardul Thakur",
            "https://sports.ndtv.com/cricket/kkr-vs-rcb-scorecard-live-cricket-score-ipl-2023-match-9"
            "-krbc04062023222178",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight-riders-vs-royal"
            "-challengers-bangalore-9th-match-1359483/full-scorecard"
        )
    )


def match10():
    asyncio.run(
        match_data(
            10, "SRH", "LSG", "Atal Bihari Vajpayee Ekana Cricket Stadium", "SRH", "bat", True, "LSG", "121/8", "43/1",
            "127/5", "45/2", "Krunal Pandya",
            "https://sports.ndtv.com/cricket/lsg-vs-srh-scorecard-live-cricket-score-ipl-2023-match-10"
            "-lkosh04072023222180",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-sunrisers"
            "-hyderabad-10th-match-1359484/full-scorecard"
        )
    )


def match11():
    asyncio.run(match_data(11, "RR", "DC", "Barsapara Cricket Stadium", "DC", "field", False, "RR", "199/4", "68/0",
                           "142/9", "38/3", "Yashasvi Jaiswal",
                           "https://sports.ndtv.com/cricket/rr-vs-dc-scorecard-live-cricket-score-ipl-2023-match-11"
                           "-rrdd04082023222182",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-delhi-capitals-11th-match-1359485/full-scorecard"))


def match12():
    asyncio.run(
        match_data(
            12, "MI", "CSK", "Wankhede Stadium", "CSK", "field", True, "CSK", "157/8", "61/1", "159/3", "68/1",
            "Ravindra Jadeja",
            "https://sports.ndtv.com/cricket/mi-vs-csk-scorecard-live-cricket-score-ipl-2023-match-12"
            "-mick04082023222183",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs-chennai-super"
            "-kings-12th-match-1359486/full-scorecard"
        )
    )


def match13():
    asyncio.run(
        match_data(
            13, "GT", "KKR", "Narendra Modi Stadium", "GT", "bat", False, "KKR", "204/4", "54/1", "207/7", "43/2",
            "Rinku Singh",
            "https://sports.ndtv.com/cricket/gt-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-13-ahmkr04092023222185",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
            "-kolkata-knight-riders-13th-match-1359487/full-scorecard"))


def match14():
    asyncio.run(
        match_data(
            14, "SRH", "PBKS", "Rajiv Gandhi International Stadium", "SRH", "field", True, "PBKS", "143/9", "41/3",
            "145/2", "34/1", "Shikhar Dhawan",
            "https://sports.ndtv.com/cricket/srh-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-14"
            "-shkp04092023222186",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-punjab"
            "-kings-14th-match-1359488/full-scorecard"
        )
    )


def match15():
    asyncio.run(
        match_data(
            15, "RCB", "LSG", "M.Chinnaswamy Stadium", "LSG", "field", True, "LSG", "212/2", "56/0", "213/9", "37/3",
            "Nicholas Pooran",
            "https://sports.ndtv.com/cricket/rcb-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-15"
            "-bclko04102023222187",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers-bangalore-vs"
            "-lucknow-super-giants-15th-match-1359489/full-scorecard"
        )
    )


def match16():
    asyncio.run(
        match_data(
            16, "DC", "MI", "Arun Jaitley Stadium", "MI", "field", True, "MI", "172/10", "51/1", "173/4", "68/0",
            "Rohit Sharma",
            "https://sports.ndtv.com/cricket/dc-vs-mi-scorecard-live-cricket-score-ipl-2023-match-16"
            "-ddmi04112023222188",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-mumbai-indians"
            "-16th-match-1359490/full-scorecard"
        )
    )


def match17():
    asyncio.run(match_data(17, "CSK", "RR", "MA Chidambaram Stadium", "CSK", "field", True, "RR", "175/8", "57/1",
                           "172/6", "45/1", "Ravichandran Ashwin",
                           "https://sports.ndtv.com/cricket/csk-vs-rr-scorecard-live-cricket-score-ipl-2023-match-17"
                           "-ckrr04122023222189",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super"
                           "-kings-vs-rajasthan-royals-17th-match-1359491/full-scorecard"))


def match18():
    asyncio.run(match_data(18, "PBKS", "GT", "Punjab Cricket Association IS Bindra Stadium", "GT", "field", True,
                           "GT", "153/8", "52/2", "154/4", "56/1", "Mohit Sharma",
                           "https://sports.ndtv.com/cricket/pbks-vs-gt-scorecard-live-cricket-score-ipl-2023-match-18"
                           "-kpahm04132023222190",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs"
                           "-gujarat-titans-18th-match-1359492/full-scorecard"))


def match19():
    asyncio.run(
        match_data(
            19, "KKR", "SRH", "Eden Gardens", "KKR", "field", True, "SRH", "228/4", "65/2", "205/7", "62/3",
            "Harry Brook",
            "https://sports.ndtv.com/cricket/kkr-vs-srh-scorecard-live-cricket-score-indian-premier-league-2023-match"
            "-19-krsh04142023222191",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight-riders-vs"
            "-sunrisers-hyderabad-19th-match-1359493/full-scorecard"
        )
    )


def match20():
    asyncio.run(
        match_data(
            20, "RCB", "DC", "M.Chinnaswamy Stadium", "DC", "field", False, "RCB", "174/6", "47/1", "151/9", "32/4",
            "Virat Kohli",
            "https://sports.ndtv.com/cricket/rcb-vs-dc-scorecard-live-cricket-score-ipl-2023-match-20"
            "-bcdd04152023222192",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers-bangalore-vs"
            "-delhi-capitals-20th-match-1359494/full-scorecard"
        )
    )


def match21():
    asyncio.run(
        match_data(
            21, "LSG", "PBKS", "Atal Bihari Vajpayee Ekana Cricket Stadium", "PBKS", "field", True, "PBKS", "159/8",
            "49/0", "161/8", "45/3", "Sikandar Raza",
            "https://sports.ndtv.com/cricket/lsg-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-21"
            "-lkokp04152023222193",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-punjab"
            "-kings-21st-match-1359495/full-scorecard"
        )
    )


def match22():
    asyncio.run(
        match_data(
            22, "MI", "KKR", "Wankhede Stadium", "MI", "field", False, "MI", "185/6", "57/2", "186/5", "72/1",
            "Venkatesh Iyer",
            "https://sports.ndtv.com/cricket/mi-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-22"
            "-mikr04162023222194",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs-kolkata-knight"
            "-riders-22nd-match-1359496/full-scorecard"
        )
    )


def match23():
    asyncio.run(match_data(23, "GT", "RR", "Narendra Modi Stadium", "RR", "field", True, "RR", "177/7", "42/2", "179/7",
                           "26/2", "Shimron Hetmyer",
                           "https://sports.ndtv.com/cricket/gt-vs-rr-scorecard-live-cricket-score-ipl-2023-match-23"
                           "-ahmrr04162023222195",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-rajasthan-royals-23rd-match-1359497/full-scorecard"))


def match24():
    asyncio.run(
        match_data(
            24, "RCB", "CSK", "M.Chinnaswamy Stadium", "RCB", "field", True, "CSK", "226/6", "53/1", "218/8", "75/2",
            "Devon Conway",
            "https://sports.ndtv.com/cricket/rcb-vs-csk-scorecard-live-cricket-score-ipl-2023-match-24"
            "-bcck04172023222196",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers-bangalore-vs"
            "-chennai-super-kings-24th-match-1359498/full-scorecard"
        )
    )


def match25():
    asyncio.run(
        match_data(
            25, "SRH", "MI", "Rajiv Gandhi International Stadium", "SRH", "field", True, "MI", "192/5", "53/1",
            "178/10", "42/2", "Cameron Green",
            "https://sports.ndtv.com/cricket/srh-vs-mi-scorecard-live-cricket-score-ipl-2023-match-25"
            "-shmi04182023222197",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-mumbai"
            "-indians-25th-match-1359499/full-scorecard"
        )
    )


def match26():
    asyncio.run(match_data(26, "RR", "LSG", "Sawai Mansingh Stadium", "RR", "field", True, "LSG", "37/0", "154/7",
                           "144/6", "47/0", "Marcus Stoinis",
                           "https://sports.ndtv.com/cricket/rr-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-26"
                           "-rrlko04192023222198",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-lucknow-super-giants-26th-match-1359500/full-scorecard"))


def match27():
    asyncio.run(
        match_data(
            27, "PBKS", "RCB", "Punjab Cricket Association IS Bindra Stadium", "PBKS", "field", False, "RCB", "174/4",
            "59/0", "150/10", "49/4", "Mohammed Siraj",
            "https://sports.ndtv.com/cricket/pbks-vs-rcb-scorecard-live-cricket-score-ipl-2023-match-27"
            "-kpbc04202023222199",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-royal-challengers"
            "-bangalore-27th-match-1359501/full-scorecard"
        )
    )


def match28():
    asyncio.run(
        match_data(
            28, "DC", "KKR", "Arun Jaitley Stadium", "DC", "field", True, "DC", "127/10", "35/3", "128/6", "61/1",
            "Ishant Sharma",
            "https://sports.ndtv.com/cricket/dc-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-28"
            "-ddkr04202023222200",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-kolkata-knight"
            "-riders-28th-match-1359502/full-scorecard"
        )
    )


def match29():
    asyncio.run(
        match_data(
            29, "CSK", "SRH", "MA Chidambaram Stadium", "CSK", "field", True, "CSK", "134/7", "45/1", "138/3", "60/0",
            "Ravindra Jadeja",
            "https://sports.ndtv.com/cricket/csk-vs-srh-scorecard-live-cricket-score-ipl-2023-match-29"
            "-cksh04212023222201",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-sunrisers"
            "-hyderabad-29th-match-1359503/full-scorecard"
        )
    )


def match30():
    asyncio.run(match_data(30, "LSG", "GT", "Atal Bihari Vajpayee Ekana Cricket Stadium", "GT", "bat", False, "GT",
                           "135/6", "40/1", "128/7", "53/0", "Mohit Sharma",
                           "https://sports.ndtv.com/cricket/lsg-vs-gt-scorecard-live-cricket-score-ipl-2023-match-30"
                           "-lkoahm04222023222202",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super"
                           "-giants-vs-gujarat-titans-30th-match-1359504/full-scorecard"))


def match31():
    asyncio.run(
        match_data(
            31, "MI", "PBKS", "Wankhede Stadium", "MI", "field", True, "PBKS", "214/8", "58/1", "201/6", "54/1",
            "Sam Curran",
            "https://sports.ndtv.com/cricket/mi-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-31"
            "-mikp04222023222203",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs-punjab-kings"
            "-31st-match-1359505/full-scorecard"
        )
    )


def match32():
    asyncio.run(match_data(32, "RCB", "RR", "M.Chinnaswamy Stadium", "RR", "field", False, "RCB", "189/9", "62/2",
                           "182/6", "47/1", "Glenn Maxwell",
                           "https://sports.ndtv.com/cricket/rcb-vs-rr-scorecard-live-cricket-score-ipl-2023-match-32"
                           "-bcrr04232023222204",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers"
                           "-bangalore-vs-rajasthan-royals-32nd-match-1359506/full-scorecard"))


def match33():
    asyncio.run(
        match_data(
            33, "KKR", "CSK", "Eden Gardens", "KKR", "field", True, "CSK", "235/4", "59/0", "186/8", "38/2",
            "Ajinkya Rahane",
            "https://sports.ndtv.com/cricket/kkr-vs-csk-scorecard-live-cricket-score-ipl-2023-match-33"
            "-krck04232023222205",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight-riders-vs-chennai"
            "-super-kings-33rd-match-1359507/full-scorecard"
        )
    )


def match34():
    asyncio.run(
        match_data(
            34, "SRH", "DC", "Rajiv Gandhi International Stadium", "DC", "bat", True, "DC", "144/9", "49/2", "137/6",
            "36/1", "Axar Patel",
            "https://sports.ndtv.com/cricket/srh-vs-dc-scorecard-live-cricket-score-ipl-2023-match-34"
            "-shdd04242023222206",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-delhi"
            "-capitals-34th-match-1359508/full-scorecard"
        )
    )


def match35():
    asyncio.run(match_data(35, "GT", "MI", "Narendra Modi Stadium", "MI", "field", True, "GT", "207/6", "50/1", "152/9",
                           "29/1", "Abhinav Manohar",
                           "https://sports.ndtv.com/cricket/gt-vs-mi-scorecard-live-cricket-score-ipl-2023-match-35"
                           "-ahmmi04252023222207",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-mumbai-indians-35th-match-1359509/full-scorecard"))


def match36():
    asyncio.run(
        match_data(
            36, "RCB", "KKR", "M.Chinnaswamy Stadium", "RCB", "field", True, "KKR", "200/5", "66/0", "179/8", "58/3",
            "Varun Chakravarthy",
            "https://sports.ndtv.com/cricket/rcb-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-36"
            "-bckr04262023222208",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers-bangalore-vs"
            "-kolkata-knight-riders-36th-match-1359510/full-scorecard"
        )
    )


def match37():
    asyncio.run(match_data(37, "RR", "CSK", "Sawai Mansingh Stadium", "RR", "bat", True, "RR", "202/5", "64/0",
                           "170/6", "42/1", "Yashasvi Jaiswal",
                           "https://sports.ndtv.com/cricket/rr-vs-csk-scorecard-live-cricket-score-ipl-2023-match-37"
                           "-rrck04272023222209",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-chennai-super-kings-37th-match-1359511/full-scorecard"))


def match38():
    asyncio.run(
        match_data(
            38, "PBKS", "LSG", "Punjab Cricket Association IS Bindra Stadium", "PBKS", "field", True, "LSG", "257/5",
            "74/2", "201/10", "55/2", "Marcus Stoinis",
            "https://sports.ndtv.com/cricket/pbks-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-38"
            "-kplko04282023222210",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-lucknow-super"
            "-giants-38th-match-1359512/full-scorecard"
        )
    )


def match39():
    asyncio.run(match_data(39, "KKR", "GT", "Eden Gardens", "GT", "field", False, "GT", "179/7", "61/2", "180/3",
                           "52/1", "Josh Little",
                           "https://sports.ndtv.com/cricket/kkr-vs-gt-scorecard-live-cricket-score-ipl-2023-match-39"
                           "-krahm04292023222211",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight"
                           "-riders-vs-gujarat-titans-39th-match-1359513/full-scorecard"))


def match40():
    asyncio.run(
        match_data(
            40, "DC", "SRH", "Arun Jaitley Stadium", "SRH", "bat", True, "SRH", "197/6", "62/2", "188/6",
            "57/1", "Mitchell Marsh",
            "https://sports.ndtv.com/cricket/dc-vs-srh-scorecard-live-cricket-score-ipl-2023-match-40"
            "-ddsh04292023222212",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-sunrisers"
            "-hyderabad-40th-match-1359514/full-scorecard"
        )
    )


def match41():
    asyncio.run(
        match_data(
            41, "CSK", "PBKS", "M.Chinnaswamy Stadium", "CSK", "bat", False, "PBKS", "200/4", "57/0", "201/6", "62/1",
            "Devon Conway",
            "https://sports.ndtv.com/cricket/csk-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-41"
            "-ckkp04302023222213",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-punjab"
            "-kings-41st-match-1359515/full-scorecard"
        )
    )


def match42():
    asyncio.run(match_data(42, "MI", "RR", "Wankhede Stadium", "RR", "bat", True, "MI", "212/7", "65/0", "214/4",
                           "58/1", "Yashasvi Jaiswal",
                           "https://sports.ndtv.com/cricket/mi-vs-rr-scorecard-live-cricket-score-ipl-2023-match-42"
                           "-mirr04302023222214",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs"
                           "-rajasthan-royals-42nd-match-1359516/full-scorecard"))


def match43():
    asyncio.run(
        match_data(
            43, "LSG", "RCB", "Atal Bihari Vajpayee Ekana Cricket Stadium", "RCB", "bat", True, "RCB", "126/9", "42/0",
            "108/10", "34/4", "Faf du Plessis",
            "https://sports.ndtv.com/cricket/lsg-vs-rcb-scorecard-live-cricket-score-indian-premier-league-2023-match"
            "-43-lkobc05012023222215",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-royal"
            "-challengers-bangalore-43rd-match-1359517/full-scorecard"
        )
    )


def match44():
    asyncio.run(match_data(44, "GT", "DC", "Narendra Modi Stadium", "DC", "bat", True, "DC", "130/8", "28/5", "125/6",
                           "31/3", "Mohammed Shami",
                           "https://sports.ndtv.com/cricket/gt-vs-dc-scorecard-live-cricket-score-ipl-2023-match-44"
                           "-ahmdd05022023222216",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-delhi-capitals-44th-match-1359518/full-scorecard"))


def match45():
    # Match-45 was cancelled due to rain
    return None


def match46():
    asyncio.run(
        match_data(
            46, "PBKS", "MI", "Punjab Cricket Association IS Bindra Stadium", "MI", "field", True, "MI", "214/3",
            "50/1", "216/4", "54/2", "Ishan Kishan",
            "https://sports.ndtv.com/cricket/pbks-vs-mi-scorecard-live-cricket-score-ipl-2023-match-46"
            "-kpmi05032023222217",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-mumbai-indians"
            "-46th-match-1359520/full-scorecard"
        )
    )


def match47():
    asyncio.run(
        match_data(
            47, "SRH", "KKR", "Rajiv Gandhi International Stadium", "KKR", "bat", True, "KKR", "171/9", "49/3", "166/8",
            "53/3", "Varun Chakravarthy",
            "https://sports.ndtv.com/cricket/srh-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-47"
            "-shkr05042023222219",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-kolkata"
            "-knight-riders-47th-match-1359521/full-scorecard"
        )
    )


def match48():
    asyncio.run(match_data(48, "RR", "GT", "Sawai Mansingh Stadium", "RR", "bat", True, "GT", "118/10", "50/2",
                           "119/1", "49/0", "Rashid Khan",
                           "https://sports.ndtv.com/cricket/rr-vs-gt-scorecard-live-cricket-score-ipl-2023-match-48"
                           "-rrahm05052023222220",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-gujarat-titans-48th-match-1359522/full-scorecard"))


def match49():
    asyncio.run(
        match_data(
            49, "CSK", "MI", "MA Chidambaram Stadium", "CSK", "field", False, "CSK", "139/8", "34/3", "140/4", "55/1",
            "Matheesha Pathirana",
            "https://sports.ndtv.com/cricket/csk-vs-mi-scorecard-live-cricket-score-ipl-2023-match-49"
            "-ckmi05062023222221",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-mumbai"
            "-indians-49th-match-1359523/full-scorecard"
        )
    )


def match50():
    asyncio.run(
        match_data(
            50, "DC", "RCB", "Arun Jaitley Stadium", "RCB", "bat", True, "DC", "181/4", "51/0", "187/3", "70/1",
            "Phil Salt",
            "https://sports.ndtv.com/cricket/dc-vs-rcb-scorecard-live-cricket-score-indian-premier-league-2023-match"
            "-50-ddbc05062023222222",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-royal"
            "-challengers-bangalore-50th-match-1359524/full-scorecard"
        )
    )


def match51():
    asyncio.run(match_data(51, "GT", "LSG", "Narendra Modi Stadium", "LSG", "field", False, "GT", "227/2",
                           "78/0", "171/7", "72/0", "Shubman Gill",
                           "https://sports.ndtv.com/cricket/gt-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-51"
                           "-ahmlko05072023222223",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-lucknow-super-giants-51st-match-1359525/full-scorecard"))


def match52():
    asyncio.run(match_data(52, "RR", "SRH", "Sawai Mansingh Stadium", "RR", "bat", True, "SRH", "214/2", "61/1",
                           "217/6", "52/1", "Glenn Phillips",
                           "https://sports.ndtv.com/cricket/rr-vs-srh-scorecard-live-cricket-score-ipl-2023-match-52"
                           "-rrsh05072023222224",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-sunrisers-hyderabad-52nd-match-1359526/full-scorecard"))


def match53():
    asyncio.run(
        match_data(
            53, "KKR", "PBKS", "Eden Gardens", "PBKS", "bat", True, "KKR", "179/7", "58/3", "182/5", "52/1",
            "Andre Russell",
            "https://sports.ndtv.com/cricket/kkr-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-53"
            "-krkp05082023222225",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight-riders-vs-punjab"
            "-kings-53rd-match-1359527/full-scorecard"
        )
    )


def match54():
    asyncio.run(
        match_data(
            54, "MI", "RCB", "Wankhede Stadium", "MI", "field", True, "MI", "199/6", "56/2", "200/4", "62/2",
            "Suryakumar Yadav",
            "https://sports.ndtv.com/cricket/mi-vs-rcb-scorecard-live-cricket-score-indian-premier-league-2023-match"
            "-54-mibc05092023222226",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs-royal"
            "-challengers-bangalore-54th-match-1359528/full-scorecard"
        )
    )


def match55():
    asyncio.run(
        match_data(
            55, "CSK", "DC", "MA Chidambaram Stadium", "CSK", "bat", True, "CSK", "167/8", "49/1", "140/8", "47/3",
            "Ravindra Jadeja",
            "https://sports.ndtv.com/cricket/csk-vs-dc-scorecard-live-cricket-score-ipl-2023-match-55"
            "-ckdd05102023222227",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-delhi"
            "-capitals-55th-match-1359529/full-scorecard"
        )
    )


def match56():
    asyncio.run(match_data(56, "KKR", "RR", "Eden Gardens", "RR", "field", True, "RR", "149/8", "37/2", "151/1", "78/1",
                           "Yashasvi Jaiswal",
                           "https://sports.ndtv.com/cricket/kkr-vs-rr-scorecard-live-cricket-score-ipl-2023-match-56"
                           "-krrr05112023222228",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight"
                           "-riders-vs-rajasthan-royals-56th-match-1359530/full-scorecard"))


def match57():
    asyncio.run(match_data(57, "MI", "GT", "Wankhede Stadium", "GT", "field", True, "MI", "218/5", "61/0", "191/8",
                           "48/3", "Suryakumar Yadav",
                           "https://sports.ndtv.com/cricket/mi-vs-gt-scorecard-live-cricket-score-ipl-2023-match-57"
                           "-miahm05122023222229",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs"
                           "-gujarat-titans-57th-match-1359531/full-scorecard"))


def match58():
    asyncio.run(
        match_data(
            58, "SRH", "LSG", "Rajiv Gandhi International Stadium", "SRH", "bat", False, "LSG", "182/6", "56/2",
            "185/3", "30/1", "Prerak Mankad",
            "https://sports.ndtv.com/cricket/srh-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-58"
            "-shlko05132023222230",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-lucknow"
            "-super-giants-58th-match-1359532/full-scorecard"
        )
    )


def match59():
    asyncio.run(
        match_data(
            59, "DC", "PBKS", "Arun Jaitley Stadium", "DC", "field", True, "PBKS", "167/7", "46/3", "136/8", "65/0",
            "Prabhsimran Singh",
            "https://sports.ndtv.com/cricket/dc-vs-pbks-scorecard-live-cricket-score-ipl-2023-match-59"
            "-ddkp05132023222231",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-punjab-kings"
            "-59th-match-1359533/full-scorecard"
        )
    )


def match60():
    asyncio.run(match_data(60, "RR", "RCB", "Sawai Mansingh Stadium", "RCB", "bat", False, "RCB", "171/5", "42/0",
                           "59/10", "28/5", "Wayne Parnell",
                           "https://sports.ndtv.com/cricket/rr-vs-rcb-scorecard-live-cricket-score-ipl-2023-match-60"
                           "-rrbc05142023222232",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/rajasthan-royals"
                           "-vs-royal-challengers-bangalore-60th-match-1359534/full-scorecard"))


def match61():
    asyncio.run(
        match_data(
            61, "CSK", "KKR", "MA Chidambaram Stadium", "CSK", "bat", True, "KKR", "144/6", "52/1", "147/4", "46/3",
            "Rinku Singh",
            "https://sports.ndtv.com/cricket/csk-vs-kkr-scorecard-live-cricket-score-ipl-2023-match-61"
            "-ckkr05142023222233",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-kolkata"
            "-knight-riders-61st-match-1359535/full-scorecard"
        )
    )


def match62():
    asyncio.run(match_data(62, "GT", "SRH", "Narendra Modi Stadium", "SRH", "field", True, "GT", "188/9", "65/1",
                           "154/9", "45/4", "Shubman Gill",
                           "https://sports.ndtv.com/cricket/gt-vs-srh-scorecard-live-cricket-score-ipl-2023-match-62"
                           "-ahmsh05152023222234",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                           "-sunrisers-hyderabad-62nd-match-1359536/full-scorecard"))


def match63():
    asyncio.run(
        match_data(
            63, "LSG", "MI", "Atal Bihari Vajpayee Ekana Cricket Stadium", "MI", "field", True, "LSG", "177/3", "35/2",
            "172/5", "58/0", "Marcus Stoinis",
            "https://sports.ndtv.com/cricket/lsg-vs-mi-scorecard-live-cricket-score-ipl-2023-match-63"
            "-lkomi05162023222235",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-mumbai"
            "-indians-63rd-match-1359537/full-scorecard"
        )
    )


def match64():
    asyncio.run(
        match_data(
            64, "PBKS", "DC", "Dharamsala Stadium", "PBKS", "field", True, "DC", "213/2", "61/0", "198/8", "47/1",
            "Rilee Rossouw",
            "https://sports.ndtv.com/cricket/pbks-vs-dc-scorecard-live-cricket-score-ipl-2023-match-64"
            "-kpdd05172023222236",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-delhi-capitals"
            "-64th-match-1359538/full-scorecard"
        )
    )


def match65():
    asyncio.run(
        match_data(
            65, "SRH", "RCB", "Rajiv Gandhi International Stadium", "RCB", "field", True, "RCB", "186/5", "49/2",
            "187/2", "64/0", "Virat Kohli",
            "https://sports.ndtv.com/cricket/srh-vs-rcb-scorecard-live-cricket-score-indian-premier-league-2023-match"
            "-65-shbc05182023222237",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/sunrisers-hyderabad-vs-royal"
            "-challengers-bangalore-65th-match-1359539/full-scorecard"
        )
    )


def match66():
    asyncio.run(match_data(66, "PBKS", "RR", "Dharamsala Stadium", "RR", "field", True, "RR", "187/5", "48/3", "189/6",
                           "57/1", "Devdutt Padikkal",
                           "https://sports.ndtv.com/cricket/pbks-vs-rr-scorecard-live-cricket-score-ipl-2023-match-66"
                           "-kprr05192023222238",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs"
                           "-rajasthan-royals-66th-match-1359540/full-scorecard"))


def match67():
    asyncio.run(
        match_data(
            67, "DC", "CSK", "Arun Jaitley Stadium", "CSK", "bat", False, "CSK", "223/3", "52/0", "146/9", "34/3",
            "Ruturaj Gaikwad",
            "https://sports.ndtv.com/cricket/dc-vs-csk-scorecard-live-cricket-score-ipl-2023-match-67"
            "-ddck05202023222239",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/delhi-capitals-vs-chennai-super"
            "-kings-67th-match-1359541/full-scorecard"
        )
    )


def match68():
    asyncio.run(
        match_data(
            68, "KKR", "LSG", "Eden Gardens", "KKR", "field", True, "LSG", "176/8", "54/1", "175/7", "61/1",
            "Nicholas Pooran",
            "https://sports.ndtv.com/cricket/kkr-vs-lsg-scorecard-live-cricket-score-ipl-2023-match-68"
            "-krlko05202023222240",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/kolkata-knight-riders-vs-lucknow"
            "-super-giants-68th-match-1359542/full-scorecard"
        )
    )


def match69():
    asyncio.run(
        match_data(
            69, "MI", "SRH", "Wankhede Stadium", "MI", "field", False, "MI", "200/5", "53/0", "201/2", "60/1",
            "Cameron Green",
            "https://sports.ndtv.com/cricket/mi-vs-srh-scorecard-live-cricket-score-ipl-2023-match-69"
            "-mish05212023222241",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/mumbai-indians-vs-sunrisers"
            "-hyderabad-69th-match-1359543/full-scorecard"
        )
    )


def match70():
    asyncio.run(match_data(70, "RCB", "GT", "M.Chinnaswamy Stadium", "GT", "field", True, "GT", "197/5", "62/0",
                           "198/4", "51/1", "Shubman Gill",
                           "https://sports.ndtv.com/cricket/rcb-vs-gt-scorecard-live-cricket-score-ipl-2023-match-70"
                           "-bcahm05212023222242",
                           "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers"
                           "-bangalore-vs-gujarat-titans-70th-match-1359544/full-scorecard"))


def match71():
    asyncio.run(
        match_data(
            71, "CSK", "GT", "MA Chidambaram Stadium", "GT", "field", True, "CSK", "172/7", "49/0", "157/10", "41/2",
            "Ruturaj Gaikwad",
            "https://sports.ndtv.com/cricket/gt-vs-csk-scorecard-live-cricket-score-ipl-2023-qualifier-1"
            "-ahmck05232023225987",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/chennai-super-kings-vs-gujarat"
            "-titans-qualifier-1-1370350/full-scorecard"
        )
    )


def match72():
    # Technically not really a home match for MI but just so I can scrap data
    asyncio.run(
        match_data(
            72, "MI", "LSG", "MA Chidambaram Stadium", "MI", "bat", True, "MI", "182/8", "62/2", "101/10", "54/2",
            "Akash Madhwal",
            "https://sports.ndtv.com/cricket/lsg-vs-mi-scorecard-live-cricket-score-ipl-2023-eliminator"
            "-lkomi05242023225988",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-mumbai"
            "-indians-eliminator-1370351/full-scorecard"
        )
    )


def match73():
    asyncio.run(
        match_data(73, "GT", "MI", "Narendra Modi Stadium", "MI", "field", True, "GT", "233/3", "50/0", "171/10",
                   "72/3", "Shubman Gill",
                   "https://sports.ndtv.com/cricket/gt-vs-mi-scorecard-live-cricket-score-ipl-2023-qualifier-2"
                   "-ahmmi05262023225989",
                   "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs"
                   "-mumbai-indians-qualifier-2-1370352/full-scorecard"))


def match74():
    asyncio.run(
        match_data(
            74, "GT", "CSK", "Narendra Modi Stadium", "CSK", "field", True, "CSK", "214/4", "62/0", "171/5", "72/0",
            "Devon Conway",
            "https://sports.ndtv.com/cricket/csk-vs-gt-scorecard-live-cricket-score-ipl-2023-final-ckahm05282023225990",
            "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs-chennai-super"
            "-kings-final-1370353/full-scorecard"
        )
    )


def ipl_database_generator():
    import database.database_table_create
    database.database_table_create.create_database()
    match1()
    match2()
    match3()
    match4()
    match5()
    match6()
    match7()
    match8()
    match9()
    match10()
    match11()
    match12()
    match13()
    match14()
    match15()
    match16()
    match17()
    match18()
    match19()
    match20()
    match21()
    match22()
    match23()
    match24()
    match25()
    match26()
    match27()
    match28()
    match29()
    match30()
    match31()
    match32()
    match33()
    match34()
    match35()
    match36()
    match37()
    match38()
    match39()
    match40()
    match41()
    match42()
    match43()
    match44()  # -- Possible Error
    match45()
    match46()
    match47()
    match48()
    match49()
    match50()
    match51()
    match52()
    match53()
    match54()
    match55()
    match56()
    match57()
    match58()
    match59()
    match60()
    match61()
    match62()
    match63()
    match64()
    match65()
    match66()
    match67()
    match68()
    match69()
    match70()
    match71()
    match72()
    match73()
    match74()
