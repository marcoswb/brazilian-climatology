from flask_restful import Resource
from flask import Response


class Root(Resource):

    @staticmethod
    def get():
        return Response(status=200, mimetype='application/json')
