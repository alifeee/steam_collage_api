# Web api using Flask, to return simple data
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class GetImage(Resource):
    def get(self, profile):
        return {"profile": profile}


api.add_resource(GetImage, '/steamcollage/<string:profile>')

if __name__ == '__main__':
    app.run()
