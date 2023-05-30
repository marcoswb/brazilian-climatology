from flask_restful import Resource
from flask import request
from peewee import SQL

from database.Postgre import Forecast
from utils.ValidationRequest import ValidationRequest
from utils.functions import *


class ForecastState(Resource):

    @staticmethod
    def get():
        args = request.args
        days = args.get('days')
        state = str(args.get('state')).upper()

        validation = ValidationRequest(days, state)
        validation.set_number_argument(days)
        validation.set_state_forecast_argument(state)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        init_day = get_current_day()
        end_date = get_future_day(days)
        database_result = Forecast.select().where(SQL(f"id_city in (select sub.id from city as sub where sub.state = '{state}')") &
                                                  SQL(f"day >= '{init_day}'") &
                                                  SQL(f"day <= '{end_date}'")).order_by(Forecast.id_city, Forecast.day).dicts()

        response = {
            'state': state,
            'end_date': end_date,
            'data': {}
        }
        for line in database_result:
            formated_line = {}
            city = ''
            for key, value in line.items():
                if isinstance(value, date):
                    value = value.strftime('%d/%m/%Y')

                if key == 'id_city':
                    city = value

                formated_line[key] = value

            if city not in response['data'].keys():
                response['data'][city] = []

            response['data'][city].append(formated_line)

        return response
