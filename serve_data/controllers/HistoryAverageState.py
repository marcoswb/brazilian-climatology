from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
from utils.functions import *


class HistoryAverageState(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        state = str(args.get('state')).upper()
        frequency = args.get('frequency')

        validation = ValidationRequest(init_date, state, frequency)
        validation.set_date_argument(init_date)
        validation.set_state_history_argument(state)
        validation.set_frequency_argument(frequency)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        match frequency:
            case 'daily':
                database_result = Database().get_daily_average_history_state(state, init_date)
            case 'weekly':
                database_result = Database().get_weekly_average_history_state(state, init_date)
            case 'monthly':
                database_result = Database().get_monthly_average_history_state(state, init_date)

        response = {
            'state': state,
            'init_date': init_date,
            'frequency': frequency,
            'data': {}
        }
        for line in database_result:
            formated_line = {}
            station_id = ''
            competence = ''
            for key, value in line.items():
                if isinstance(value, date):
                    value = value.strftime('%d/%m/%Y')

                formated_line[key] = value

                match frequency:
                    case 'daily':
                        if key == 'date':
                            competence = get_competence(value, result_format='%d/%m/%Y')
                    case 'weekly':
                        if key == 'init_date':
                            competence = get_competence(value, result_format='%d/%m/%Y')
                    case 'monthly':
                        if key == 'competence':
                            competence = str(value)

                if key == 'station_id':
                    station_id = value

            if station_id not in response['data'].keys():
                response['data'][station_id] = {}
            if competence not in response['data'][station_id].keys():
                response['data'][station_id][competence] = []

            response['data'][station_id][competence].append(formated_line)

        return response
