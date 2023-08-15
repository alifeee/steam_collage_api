"""Web api using Flask, to return simple data"""
import os
import sys
import logging
from dotenv import load_dotenv
from waitress import serve
from flask import Flask, request, send_file
from steam_api import isVanityUrl, get64BitFromVanityUrl, getGamesFromSteamId
from images import makeCollage, bytesFromPilImage

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")


load_dotenv()

app = Flask(__name__)

API_KEY = os.environ["API_KEY"]


@app.route("/steamcollage/alive")
def alive():
    """Simple endpoint to check if the server is alive"""
    return "Alive"


@app.route("/steamcollage/alive_img")
def alive_img():
    """Simple endpoint to check if the server is alive"""
    return send_file("sheep.png", mimetype="image/png")


@app.route("/steamcollage/verifyuser")
def verifyuser():
    """Endpoint to check if a user exists and is public"""
    profile_string = request.args.get("id")
    if isVanityUrl(profile_string):
        try:
            profile_id = get64BitFromVanityUrl(API_KEY, profile_string)
        except ValueError as error:
            if "Vanity url conversion failed" in str(error):
                return {"exists": False}
            return f"Error: {error}", 500
    else:
        profile_id = profile_string

    try:
        _, _ = getGamesFromSteamId(API_KEY, profile_id)
    except ValueError as error:
        if "Request failed with status code 500" in str(error):
            return {"exists": False}
        if "No games in response" in str(error):
            return {"exists": True, "private": True}
        else:
            return f"Error: {error}", 500

    return {"exists": True, "private": False}


@app.route("/steamcollage/games")
def games():
    """Endpoint to return a list of games for a user. See readme for more info"""
    profile_string = request.args.get("id")
    columns = request.args.get("cols", default=8, type=int)
    rows = request.args.get("rows", default=9, type=int)
    sort = request.args.get("sort", default="playtime", type=str)
    if isVanityUrl(profile_string):
        try:
            profile_id = get64BitFromVanityUrl(API_KEY, profile_string)
        except ValueError:
            return send_file("validity_bad-vanity-url.png", mimetype="image/png")
    else:
        profile_id = profile_string

    try:
        allgames, _ = getGamesFromSteamId(API_KEY, profile_id)
    except ValueError as error:
        if "Request failed with status code 500" in str(error):
            return send_file(
                "validity_account-does-not-exist.png",
                mimetype="image/png",
            )
        if "No games in response" in str(error):
            return send_file("validity_account-private.png", mimetype="image/png")
        else:
            return send_file(
                "validity_account-does-not-exist.png", mimetype="image/png"
            )

    if sort == "playtime":
        allgames.sort(key=lambda x: x["playtime_forever"], reverse=True)
    elif sort == "name":
        allgames.sort(key=lambda x: x["name"])
    elif sort == "recent":
        allgames.sort(key=lambda x: x["rtime_last_played"], reverse=True)
    else:
        return f"Error: Invalid sort option: {sort}", 500

    collage = makeCollage(allgames, (columns, rows))
    collage_bytes = bytesFromPilImage(collage)
    return send_file(collage_bytes, mimetype="image/jpeg")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app, host="0.0.0.0", port=5000)
