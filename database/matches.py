import sqlite3


def add_match(match_id, home_team, away_team, toss_win, toss_win_field_first, winner, man_of_the_match, night_match,
              score_inning1, score_inning2, score_inning1_highest_score, score_inning1_highest_scorer,
              score_inning1_best_bowler, score_inning1_best_bowling, score_inning2_highest_score,
              score_inning2_highest_scorer, score_inning2_best_bowler, score_inning2_best_bowling) -> str:
    ipl_db = sqlite3.connect("ipl.db")
    ipl_cursor = ipl_db.cursor()

    try:
        insert_statement = "INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        ipl_cursor.execute(insert_statement, (match_id, home_team, away_team, toss_win, toss_win_field_first, winner,
                                              man_of_the_match, night_match, score_inning1, score_inning2,
                                              score_inning1_highest_score, score_inning1_highest_scorer,
                                              score_inning1_best_bowler, score_inning1_best_bowling,
                                              score_inning2_highest_score
                                              , score_inning2_highest_scorer, score_inning2_best_bowler,
                                              score_inning2_best_bowling))
        ipl_db.commit()
        ipl_cursor.close()
        ipl_db.close()
        return f"Match-{match_id}) {home_team} vs {away_team} added successfully."

    except sqlite3.IntegrityError:
        print(f"Match-{match_id} already exist in database")
        return f"Match-{match_id} already exist in database"


# Match-1
add_match(1, "GT", "CSK", "GT", 1, "GT", "Rashid Khan", 1, "178/7", "182/5", 92, "Ruturaj Gaikwad", "Rashid Khan",
          "26/2", 63, "Shubman Gill", "Rajvardhan Hangargekar", "36/3")

# Match-2
# add_match(2, "PBKS", "KKR", "KKR", 1, "PBKS", "Arshdeep Singh", 1, )
