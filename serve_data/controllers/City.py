from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database


class City(Resource):

    @staticmethod
    def get():
        args = request.args
        filter_state = args.get('state')

        if filter_state is not None:
            validation = ValidationRequest()
            validation.set_state_forecast_argument(filter_state)

            invalid_data, response = validation.validate()
            if invalid_data:
                return response

        if filter_state is not None:
            database_result = Database().get_city_from_state(filter_state)
        else:
            database_result = Database().get_all_city()

        response = {}
        for line in database_result:
            state = line.get('state')
            if state not in response.keys():
                response[state] = []

            response[state].append(line)

        return response
