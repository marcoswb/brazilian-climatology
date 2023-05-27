from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL

from database.Postgre import City, ForecastAverage
from utils.functions import *


class ForecastAverageState(Resource):

    @staticmethod
    def get():
        args = request.args
        period_day = args.get('period_day')
        state = str(args.get('state')).upper()

        if not are_valid_values(period_day, state):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if period_day not in ['7', '14']:
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'period_day'"})
            response.status_code = 400
            return response

        states = City.select(City.state)
        list_states = [state_db.state for state_db in states]

        if state not in list_states:
            response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
            response.status_code = 400
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
