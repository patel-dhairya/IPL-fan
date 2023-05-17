import re
import unicodedata
import requests
from bs4 import BeautifulSoup


def remove_non_alphabetic_chars(string):
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


def get_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store batting and bowling performances
    all_batting_performance = []
    all_bowling_performance = []

    # Batting Scoreboards
    batting_scoreboard_class = soup.find_all("table", {"class": "ds-w-full ds-table ds-table-md ds-table-auto "
                                                                "ci-scorecard-table"})
    for score in batting_scoreboard_class:
        rows = score.find_all('tr')
        temp_batting_performance = []
        for row in rows[1:]:
            if "ds-text-tight-s" in row.get('class', []):
                break
            if row.get_text() == "":
                continue
            data = row.find_all('td')
            name = remove_non_alphabetic_chars(data[0].text.strip())
            dismissal = data[1].text.strip()
            runs = data[2].text.strip()
            balls = data[3].text.strip()
            fours = data[5].text.strip()
            sixes = data[6].text.strip()

            temp_batting_performance.append([name, dismissal, runs, balls, fours, sixes])
        all_batting_performance.append(temp_batting_performance)

    # Bowling Scoreboard
    bowling_scoreboard_class = soup.find_all("table", {"class": "ds-w-full ds-table ds-table-md ds-table-auto"})
    for scoreboard in bowling_scoreboard_class:
        rows = scoreboard.find_all('tr')
        temp_bowling_performance = []
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
            temp_bowling_performance.append([name, overs, maiden, runs, wickets, economy, dot, boundary, six, wide,
                                            no_balls])
        all_bowling_performance.append(temp_bowling_performance)
    # scorecard = soup.find('table', class_='ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table')
    #
    # rows = scorecard.find_all('tr')
    #
    # not_out_counter = 0
    # # Loop through the rows and extract the data for each player
    # for row in rows[1:]:  # Skip the first row (header)
    #     # Extract the data for the player

    #
    #     if dismissal == "not out":
    #         not_out_counter += 1

    # Inning-1 Scoreboard
    # inning1 = soup.select("table.ds-w-full.ds-table.ds-table-md.ds-table-auto.ci-scorecard-table")
    # print(inning1)
    #
    # batsman_name_inning1 = inning1[0].find_all("td", {"class": "ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex "
    #                                                            "ds-items-center"})
    #
    # for name in batsman_name_inning1:
    #     print(name.get_text())

    # runs = soup.find_all("td", {"class": "ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center"})
    # wickets = soup.find_all("td", {"class": "ds-min-w-max !ds-pl-[100px]"})
    #
    # bowling_table = soup.select("table.ds-w-full.ds-table.ds-table-md.ds-table-auto")
    # # print(bowling_table)
    # bowlers = bowling_table[3].find_all("span", {"class": "ds-text-tight-s ds-font-medium ds-text-typo ds-underline "
    #                                                       "ds-decoration-ui-stroke hover:ds-text-typo-primary "
    #                                                       "hover:ds-decoration-ui-stroke-primary ds-block"})
    # # batsman, bowler = [], []
    # # for run in runs:
    # #     batsman.append(" ".join(run.get_text().split()[:2]))
    # # for wicket in wickets:
    # #     if wicket.get_text().startswith("c") or wicket.get_text().startswith(" b"):
    # #         bowler.append(wicket.get_text().replace('†', ''))
    # # print(len(batsman))
    # # print(len(bowler))
    # # for i in range(len(batsman)):
    # #     print(batsman[i], bowler[i])
    # for bowler in bowlers:
    #     print(bowler.get_text())
    return all_batting_performance, all_bowling_performance
