import sqlite3


def update_player_stat(player_name, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0,
                       out_style=None, not_out=0, catch=0, run_out=0, stumping=0, bowling_bowl=0, bowling_run=0,
                       wicket_taken=0, wicket_taken_catch=0, wicket_taken_bowled=0, wicket_taken_stump=0):
    """
            Adds data to the player's record for a match they played in

            Parameters:
            batting_run (int): the number of runs scored by the player while batting
            batting_bowl (int): the number of balls faced by the player while batting
            batting_4 (int): the number of fours scored by the player while batting
            batting_6 (int): the number of sixes scored by the player while batting
            out_style (str): the way the player was dismissed (catch, run-out, stump, bowled) or None if not out
            not_out (int): 1 if the player was not out, 0 otherwise
            catch (int): the number of catches taken by the player in the field
            run_out (int): the number of run outs executed by the player in the field
            stumping (int): the number of stumpings executed by the player in the field
            bowling_bowl (int): the number of balls bowled by the player
            bowling_run (int): the number of runs given away by the player while bowling
            wicket_taken (int): the number of wickets taken by the player while bowling
            wicket_taken_catch (int): the number of wickets taken by the player through catches
            wicket_taken_bowled (int): the number of wickets taken by the player through bowled
            wicket_taken_stump (int): the number of wickets taken by the player through stumping

            Returns:
            None
    """

    # Create a connection with database
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    query = "UPDATE player_stat " \
            "SET match_played = match_player + 1, batting_runs_scored = batting_runs_scored + ?," \
            "batting_bowls_played = batting_bowls_played + ?, batting_boundary = batting_boundary + ?," \
            "batting_six = batting_six + ?, batting_half_century = batting_half_century + ?, " \
            "batting_century = batting_century + ?, batting_duck_out = batting_duck_out + ?, " \
            "highest_score = highest_score + ?, batting_not_out = batting_not_out + ?, out_catch = out_catch + ?" \
            "out_run_out = out_run_out + ?, out_stumped = out_stumped + ?, out_bowled = out_bowled + ?, " \
            "field_catch = field_catch + ?, field_run_out = field_run_out + ?, field_stumping = field_stumping + ?," \
            "bowling_bowls = bowling_bowls + ?, bowling_runs = bowling_runs + ?, bowling_wickets = bowling_wickets+?," \
            "bowling_wicket_catch = bowling_wicket_catch + ?, bowling_wicket_bowled = bowling_wicket_bowled + ?," \
            "bowling_wicket_stump = bowling_wicket_stump + ?, bowling_best_figure = ? , " \
            "bowling_five_wickets = bowling_five_wickets + ?" \
            "WHERE player_name = ? LIMIT 1;"

    # Check if player hit half-century(50 runs) or century(100 runs)
    century = True if batting_run >= 100 else False
    half_century = True if 50 <= batting_run < 100 else False

    # Check if player is duck out/got out on 0
    duck_out = True if batting_run == 0 else False

    # Check if new score of player is higher than previous highest score
    current_high_score = \
        ipl_cursor.execute('SELECT highest_score FROM player_stat WHERE name = ?', (player_name,)).fetchone()[0]
    new_high_score = max(batting_run, current_high_score)

    # Type of how player got out
    # I am assuming that input provided by user is correct as currently I am the only one providing input
    out_catch = 1 if out_style == "catch" else 0
    out_run_out = 1 if out_style == "run-out" else 0
    out_stumped = 1 if out_style == "stumped" else 0
    out_bowled = 1 if out_style == "bowled" else 0

    # Check if current bowling figure is best bowling figure of bowler.

    current_best_bowling_figure = ipl_cursor.execute("SELECT bowling_best_figure FROM player_stat WHERE name = ?",
                                                     (player_name,)).fetchone()[0]
    if wicket_taken > 0:
        current_best_bowling_figure = ipl_cursor.execute("SELECT bowling_best_figure FROM player_stat WHERE name = ?",
                                                         (player_name,)).fetchone()[0]
        if wicket_taken >= int(current_best_bowling_figure.split("/")[1]):
            new_best_bowling_figure = f"{min(current_best_bowling_figure.split('/')[0], bowling_run)}/" \
                                      f"{current_best_bowling_figure.split('/')[1]}"
        else:
            new_best_bowling_figure = current_best_bowling_figure
    else:
        new_best_bowling_figure = current_best_bowling_figure

    # Check if bowler got more than or equal to 5 wickets
    five_wickets = 1 if wicket_taken >= 5 else 0

    ipl_cursor.execute(query, (batting_run, batting_bowl, batting_4, batting_6, int(half_century), int(century),
                               int(duck_out), new_high_score, not_out, out_catch, out_run_out, out_stumped,
                               out_bowled, catch, run_out, stumping, bowling_bowl, bowling_run, wicket_taken,
                               wicket_taken_catch, wicket_taken_bowled, wicket_taken_stump, new_best_bowling_figure,
                               five_wickets, player_name,))

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()


