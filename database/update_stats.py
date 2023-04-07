import sqlite3


def update_player_stat(player_name, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0, out_style=None,
                       not_out=False, catch=0, run_out=0, catch_miss=0, stumping=0, bowling_bowl=0, bowling_run=0,
                       wicket_taken=0, wicket_taken_catch=0, wicket_taken_bowled=0, wicket_taken_stump=0):
    """
            Adds data to the player's record for a match they played in

            Parameters:
            batting_run (int): the number of runs scored by the player while batting
            batting_bowl (int): the number of balls faced by the player while batting
            batting_4 (int): the number of fours scored by the player while batting
            batting_6 (int): the number of sixes scored by the player while batting
            out_style (str): the way the player was dismissed (catch, run-out, stump, bowled) or None if not out
            not_out (bool): True if the player was not out, False otherwise
            catch (int): the number of catches taken by the player in the field
            run_out (int): the number of run outs executed by the player in the field
            catch_miss (int): the number of catches missed by the player in the field
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

    # query = "UPDATE player_stat " \
    #         "SET match_played = match_player + 1, batting_runs_scored = batting_runs_scored + ?," \
    #         "batting_bowls_played = batting_bowls_played + ?, batting_boundary = batting_boundary + ?," \
    #         "batting_six = batting_six + ?, batting_half_century = batting_half_century + ?, " \
    #         "batting_century = batting_century + ?, batting_duck_out = batting_duck_out + ?, " \
    #         "highest_score = highest_score + ?, batting_not_out = batting_not_out + ?" \
    #         "WHERE player_name = ? LIMIT 1;"
    # ipl_cursor.execute(query, (batting_run, player_name,))

    ipl_db.commit()
    ipl_cursor.close()
    ipl_db.close()

#
# def player_stat_db_add(player_name, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0, out_style=None,
#                        not_out=False, catch=0, run_out=0, catch_miss=0, stumping=0, bowling_bowl=0, bowling_run=0,
#                        wicket_taken=0, wicket_taken_catch=0, wicket_taken_bowled=0, wicket_taken_stump=0) -> None:
#     """
#         Adds data to the player's record for a match they played in
#
#         Parameters:
#         player_name (str): the name of player
#         batting_run (int): the number of runs scored by the player while batting
#         batting_bowl (int): the number of balls faced by the player while batting
#         batting_4 (int): the number of fours scored by the player while batting
#         batting_6 (int): the number of sixes scored by the player while batting
#         out_style (str): the way the player was dismissed (catch, run-out, stump, bowled) or None if not out
#         not_out (bool): True if the player was not out, False otherwise
#         catch (int): the number of catches taken by the player in the field
#         run_out (int): the number of run outs executed by the player in the field
#         catch_miss (int): the number of catches missed by the player in the field
#         stumping (int): the number of stumpings executed by the player in the field
#         bowling_bowl (int): the number of balls bowled by the player
#         bowling_run (int): the number of runs given away by the player while bowling
#         wicket_taken (int): the number of wickets taken by the player while bowling
#         wicket_taken_catch (int): the number of wickets taken by the player through catches
#         wicket_taken_bowled (int): the number of wickets taken by the player through bowleds
#         wicket_taken_stump (int): the number of wickets taken by the player through stumpings
#
#         Returns:
#         None
#         """
#     ipl_db = sqlite3.connect("ipl.db")
