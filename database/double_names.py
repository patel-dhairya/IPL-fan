# As program uses two different websites for batting and fielding performance scrap, sometimes players name have typo
# on one of website which could create trouble in storing all data related to player. To solve that issue, this file
# will have single function which can use stored name typo dictionary to return correct name

# Dictionary to store the corrected names for players with typos on one of the websites
name_corrections = {
    "Mohammed Shami": "Mohammad Shami",
    "Josh Little": "Joshua Little",
    "Varun Chakaravarthy": "Varun Chakravarthy",
    "Aman Khan": "Aman Hakim Khan"
}


def change_name(name: str) -> str:
    """
    Checks if a player's name has a typo on at least one website and returns the corrected name if found.
    If no correction is needed, the original name is returned.

    :param name: The name of the player to check
    :return: The corrected name if there is a typo, otherwise the original name
    """
    if name in name_corrections:
        return name_corrections[name]
    else:
        return name
