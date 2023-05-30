from flask_restful import Resource
from flask import request
from peewee import SQL

from database.Postgre import ForecastAverage
from utils.ValidationRequest import ValidationRequest


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

        database_result = ForecastAverage.select().where(SQL(f"id_city = '{city}'") &
                                                         SQL(f"period_day = '{period_day}'")).dicts()

        response = {
            'city': city,
            'period_day': period_day,
            'data': []
        }
        for line in database_result:
            response['data'].append(line)

        return response
