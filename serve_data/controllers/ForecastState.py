from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
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

        init_date = get_current_day()
        end_date = get_future_day(days)
        database_result = Database().get_forecast_state(state, init_date, end_date)

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
