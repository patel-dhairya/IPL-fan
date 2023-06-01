import re
import requests
from bs4 import BeautifulSoup


def remove_non_alphabetic_chars(string: str) -> str:
    """
    This function cleans string with special characters such that Shikhar Dhawan\xa0(c) to Shikhar Dhawan
    :param string: String to clean
    :return: New clean string without any special character or number
    """
    string = string.replace('\xa0', ' ')
    pattern = r'[^A-Za-z ()\-]'
    cleaned_string = re.sub(pattern, '', string)
    cleaned_string = re.sub(r'\(.*?\)', '', cleaned_string)
    return cleaned_string.strip()


def get_bowling_performance(url: str) -> dict:
    """
    Scrapes the bowling performances of players in a cricket match from the specified URL.

    :param url: The link to the match scoreboard.
    :return: A dictionary with player names as keys and a list of their performance statistics, including overs,
    maidens, runs, wickets, economy, dot balls, boundaries, sixes, wides, and no balls.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Dictionary to store bowling performances
    all_bowling_performance = {}

    # Bowling Scoreboard
    bowling_scoreboard_class = soup.find_all("table", {"class": "ds-w-full ds-table ds-table-md ds-table-auto"})
    for scoreboard in bowling_scoreboard_class:
        rows = scoreboard.find_all('tr')
        for row in rows[1:]:
            if "ds-hidden" in row.get('class', []):
                continue
            data = row.find_all("td")
            name = remove_non_alphabetic_chars(data[0].text.strip())

            overs = data[1].text.strip()
            maiden = data[2].text.strip()
            runs = data[3].text.strip()
            wickets = data[4].text.strip()
            economy = data[5].text.strip()
            dot = data[6].text.strip()
            boundary = data[7].text.strip()
            six = data[8].text.strip()
            wide = data[9].text.strip()
            no_balls = data[10].text.strip()
            all_bowling_performance[name] = [overs, maiden, runs, wickets, economy, dot, boundary, six, wide, no_balls]
    return all_bowling_performance


def get_batting_performance(url: str, scoreboard1_id: str, scoreboard2_id: str) -> dict:
    """
    Scrapes the batting performances of players in a cricket match from the NDTV Sports website.

    :param url: The link to the match scoreboard on the NDTV Sports website.
    :param scoreboard1_id: The HTML class ID for the scoreboard of the first inning.
    :param scoreboard2_id: The HTML class ID for the scoreboard of the second inning.
    :return: A dictionary with player names as keys and a list of their performance statistics, including runs, balls,
    fours, sixes, and dismissal reason (including if the player was not out).
    """

    def player_data_extraction(database, inning_number) -> dict:
        """
        Helper function to extract necessary data from the scoreboard.

        :param database: A ResultSet containing the scoreboard data.
        :param inning_number: Indicates whether it's the scoreboard of the first inning or the second inning.
        :return: A dictionary with player performances.
        """
        player_dict = {}
        for data in database:
            player_performances = data.select(f'[id^="bat_{inning_number}"]')

            for player_performance in player_performances:
                name = player_performance.find("a").contents[0].text.strip()
                runs = player_performance.select(f'[id^="runs_{inning_number}"]')[0].text
                balls = player_performance.select(f'[id^="balls_{inning_number}"]')[0].text
                boundaries = player_performance.select(f'[id^="fours_{inning_number}"]')[0].text
                sixes = player_performance.select(f'[id^="sixes_{inning_number}"]')[0].text
                player_dict[name] = [runs, balls, boundaries, sixes, None]
        return player_dict

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    inning1 = soup.find_all(id=scoreboard1_id)
    inning2 = soup.find_all(id=scoreboard2_id)
    # All dismissals in the match, including "not out" if a player stayed not out till the inning completed
    dismissals = soup.find_all(class_=["tbl_sld-ttl", "tbl_sld-tag tbl_sld-tag_1", "tbl_sld-tag tbl_sld-tag_2"])
    player_performances_combined = {**player_data_extraction(inning1, 1), **player_data_extraction(inning2, 2)}

    for index, player_performance_single in enumerate(player_performances_combined):
        player_performances_combined[player_performance_single][4] = dismissals[index].get_text()

    return player_performances_combined
