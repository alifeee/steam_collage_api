# Web api using Flask, to return simple data
from flask import Flask, request
from steam_api import isVanityUrl, get64BitFromVanityUrl, getGamesFromSteamId, getImageUrlForGameId
from markupsafe import escape

app = Flask(__name__)


@app.route('/steamcollage')
def get():
    profile_string = request.args.get('profile_string')
    if isVanityUrl(profile_string):
        try:
            profile_id = get64BitFromVanityUrl(profile_string)
        except Exception as e:
            return f"Error: {e}", 500
    else:
        profile_id = profile_string

    try:
        games, game_count = getGamesFromSteamId(profile_id)
    except Exception as e:
        return f"Error: {e}", 500
    for game in games:
        game["img_icon_url"] = getImageUrlForGameId(game["appid"])

    return {
        "games": games,
        "game_count": game_count
    }


if __name__ == '__main__':
    app.run(debug=True)
