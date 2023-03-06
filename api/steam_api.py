import re
import requests

with open("api_key.txt", "r") as f:
    API_KEY = f.read()


def isVanityUrl(profile_string):
    return re.match(r'^[0-9]{17}$', profile_string) is None


def get64BitFromVanityUrl(vanity_url):
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
