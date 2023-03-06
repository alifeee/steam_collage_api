# Web api using Flask, to return simple data
from flask import Flask
from flask_restful import Resource, Api
import re
import requests
from steam_api import isVanityUrl, get64BitFromVanityUrl

app = Flask(__name__)
api = Api(app)


class GetImage(Resource):
    def get(self, profile_string):
        if isVanityUrl(profile_string):
            profile_id = get64BitFromVanityUrl(profile_string)
        else:
            profile_id = profile_string

        return {"success": "true", "profile_id": profile_id}


api.add_resource(GetImage, '/steamcollage/<string:profile_string>')

if __name__ == '__main__':
    app.run(debug=True)
