from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL
from datetime import time

from database.Postgre import Station, History
from utils.functions import *


class HistoryState(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        times_of_day = args.get('times_of_day')
        state = str(args.get('state')).upper()

        if not are_valid_values(init_date, state):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if not is_date(init_date):
            response = jsonify({'message': f"Preencha com uma data válida o argumento 'init_date'"})
            response.status_code = 400
            return response

        if len(state) != 2:
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'state'"})
            response.status_code = 400
            return response

        states = Station.select(Station.state)
        list_states = [str(state_obj.state).upper() for state_obj in states]

        if state not in list_states:
            response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
            response.status_code = 400
            return response

        if times_of_day is not None:
            list_times = convert_time_days(times_of_day)
            if not list_times:
                response = jsonify({'message': f"Valor do argumento 'times_of_day' não é permitido."})
                response.status_code = 400
                return response
        else:
            list_times = list(range(0, 24))

        formated_list_times = "('"+"','".join([format_int_to_time(hour) for hour in list_times])+"')"
        database_result = History.select().where(SQL(f"station_id in (SELECT sub.id_station from station as sub where sub.state = '{state}')") &
                                                 SQL(f"date >= '{init_date}'") &
                                                 SQL(f"hour in {formated_list_times}")).order_by(History.date, History.hour).dicts()

        response = {
            'state': state,
            'init_date': init_date,
            'list_times': [format_int_to_time(hour) for hour in list_times],
            'data': {}
        }
        for line in database_result:
            formated_line = {}
            station_id = ''
            competence = ''
            for key, value in line.items():
                if isinstance(value, date):
                    value = value.strftime('%d/%m/%Y')
                elif isinstance(value, time):
                    value = value.strftime('%H:%M:%S')

                formated_line[key] = value
                if key == 'date':
                    competence = get_competence(value, result_format='%d/%m/%Y')
                elif key == 'station_id':
                    station_id = value

            if station_id not in response['data'].keys():
                response['data'][station_id] = {}
            if competence not in response['data'][station_id].keys():
                response['data'][station_id][competence] = []

            response['data'][station_id][competence].append(formated_line)

        return response
