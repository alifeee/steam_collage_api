import re
import requests

with open("api_key.txt", "r") as f:
    API_KEY = f.read()


def isVanityUrl(profile_string: str):
    """Check if profile string is a vanity url

    Args:
        profile_string (str): Profile string, e.g. "alifeee" or "5164879451874"

    Returns:
        bool: True if profile string is a vanity url
    """
    return re.match(r'^[0-9]{17}$', profile_string) is None


def get64BitFromVanityUrl(vanity_url: str):
    """Get 64 bit steam id from vanity url

    Args:
        vanity_url (str): Vanity url extension, e.g. "alifeee"

    Raises:
        Exception: If API response is invalid

    Returns:
        str: 64 bit steam id
    """
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {
        "key": API_KEY,
        "vanityurl": vanity_url
    }
    r = requests.get(url, params=params)
    json = r.json()
    if "response" not in json:
        raise Exception(f"No response in json: {json}")
    response = json["response"]
    if "steamid" not in response:
        raise Exception(f"No steamid in response: {response}")
    return response["steamid"]
