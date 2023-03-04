# gets a list of game ids from a steam profile ID or custom URL. errors if the profile is private

# example url: https://steamcommunity.com/id/alifeee/games/?tab=all&sort=playtime

import requests
from bs4 import BeautifulSoup


def _getProfileUrl(user: str, sort: str = "playtime"):
    assert sort in ["name", "playtime", "achievements"]
    if user.isdecimal():
        lib_url = "https://steamcommunity.com/profiles/"+user+"/games/?tab=all&sort="+sort
    else:
        lib_url = "https://steamcommunity.com/id/"+user+"/games/?tab=all&sort="+sort
    return lib_url


def _getGamesFromHTML(html: str):
    soup = BeautifulSoup(html, "html.parser")
    games = soup.find_all("div", class_="gameListRow")
    game_ids = []
    for game in games:
        # gameListRow has id="game_123456"
        game_id = game["id"].split("_")[1]
        game_ids.append(game_id)
    return game_ids


def _getHTML(url: str):
    r = requests.get(url)
    return r.text


def getGamesFromID(user: str, sort: str = "playtime"):
    url = _getProfileUrl(user, sort)
    html = _getHTML(url)
    return _getGamesFromHTML(html)

def _getGameImageURL(id: str):
    url = "https://store.steampowered.com/api/appdetails?appids="+id
    
