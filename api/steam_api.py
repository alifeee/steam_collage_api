import re

with open("api_key.txt", "r") as f:
    API_KEY = f.read()


def isVanityUrl(profile_string):
    return re.match(r'^[0-9]{17}$', profile_string) is None


