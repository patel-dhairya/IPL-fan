import sqlite3


def update_player_stat(player_name, match_id, opponent_team, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0,
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
            wicket_taken_bowled (int): the number of wickets taken by the player through bowleds
            wicket_taken_stump (int): the number of wickets taken by the player through stumpings

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
