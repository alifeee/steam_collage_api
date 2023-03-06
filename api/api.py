# Web api using Flask, to return simple data
from flask import Flask
from steam_api import isVanityUrl, get64BitFromVanityUrl
from markupsafe import escape

app = Flask(__name__)


@app.route('/steamcollage/<string:profile_string>')
def get(profile_string):
    profile_string = escape(profile_string)
    if isVanityUrl(profile_string):
        profile_id = get64BitFromVanityUrl(profile_string)
    else:
        profile_id = profile_string

    return {"success": "true", "profile_id": profile_id}


if __name__ == '__main__':
    app.run(debug=True)
