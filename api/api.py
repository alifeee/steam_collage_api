# Web api using Flask, to return simple data
from flask import Flask, request, send_file
from steam_api import isVanityUrl, get64BitFromVanityUrl, getGamesFromSteamId
from images import makeCollage, bytesFromPilImage
from markupsafe import escape
import os
import sys
from dotenv import load_dotenv
from waitress import serve
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


load_dotenv()

app = Flask(__name__)

API_KEY = os.environ["API_KEY"]


@app.route('/steamcollage/games')
def get():
    profile_string = request.args.get('id')
    columns = request.args.get('cols', default=8, type=int)
    rows = request.args.get('rows', default=9, type=int)
    sort = request.args.get('sort', default="playtime", type=str)
    if isVanityUrl(profile_string):
        try:
            profile_id = get64BitFromVanityUrl(API_KEY, profile_string)
        except Exception as e:
            return f"Error: {e}", 500
    else:
        profile_id = profile_string

    try:
        games, game_count = getGamesFromSteamId(API_KEY, profile_id)
    except Exception as e:
        return f"Error: {e}", 500

    if sort == "playtime":
        games.sort(key=lambda x: x["playtime_forever"], reverse=True)
    elif sort == "name":
        games.sort(key=lambda x: x["name"])
    elif sort == "recent":
        games.sort(key=lambda x: x["rtime_last_played"], reverse=True)
    else:
        return f"Error: Invalid sort option: {sort}", 500

    collage = makeCollage(games, (columns, rows))
    collage_bytes = bytesFromPilImage(collage)
    return send_file(collage_bytes, mimetype="image/png")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app, host="0.0.0.0", port=5000)
