from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL

from database.Postgre import City, Forecast
from utils.functions import *


class ForecastState(Resource):

    @staticmethod
    def get():
        args = request.args
        days = args.get('days')
        state = str(args.get('state')).upper()

        if not are_valid_values(days, state):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if not days.isdigit():
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'days'"})
            response.status_code = 400
            return response

        states = City.select(City.state)
        list_states = [state_db.state for state_db in states]

        if state not in list_states:
            response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
            response.status_code = 400
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
