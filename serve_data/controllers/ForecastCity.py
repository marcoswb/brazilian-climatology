from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL
from datetime import time

from database.Postgre import City, Forecast
from utils.functions import *


class ForecastCity(Resource):

    @staticmethod
    def get():
        args = request.args
        days = args.get('days')
        city = args.get('city')

        if not are_valid_values(days, city):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if not days.isdigit():
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'days'"})
            response.status_code = 400
            return response

        cities = City.select(City.id)
        list_cities = [city_db.id for city_db in cities]

        if int(city) not in list_cities:
            response = jsonify({'message': f"Valor do argumento 'city' não consta no banco de dados."})
            response.status_code = 400
            return response

        end_date = get_future_day(days)
        database_result = Forecast.select().where(SQL(f"id_city = '{city}'") &
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
