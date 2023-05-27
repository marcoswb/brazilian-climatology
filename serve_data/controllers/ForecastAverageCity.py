from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL

from database.Postgre import City, ForecastAverage
from utils.functions import *


class ForecastAverageCity(Resource):

    @staticmethod
    def get():
        args = request.args
        period_day = args.get('period_day')
        city = args.get('city')

        if not are_valid_values(period_day, city):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if period_day not in ['7', '14']:
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'period_day'"})
            response.status_code = 400
            return response

        cities = City.select(City.id)
        list_cities = [city_db.id for city_db in cities]

        if int(city) not in list_cities:
            response = jsonify({'message': f"Valor do argumento 'city' não consta no banco de dados."})
            response.status_code = 400
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
