from flask_restful import Resource

from database.Postgre import WeatherType as WeatherTypeDatabase


class WeatherType(Resource):

    @staticmethod
    def get():
        database_result = WeatherTypeDatabase.select().order_by(WeatherTypeDatabase.weather_condition).dicts()

        response = []
        for line in database_result:
            response.append(line)

        return response
