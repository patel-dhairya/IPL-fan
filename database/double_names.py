# The main program scrapes batting and fielding performance data from two different websites. However, there may be
# typos in players' names on one of the websites, which can cause issues when storing the data. To address this problem,
# this file contains a function that uses a dictionary to return the correct name for a player.

# Dictionary to store the corrected names for players with typos on one of the websites
name_corrections = {
    "Mohammed Shami": "Mohammad Shami",
    "Josh Little": "Joshua Little",
    "Varun Chakaravarthy": "Varun Chakravarthy",
    "Aman Khan": "Aman Hakim Khan",
    "Philip Salt": "Phil Salt",
    "Vyshak Vijay Kumar": "Vijaykumar Vyshak"
}


def change_name(name: str) -> str:
    """
    Checks if a player's name has a typo on at least one website and returns the corrected name if found.
    If no correction is needed, the original name is returned.

    :param name: The name of the player to check
    :return: The corrected name if there is a typo, otherwise the original name
    """
    # Remove sub from player name
    name_divide = name.split(" ")
    if name_divide[0] == "sub":
        name = " ".join(name_divide[1:])

    if name in name_corrections:
        return name_corrections[name]
    else:
        return name