def add_player_bat_data(player_name: str, match_id: int, opponent_team: str, runs: int, balls: int, boundaries: int,
                        sixes: int, not_out: bool, out_type: str = "None", wicket_bowling_style: str = None,
                        wicket_bowler: str = None, fielder: str = None, motm: bool = False) -> str:
    """
    Add player batting performance to two tables - Batting Performance and Player Stats Summary
    Batting performance stores player performance against each opponent and can be seen with help of player name,
    match id or opponent_team name, whereas Player Stats Summary shows combined performance of player from all matches
    played in tournament by player with batting, fielding and bowling stats. It is not as detailed as individual
    performance tables - Batting Performance and Bowling Performance


    :param player_name: The name of the player.
    :param match_id: The id of match for player's performance
    :param opponent_team: Opponent team in this match
    :param runs: The number of runs scored by the player in this match
    :param balls: The total number of balls faced by the player in this match
    :param boundaries: The total number of 4s scored by the player in this match
    :param sixes: The total number of 6s scored by the player in this match
    :param not_out: Shows weather player was not out while batting in this match. False for out and True for not out.
    :param out_type: Shows how player got out in this match if player batted in this match.
    :param wicket_bowling_style: Shows if player got out then what was the bowling style if player got out except by
    run out
    :param wicket_bowler: Shows which bowler was responsible if player got out by bowled, stumped or caught. None if
    player was not out or got run out
    :param fielder: Show which fielder was responsible for player dismissal if player got caught, stumped or run out.
    None if player was not out or got bowled
    :param motm: True if performance of player received man of the match award
    :return: Returns message about successful entry of player stat to database else raise error
    :rtype: str
    """
    try:
        # Create a connection to the database
        ipl_db = sqlite3.connect("ipl.db")
        ipl_cursor = ipl_db.cursor()

        # First, add data to batting performance
        ipl_cursor.execute('''
        INSERT INTO "Batting Performance" (
            Name, "Match ID", Opponent, Runs, Balls, "4s", "6s", "Not out", "Out type", "Wicket bowling style", "Wicket 
            bowler", Fielder, "Man of the match") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_name, match_id, opponent_team, runs, balls, boundaries, sixes, not_out, out_type,
              wicket_bowling_style, wicket_bowler, fielder, int(motm)))

        # Now, add data to player overall performance summary table
        # But before that we need few extra variables to handle cases
        query = ''' UPDATE "Player Stats Summary"
            SET "Match Played (bat)" = "Match Played (bat)" + 1, "Runs (bat)" = "Runs (bat)" + ?, "Balls (bat)" = 
            "Balls (bat)" + ?, "4s" = "4s" + ?, "6s" = "6s" + ?, "Half Centuries" = "Half Centuries" + ?, "Centuries" = 
            "Centuries" + ?, "Duck outs" = "Duck outs" + ?, "Highest Score" = ?, NO = NO + ?, "Out (catch)" = 
            "Out (catch)" + ?, "Out (run out)" = "Out (run out)" + ?, "Out (stumped)" = "Out (stumped)" + ?, 
            "Out (bowled)" = "Out (bowled)" + ?, "Out (lbw)" = "Out (lbw)" + ?
            WHERE player_name = ? LIMIT 1;"
        '''

        # Extra variables for query for Player Stats summary
        # Check if player hit half-century(50 runs) or century(100 runs)
        century = True if runs >= 100 else False
        half_century = True if 50 <= runs < 100 else False

        # Check if player is duck out/got out on 0
        duck_out = True if runs == 0 else False

        # Check if new score of player is higher than previous highest score
        current_high_score = ipl_cursor.execute('SELECT "Highest Score" FROM "Player Stats Summary" WHERE name = ?',
                                                player_name).fetchone()
        new_high_score = max(runs, current_high_score)

        # Type of how player got out
        # I am assuming that input provided by user is correct as currently I am the only one providing input
        out_catch = 1 if out_type == "catch" else 0
        out_run_out = 1 if out_type == "run-out" else 0
        out_stumped = 1 if out_type == "stumped" else 0
        out_bowled = 1 if out_type == "bowled" else 0
        out_lbw = 1 if out_type == "lbw" else 0

        ipl_cursor.execute(query, (runs, balls, boundaries, sixes, half_century, century, duck_out,
                                   new_high_score, int(not_out), out_catch, out_run_out, out_stumped, out_bowled,
                                   out_lbw, player_name))

        # Close the connection
        ipl_db.commit()
        ipl_cursor.close()
        ipl_db.close()
        return f"Batting data added successfully for {player_name}, {match_id}"

    except Exception as e:
        return f"Error: {str(e)}"


def add_player_bowl_data(player_name: str, match_id: int, opponent_team: str, balls: int, runs_conceded: int,
                         wickets: int, maiden_overs: int, dot_balls: int, boundaries_conceded: int,
                         six_conceded: int, wides: int, no_balls: int, wickets_catch: int, wickets_bowled: int,
                         wickets_stumped: int, wickets_lbw: int, field_catch: int, field_runout: int,
                         field_stumping: int, motm: bool) -> str:
    """
    Add player bowling/fielding performance to two tables - Bowling Performance and Player Stats Summary
    Bowling performance stores player performance against each opponent and can be seen with help of player name,
    match id or opponent_team name, whereas Player Stats Summary shows combined performance of player from all matches
    played in tournament by player with batting, fielding and bowling stats. It is not as detailed as individual
    performance tables - Batting Performance and Bowling Performance

    :param player_name: The name of the player.
    :param match_id:  The id of match for player's performance
    :param opponent_team: Opponent team in this match
    :param balls: The total number of balls bowled by the player in this match
    :param runs_conceded: The total number of runs given by the player while bowling in this match
    :param wickets: The total number of wickets taken by the player in this match
    :param maiden_overs: The total number of maiden overs thrown by bowler (maiden over = 0 runs in over)
    :param dot_balls: The total number of dot balls thrown by bowler (dot ball = 0 run conceded)
    :param boundaries_conceded: Number of boundaries conceded by bowler
    :param six_conceded: Number of sixes conceded by bowler
    :param wides: Number of wides thrown by bowler
    :param no_balls: Number of no balls thrown by bowler
    :param wickets_catch: The total number of wickets taken by the bowler through catches in this match
    :param wickets_bowled: The total number of wickets taken by the bowler by hitting the wicket with a ball in this
    match
    :param wickets_stumped: The total number of wickets taken by the bowler through stump out in this match
    :param wickets_lbw: The total number of wickets taken by bowler through lbw in this match
    :param field_catch: The total number of catches taken by the player in the field in this match
    :param field_runout: The total number of run outs player was associated with in this match
    :param field_stumping: The total number of times the player has stumped out a batsman in this match
    :param motm: 1 if performance of player received man of the match award
    :return: Returns message about successful entry of player stat to database else raise error
    :rtype: str
    """
    try:
        # Create a connection to the database
        ipl_db = sqlite3.connect("ipl.db")
        ipl_cursor = ipl_db.cursor()

        # First, add data to bowling performance
        ipl_cursor.execute('''
        INSERT INTO "Batting Performance" (
            Name, "Match ID", Opponent,  balls, "Runs conceded", Wickets, "Maiden over", "Dot ball", "4s conceded", 
            "6s conceded", Wides, "No balls", "Wicket-catch", "Wicket-bowled", "Wicket-stumped", "Wicket-lbw", 
            "Field-catch", "Field-runout", "Field-stumping", "Man of the match") 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_name, match_id, opponent_team, balls, runs_conceded, wickets, maiden_overs, dot_balls,
              boundaries_conceded, six_conceded, wides, no_balls, wickets_catch, wickets_bowled, wickets_stumped,
              wickets_lbw, field_catch, field_runout, field_stumping, motm))

        # Now, add data to player overall performance summary table

        query = '''
        UPDATE "Player Stats Summary" SET "Match Played (ball)" = "Match Played (ball)" + 1, 
        "Balls (field)" = "Balls (field)" + ?, "Runs Conceded" = "Runs Conceded" + ?, Wickets = Wickets + ?, 
        "Wicket-catch" = "Wicket-catch" + ?, "Wicket-bowled" = "Wicket-bowled" + ?, "Wicket-stumped" = 
        "Wicket-stumped" + ?, "Wicket-lbw" ="Wicket-lbw" + ?, "Best Figure" = ?, "Best Figure" = "Best Figure" + ? 
        WHERE player_name = ? LIMIT 1;
        '''

        # But before that we need few extra variables to handle cases
        # Extra variables for query for Player Stats summary
        # Check if player hit half-century(50 runs) or century(100 runs)

        # Check if current bowling figure is best bowling figure of bowler
        current_best_bowling_figure = ipl_cursor.execute('''SELECT "Best Figure" FROM player_stat WHERE name = ?''',
                                                         (player_name,)).fetchone()[0]
        best_figure_run, best_figure_wicket = list(map(int, current_best_bowling_figure.split("/")))

        # Player has never taken wicket in tournament
        if best_figure_wicket == 0 and best_figure_run == 0:
            new_best_bowling_figure = f"{runs_conceded}/{wickets}"

        # Player has taken equal wicket to best bowling figure until now
        elif wickets == best_figure_wicket:
            new_best_bowling_figure = f"{min(runs_conceded, best_figure_run)}/{wickets}"
        # Player has taken more wicket than best bowling figure until this match
        elif wickets > best_figure_wicket:
            new_best_bowling_figure = f"{runs_conceded}/{wickets}"
        # Wicket taken by player in this match is less than best bowling figure wicket
        else:
            new_best_bowling_figure = current_best_bowling_figure

        # Check if bowler got more than or equal to 5 wickets
        five_wickets = 1 if wickets >= 5 else 0

        ipl_cursor.execute(query, (balls, runs_conceded, wickets, wickets_catch, wickets_bowled, wickets_stumped,
                                   wickets_lbw, new_best_bowling_figure, five_wickets, player_name))

        # Close the connection
        ipl_db.commit()
        ipl_cursor.close()
        ipl_db.close()
        return f"Fielding data added successfully for {player_name}, {match_id}"

    except Exception as e:
        return f"Error: {str(e)}"


