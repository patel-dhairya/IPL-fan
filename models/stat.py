from player import Player
from team import Team


class PlayerStat:
    def __init__(self, player: Player):
        """
           A class to store and calculate statistics for a cricket player.

           Attributes:
           -----------
           _player : Player
               An instance of the Player class representing the cricket player
           _match_played : int
               The total number of matches played by the player
           _batting_inning : int
               The total number of innings the player has batted in
           _bowling_inning : int
               The total number of innings the player has bowled in
           _batting_runs_scored : int
               The total number of runs scored by the player
           _batting_bowls_played : int
               The total number of balls faced by the player while batting
           _batting_boundary : int
               The total number of 4s scored by the player
           _batting_six : int
               The total number of 6s scored by the player
           _batting_half_century : int
               The total number of half centuries scored by the player (50+ runs in an innings)
           _batting_century : int
               The total number of centuries scored by the player (100+ runs in an innings)
           _batting_duck_out : int
               The total number of innings the player was out without scoring any runs
           _highest_score : int
               The highest score the player has achieved in any innings
           _out_catch : int
               The total number of times the player was out caught
           _out_run_out : int
               The total number of times the player was run out
           _out_stumped : int
               The total number of times the player was stumped out
           _out_bowled : int
               The total number of times the player was bowled out
           _field_catch : int
               The total number of catches taken by the player in the field
           _field_run_out : int
               The total number of run outs achieved by the player in the field
           _field_stumping : int
               The total number of times the player has stumped out a batsman in the field
           _field_catch_miss : int
               The total number of catches missed by the player in the field
           _bowling_bowls : int
               The total number of balls bowled by the player
           _bowling_runs : int
               The total number of runs given by the player while bowling
           _bowling_wickets : int
               The total number of wickets taken by the player
           _bowling_wicket_catch : int
               The total number of wickets taken by the player through catches
           _bowling_wicket_bowled : int
               The total number of wickets taken by the player by hitting the wicket with a ball
           _bowling_wicket_stump : int
               The total number of wickets taken by the player through stump out
           _bowling_best_figures : str
               The best figure captured by player in single match
           _bowling_five_wickets : int
               Number of times player has taken 5 wickets or more in single match
           _not_out : int
               Number of times player stayed not out while batting and playing more than 0 ball
           """
        self._player = player
        self._match_played = 0
        self._batting_inning = 0
        self._bowling_inning = 0
        self._batting_runs_scored = 0
        self._batting_bowls_played = 0
        self._batting_boundary = 0
        self._batting_six = 0
        self._batting_half_century = 0
        self._batting_century = 0
        self._batting_duck_out = 0
        self._highest_score = 0
        self._out_catch = 0
        self._out_run_out = 0
        self._out_stumped = 0
        self._out_bowled = 0
        self._field_catch = 0
        self._field_run_out = 0
        self._field_stumping = 0
        self._field_catch_miss = 0
        self._bowling_bowls = 0
        self._bowling_runs = 0
        self._bowling_wickets = 0
        self._bowling_wicket_catch = 0
        self._bowling_wicket_bowled = 0
        self._bowling_wicket_stump = 0
        self._bowling_best_figure = "0/0"
        self._bowling_five_wickets = 0
        self._not_out = 0

    def add_data(self, batting_run=0, batting_bowl=0, batting_4=0, batting_6=0, out_style=None, not_out=False,
                 catch=0, run_out=0, catch_miss=0, stumping=0, bowling_bowl=0, bowling_run=0, wicket_taken=0,
                 wicket_taken_catch=0, wicket_taken_bowled=0, wicket_taken_stump=0) -> None:
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

        # Increment the number of matches played by the player
        self._match_played += 1

        # Update batting stats if player batted in the match
        if batting_bowl > 0:
            # Increment the number of innings played by the player
            self._batting_inning += 1
            # Add the batting stats for this match to the player's overall batting stats
            self._batting_runs_scored += batting_run
            self._batting_bowls_played += batting_bowl
            self._batting_boundary += batting_4
            self._batting_six += batting_6
            # Check if the player was dismissed for a duck
            if batting_run == 0:
                self._batting_duck_out += 1
            # Check if the player scored a half-century or century
            if batting_run >= 50:
                if batting_run >= 100:
                    self._batting_century += 1
                else:
                    self._batting_half_century += 1

            # Check if the player was not out or dismissed and update the relevant dismissal stats
            if not_out:
                self._not_out += 1
            else:
                if out_style == "catch":
                    self._out_catch += 1
                elif out_style == "run-out":
                    self._out_run_out += 1
                elif out_style == "stump":
                    self._out_stumped += 1
                elif out_style == "bowled":
                    self._out_bowled += 1
            self._highest_score = max(self._highest_score, batting_run)

        # Update field stats
        self._field_catch += catch
        self._field_run_out += run_out
        self._field_catch_miss += catch_miss
        self._field_stumping += stumping

        # Update bowling stats if player bowled in the match
        if bowling_bowl > 0:
            self._bowling_inning += 1
            self._bowling_bowls += bowling_bowl
            self._bowling_runs += bowling_run

            # Check if the player took wicket
            if wicket_taken > 0:
                if self._bowling_wickets >= int(self._bowling_best_figure.split("/")[0]):
                    self._bowling_best_figure = f"{self._bowling_wickets}/" \
                                                f"{min(self._bowling_runs, int(self._bowling_best_figure.split('/')[1]))}"

                self._bowling_wickets += wicket_taken
                if wicket_taken >= 5:
                    self._bowling_five_wickets += 1
                self._bowling_wicket_stump += wicket_taken_stump
                self._bowling_wicket_bowled += wicket_taken_bowled
                self._bowling_wicket_catch += wicket_taken_catch

    def stats(self, stat_type: str = None, extended: bool = False) -> dict:
        general = {"Name": self._player, "Match Played": self._match_played}
        batting_stats = {"Innings(bat)": self._batting_inning, "Runs": self._batting_runs_scored,
                         "Strike Rate": (self._batting_runs_scored / self._batting_bowls_played) * 100,
                         "Batting Average": (self._batting_runs_scored / (self._match_played - self._not_out + 1)),
                         "Boundaries": self._batting_boundary, "Sixes": self._batting_six,
                         "50s": self._batting_half_century, "100s": self._batting_century,
                         "Highest Score": self._highest_score, "Duck Out": self._batting_duck_out
                         }
        bowling_stats = {"Overs": f"{(self._bowling_bowls - self._bowling_bowls % 6) / 6}.{self._bowling_bowls % 6}",
                         "Bowls": self._bowling_bowls, "Runs Given": self._bowling_runs, "Wickets":
                             self._bowling_wickets, "Economy": 6 * (self._bowling_runs / self._bowling_bowls),
                         "Best Figures": self._bowling_best_figure,
                         "Average": self._bowling_runs if self._bowling_wickets == 0
                         else self._bowling_runs / self._bowling_wickets,
                         "5 Wickets": self._bowling_five_wickets
                         }
        fielding_stats = {"Catch Taken": self._field_catch, "Catch Missed": self._field_catch_miss,
                          "Run out": self._field_run_out}
        batting_extended = {"Total Out": self._out_stumped + self._out_catch + self._out_run_out + self._out_bowled,
                            "Out by Catch": self._out_catch, "Out by Run out": self._out_run_out,
                            "Out by Stumping": self._out_stumped, "Out by Bowled": self._out_bowled
                            }
        bowling_extended = {"Wicket Taken by Bowled": self._bowling_wicket_bowled,
                            "Wicket Taken by Catch": self._bowling_wicket_catch,
                            "Wicket Taken by Stumping": self._bowling_wicket_stump
                            }
        if stat_type is None:
            return {**general, **batting_stats, **fielding_stats, **bowling_stats}
        elif stat_type == "batting":
            return {**general, **batting_stats} if not extended else {**general, **batting_stats, **batting_extended}
        else:
            return {**general, **bowling_stats} if not extended else {**general, **bowling_stats, **bowling_extended}
