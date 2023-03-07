import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steam_api import getGamesFromSteamId, get64BitFromVanityUrl
from images import getImageForGameId
from tqdm import tqdm


with open("api_key.txt", "r") as f:
    API_KEY = f.read()

profile_id = get64BitFromVanityUrl(API_KEY, "alifeee")
games, tot = getGamesFromSteamId(API_KEY, profile_id)

sizes = {}
for game in tqdm(games, desc="Getting image sizes", total=len(games), unit="images"):
    try:
        image = getImageForGameId(game["appid"])
    except:
        continue
    if image.size in sizes:
        sizes[image.size].append(game["name"])
    else:
        sizes[image.size] = [game["name"]]

print("Image sizes:")
for size in sizes:
    if len(sizes[size]) > 1:
        print(f"{size}: {len(sizes[size])} games")
    else:
        print(f"{size}: 1 game: {sizes[size][0]}")
