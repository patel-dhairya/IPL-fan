"""
This script scrapes player data from a website and saves it to a CSV file.

Author: Dhairya Patel,
Create Date: May 16, 2023,
Update Date: May 16, 2023
"""

# important necessary modules
import asyncio
import csv
import os

import aiohttp
from bs4 import BeautifulSoup

team_code = ["CSK", "DC", "GT", "KKR", "LSG", "MI", "PBKS", "RR", "RCB", "SRH"]

# Path to database folder
current_directory = os.path.dirname(os.path.abspath(__file__))
database_directory = os.path.join(current_directory, '..', 'database')
csv_file_path = os.path.join(database_directory, 'player_data.csv')


async def get_players(url: str) -> list:
    """
        Fetches the links to the squads of the teams participating in the tournament.

        Args:
            url (str): URL of the main page containing squad links.

        Returns:
            list: List of squad links.
    """
    squad_links = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            teams = soup.find_all("div", {"class": "ds-flex lg:ds-flex-row sm:ds-flex-col lg:ds-items-center "
                                                   "lg:ds-justify-between ds-py-2 ds-px-4 ds-flex-wrap "
                                                   "odd:ds-bg-fill-content-alternate"})
            for team in teams:
                squad_information = team.find_all("a", {"class": "ds-inline-flex ds-items-start ds-leading-none"})
                for squad_link in squad_information:
                    squad_links.append(f"https://www.espncricinfo.com/{squad_link.get('href')}")
    return squad_links


async def get_player_info(session: aiohttp.ClientSession, squad_link: str) -> list:
    """
        Fetches the links to the players' profiles in a squad.

        Args:
            session (aiohttp.ClientSession): A client session to make HTTP requests.
            squad_link (str): URL of the squad page.

        Returns:
            list: List of player profile links.
    """
    async with session.get(squad_link) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        players = soup.find_all("div", {"class": "ds-border-line odd:ds-border-r ds-border-b"})
        player_urls = []
        for player in players:
            player_url = player.find("a").get("href")
            player_urls.append(f"https://www.espncricinfo.com/{player_url}")
        return player_urls


async def get_player_stat(session: aiohttp.ClientSession, player_link: str) -> tuple:
    """
        Fetches the player stats from the player's profile page.

        Args:
            session (aiohttp.ClientSession): A client session to make HTTP requests.
            player_link (str): URL of the player's profile page.

        Returns:
            tuple: Player stats - name, full name, age, batting style, bowling style, role.
    """
    async with session.get(player_link) as response:
        player_background = {}
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        player_name = soup.select_one('h1.ds-text-title-l.ds-font-bold').text
        info_title = soup.find_all("p", {"class": "ds-text-tight-m ds-font-regular ds-uppercase ds-text-typo-mid3"})
        info = soup.find_all("span", {"class": "ds-text-title-s ds-font-bold ds-text-typo"})
        country = soup.select_one('span.ds-text-comfortable-s').text
        for i in range(min(len(info_title), len(info))):
            player_background[info_title[i].get_text()] = info[i].get_text()

            # If player has no bowling style, add it to background with value None
        if "Bowling Style" not in player_background:
            player_background["Bowling Style"] = "None"
        return (
        player_name, player_background["Full Name"], player_background["Age"], player_background["Batting Style"],
        player_background["Bowling Style"], player_background["Playing Role"], country)


async def main():
    squads = await get_players("https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/squads")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for squad_link in squads:
            tasks.append(get_player_info(session, squad_link))
        player_info_list = await asyncio.gather(*tasks)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Full Name', 'Age', 'Batting Style', 'Bowling Style', 'Role', "Country", "Team"])
            for index, player_info in enumerate(player_info_list):
                player_team = team_code[index]
                player_tasks = []
                for player in player_info:
                    player_tasks.append(get_player_stat(session, player))
                player_stats = await asyncio.gather(*player_tasks)
                for stats in player_stats:
                    writer.writerow(list(stats) + [player_team])
                # for player in player_info:
                #     name, full_name, age, batting_style, bowling_style, role = await get_player_stat(session, player)
                #     writer.writerow([name, full_name, age, batting_style, bowling_style, role, player_team])


asyncio.run(main())
