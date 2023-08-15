import re
import requests


def isVanityUrl(profile_string: str):
    """Check if profile string is a vanity url

    Args:
        profile_string (str): Profile string, e.g. "alifeee" or "5164879451874"

    Returns:
        bool: True if profile string is a vanity url
    """
    return re.match(r"^[0-9]{17}$", profile_string) is None


def get64BitFromVanityUrl(API_KEY: str, vanity_url: str):
    """Get 64 bit steam id from vanity url

    Args:
        API_KEY (str): Steam API key
        vanity_url (str): Vanity url extension, e.g. "alifeee"

    Raises:
        Exception: If API response is invalid
        Exception: If vanity_url is not a valid vanity url

    Returns:
        str: 64 bit steam id
    """
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {"key": API_KEY, "vanityurl": vanity_url}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise ValueError(f"Request failed with status code {r.status_code}")
    try:
        json = r.json()
    except ValueError:
        raise ValueError(f"Response is not a valid json: {r.text}")
    if "response" not in json:
        raise ValueError(f"No response in json: {json}")
    response = json["response"]
    if "success" in response and response["success"] != 1:
        raise ValueError("Vanity url conversion failed.")
    if "steamid" not in response:
        raise ValueError(f"No steamid in response: {response}")
    return response["steamid"]


def getGamesFromSteamId(API_KEY: str, steam_id: str):
    """Get list of games from steam id

    Args:
        API_KEY (str): Steam API key
        steam_id (str): 64 bit steam id

    Raises:
        Exception: If steam_id is a vanity url
        Exception: If API response is invalid

    Returns:
        list: List of games
          game: {
            "appid": int,
            "name": str,
            "playtime_forever": int,
            "img_icon_url": str,
            "playtime_windows_forever": int,
            "playtime_mac_forever": int,
            "playtime_linux_forever": int
            "rtime_last_played": int
            }
        int: Number of games
    """
    if isVanityUrl(steam_id):
        raise ValueError(
            f"steam_id is a vanity url: {steam_id}. Use get64BitFromVanityUrl to convert vanity url to 64 bit steam id"
        )
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "format": "json",
        "include_appinfo": "true",
        "include_played_free_games": "true",
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise ValueError(f"Request failed with status code {r.status_code}")
    try:
        json = r.json()
    except ValueError:
        raise ValueError(f"Response is not a valid json: {r.text}")
    if "response" not in json:
        raise ValueError(f"No response in json: {json}")
    response = json["response"]
    if "games" not in response:
        raise ValueError(f"No games in response: {response}")
    if "game_count" not in response:
        raise ValueError(f"No game_count in response: {response}")
    return response["games"], response["game_count"]
