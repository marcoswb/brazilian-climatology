from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL

from database.Postgre import City, ForecastAverage
from utils.ValidationRequest import ValidationRequest
from utils.functions import *


class ForecastAverageState(Resource):

    @staticmethod
    def get():
        args = request.args
        period_day = args.get('period_day')
        state = str(args.get('state')).upper()

        validation = ValidationRequest(period_day, state)
        validation.set_period_argument(period_day)
        validation.set_state_forecast_argument(state)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        database_result = ForecastAverage.select().where(SQL(f"id_city in (select sub.id from city as sub where sub.state = '{state}')") &
                                                         SQL(f"period_day = '{period_day}'")).dicts()

        response = {
            'state': state,
            'period_day': period_day,
            'data': []
        }
        for line in database_result:
            response['data'].append(line)

        return response
