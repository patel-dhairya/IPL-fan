import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def get_player_async(url):
    # creates a client session which is used for multiple HTTP requests as creating a new session for each request can
    # be slow
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as team:
            # Read the content of the response using await, and parse it using BeautifulSoup.
            soup = BeautifulSoup(await team.content.read(), "html.parser")
            players = soup.find_all(class_="cb-col cb-col-50")
            players_list = [f'https://www.cricbuzz.com/{player.get("href")}' for player in players]

            tasks = []
            for player in players_list:
                tasks.append(asyncio.ensure_future(get_player_info(session, player)))
            return await asyncio.gather(*tasks)


async def get_player_info(session, player):
    async with session.get(player) as player_information:
        soup = BeautifulSoup(await player_information.content.read(), "html.parser")
        information = soup.find_all(class_="cb-col cb-col-60 cb-lst-itm-sm")
        new_information = [info.text for info in information]
        return new_information


async def main():
    info = await get_player_async("https://www.cricbuzz.com/cricket-team/gujarat-titans/971/players")
    return info

