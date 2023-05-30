from flask_restful import Resource
from flask import request
from peewee import SQL

from database.Postgre import Forecast
from utils.ValidationRequest import ValidationRequest
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

        init_day = get_current_day()
        end_date = get_future_day(days)
        database_result = Forecast.select().where(SQL(f"id_city = '{city}'") &
                                                  SQL(f"day >= '{init_day}'") &
                                                  SQL(f"day <= '{end_date}'")).order_by(Forecast.day).dicts()

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
