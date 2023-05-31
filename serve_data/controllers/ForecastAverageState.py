from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database


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

        database_result = Database().get_average_forecast_state(state, period_day)
        response = {'state': state, 'period_day': period_day, 'data': []}
        for line in database_result:
            response['data'].append(line)

        return response
