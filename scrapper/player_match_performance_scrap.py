import requests
from bs4 import BeautifulSoup

test_url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/punjab-kings-vs-kolkata-knight" \
           "-riders-2nd-match-1359476/full-scorecard"


def get_wicket_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    scoreboards = soup.find_all("table", {"class": "ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table"})
    for score in scoreboards:
        rows = score.find_all('tr')
        for row in rows[1:]:
            if "ds-text-tight-s" in row.get('class', []):
                break
            if row.get_text() == "":
                continue
            data = row.find_all('td')
            name = data[0].text.strip()
            dismissal = data[1].text.strip()
            runs = data[2].text.strip()
            balls = data[3].text.strip()
            fours = data[5].text.strip()
            sixes = data[6].text.strip()
            sr = data[7].text.strip()

            # Print the data for the player
            print(f"Player: {name}")
            print(f"How Dismissed: {dismissal}")
            print(f"Runs: {runs}")
            print(f"Balls: {balls}")
            print(f"Fours: {fours}")
            print(f"Sixes: {sixes}")
            print(f"Strike Rate: {sr}")
            print("\n")
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


get_wicket_info(test_url)
