from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database


class ForecastAverageCity(Resource):

    @staticmethod
    def get():
        args = request.args
        period_day = args.get('period_day')
        city = args.get('city')

        validation = ValidationRequest(period_day, city)
        validation.set_period_argument(period_day)
        validation.set_city_argument(city)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        database_result = Database().get_average_forecast_city(city, period_day)
        response = {'city': city, 'period_day': period_day, 'data': []}
        for line in database_result:
            response['data'].append(line)

        return response
