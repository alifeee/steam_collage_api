# gets a list of game ids from a steam profile ID or custom URL. errors if the profile is private

import requests
from bs4 import BeautifulSoup


def getProfileUrl(user: str, sort: str="playtime"):
    assert sort in ["name", "playtime", "achievements"]
    if user.isdecimal():
        lib_url = "https://steamcommunity.com/profiles/"+user+"/games/?tab=all&sort="+sort
    else:
        lib_url = "https://steamcommunity.com/id/"+user+"/games/?tab=all&sort="+sort
