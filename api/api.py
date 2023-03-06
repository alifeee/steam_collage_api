# Web api using Flask, to return simple data
from flask import Flask, request, send_file
from steam_api import isVanityUrl, get64BitFromVanityUrl, getGamesFromSteamId
from images import makeCollage, serve_pil_image
from markupsafe import escape
# import stringIO

app = Flask(__name__)


with open("api_key.txt", "r") as f:
    API_KEY = f.read()


@app.route('/steamcollage')
def get():
    profile_string = request.args.get('profile_string')
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

    collage = makeCollage(games, (200, 100))
    return serve_pil_image(collage)


if __name__ == '__main__':
    app.run(debug=True)
