from flask_restful import Resource
from flask import jsonify, request
from datetime import time

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
from utils.functions import *


class HistoryState(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        times_of_day = args.get('times_of_day')
        state = str(args.get('state')).upper()

        validation = ValidationRequest(init_date, state)
        validation.set_date_argument(init_date)
        validation.set_state_history_argument(state)

        invalid_data, response = validation.validate()
        if invalid_data:
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
        database_result = Database().get_history_state(state, init_date, formated_list_times)

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
