from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
from utils.functions import *


class ForecastCity(Resource):

    @staticmethod
    def get():
        args = request.args
        days = args.get('days')
        city = args.get('city')

        validation = ValidationRequest(days, city)
        validation.set_number_argument(days)
        validation.set_city_argument(city)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        init_date = get_current_day()
        end_date = get_future_day(days)
        database_result = Database().get_forecast_city(city, init_date, end_date)

        response = {
            'city': city,
            'end_date': end_date,
            'data': []
        }
        for line in database_result:
            formated_line = {}
            for key, value in line.items():
                if isinstance(value, date):
                    value = value.strftime('%d/%m/%Y')

                formated_line[key] = value

            response['data'].append(formated_line)

        return response