def add_match(match_id: int, home_team: str, away_team: str, stadium: str, toss_win: str, toss_win_field_first: bool,
              winner: str, man_of_the_match: str, night_match: bool, score_inning1: int, score_inning2: int,
              pp_score1: int, pp_score2: int, inning1_highest_score: int, inning1_highest_scorer: str,
              inning1_best_bowler: str, inning1_best_bowling: str, inning2_highest_score: int,
              inning2_highest_scorer: str, inning2_best_bowler: str, inning2_best_bowling: str) -> str:
    """
    Create a new match and add it matches table in ipl database. Table is defined in add_information file alongside
    explanation of each column for match.

    :param match_id: Unique match id for each match
    :param home_team: Home team in the match
    :param away_team: Away team in the match
    :param stadium: Name of stadium where match took place
    :param toss_win: Name of team that won toss
    :param toss_win_field_first: False if winner of toss decided to bat first else True
    :param winner: Name of team that won match
    :param man_of_the_match: Name of player that won man of the match award
    :param night_match: False if match was played in afternoon else True
    :param score_inning1: Runs scored by team batting first in format of runs/wickets. (Ex. 205/2)
    :param score_inning2: Runs scored by team batting second in format of runs/wickets
    :param pp_score1: Score of team batting first in first six overs
    :param pp_score2: Score of team batting second in first six overs
    :param inning1_highest_score: Runs of player who scored the highest run in team batting first
    :param inning1_highest_scorer: Name of player who scored the highest run in first batting team
    :param inning1_best_bowler:  Name of player who bowled best in first inning
    :param inning1_best_bowling:  Bowling figure of player who bowled best in first inning in format of runs/wickets
    :param inning2_highest_score: Runs of player who scored the highest run in team batting second
    :param inning2_highest_scorer:  Name of player who scored the highest run in second batting team
    :param inning2_best_bowler:  Name of player who bowled best in second inning
    :param inning2_best_bowling: Bowling figure of player who bowled best in second inning in format of runs/wickets
    :return: Returns message about successful entry of player stat to database else raise error
    :rtype: str
    """

    try:
        # Create connection
        ipl_db = sqlite3.connect("ipl.db")
        ipl_cursor = ipl_db.cursor()

        # Create and insert a new match
        insert_statement = "INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        ipl_cursor.execute(insert_statement, (match_id, home_team, away_team, stadium, toss_win,
                                              int(toss_win_field_first), winner, man_of_the_match, int(night_match),
                                              score_inning1, score_inning2, pp_score1, pp_score2, inning1_highest_score,
                                              inning1_highest_scorer, inning1_best_bowler, inning1_best_bowling,
                                              inning2_highest_score, inning2_highest_scorer, inning2_best_bowler,
                                              inning2_best_bowling
                                              ))
        # Close the connection
        ipl_db.commit()
        ipl_cursor.close()
        ipl_db.close()
        return f"Match-{match_id}) {home_team} vs {away_team} added successfully."

    except sqlite3.IntegrityError:
        print(f"Match-{match_id} already exist in database")
        return f"Match-{match_id} already exist in database"

    except Exception as e:
        return f"{e}"
