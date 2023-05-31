from flask_restful import Resource

from serve_data.classes.Database import Database


class WeatherType(Resource):

    @staticmethod
    def get():
        database_result = Database().get_weather_type()
        response = []
        for line in database_result:
            response.append(line)

        return response
