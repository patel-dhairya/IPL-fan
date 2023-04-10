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
