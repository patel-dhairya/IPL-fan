from database_table_add import add_match, add_player_bat_data, add_player_bowl_data


# Match-1
def match1() -> str:
    """
    Match-1 was played between CSK and GT in home ground of GT, Narendra Modi stadium. It was opening match of IPL 2023.
    GT won this match in thrilling way.
    """
    # Add match
    add_match(1, "GT", "CSK", "Narendra Modi Stadium", "GT", True, "GT", "Rashid Khan", True, "178/7", "182/5",
              "51/2", "65/1", 92, "Ruturaj Gaikwad", "Rashid Khan", "26/2", 63, "Shubman Gill", "Rajvardhan Hangargekar"
              , "36/3")

    # Add player performance
    # Inning-1 => CSK BAT and GT Field
    # CSK BAT
    add_player_bat_data("Devon Conway", 1, "GT", 1, 6, 0, 0, False, "bowled", "Mohammed Shami", "None", False)
    add_player_bat_data("Ruturaj Gaikwad", 1, " GT", 92, 50, 4, 9, False, "catch", "Alzarri Joseph", "Shubman Gill",
                        False)
    add_player_bat_data("Moeen Ali", 1, "GT", 23, 17, 4, 1, False, "catch", "Rashid Khan", "Wriddhiman Saha", False)
    add_player_bat_data("Ben Stokes", 1, "GT", 7, 6, 1, 0, False, "catch", "Rashid Khan", "Wriddhiman Saha", False)
    add_player_bat_data("Ambati Rayudu", 1, "GT", 12, 12, 0, 1, False, "bowled", "Joshua Little", "None", False)
    add_player_bat_data("Shivam Dube", 1, "GT", 19, 18, 0, 1, False, "catch", "Mohammed Shami", "Rashid Khan", False)
    add_player_bat_data("Ravindra Jadeja", 1, "GT", 1, 2, 0, 0, False, "catch", "Alzarri Joseph", "Vijay Shankar", False
                        )
    add_player_bat_data("MS Dhoni", 1, "GT", 14, 7, 1, 1, True, "None", "None", "None", motm=False)
    add_player_bat_data("Mitchell Santner ", 1, "GT", 1, 3, 0, 0, True, "None", "None", "None", motm=False)

    # GT Field
    add_player_bowl_data("Mohammed Shami", 1, "CSK", 24, 29, 2, 0, 13, 2, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, False)
    add_player_bowl_data("Hardik Pandya", 1, "CSK", 18, 28, 0, 0, 6, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, False)
    add_player_bowl_data("Joshua Little", 1, "CSK", 24, 41, 1, 0, 10, 4, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, False)
    add_player_bowl_data("Rashid Khan", 1, "CSK", 24, 26, 2, 0, 10, 2, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0, True)
    add_player_bowl_data("Alzarri Joseph", 1, "CSK", 24, 33, 2, 0, 8, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, False)
    add_player_bowl_data("Yash Dayal", 1, "CSK", 6, 14, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, False)
    add_player_bowl_data("Shubman Gill", 1, "CSK", field_catch=1)
    add_player_bowl_data("Wriddhiman Saha", 1, "CSK", field_catch=2)
    add_player_bowl_data("Vijay Shankar", 1, "CSK", field_catch=1)

    return "Data added successfully for match-1"


print(match1())
