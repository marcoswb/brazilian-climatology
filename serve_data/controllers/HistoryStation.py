from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL
from datetime import time

from utils.ValidationRequest import ValidationRequest
from database.Postgre import History
from utils.functions import *


class HistoryStation(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        times_of_day = args.get('times_of_day')
        station = args.get('station')

        validation = ValidationRequest(init_date, station)
        validation.set_date_argument(init_date)
        validation.set_station_argument(station)

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
        database_result = History.select().where(SQL(f"station_id = '{station}'") &
                                                 SQL(f"date >= '{init_date}'") &
                                                 SQL(f"hour in {formated_list_times}")).order_by(History.date, History.hour).dicts()

        response = {
            'station': station,
            'init_date': init_date,
            'list_times': [format_int_to_time(hour) for hour in list_times],
            'data': {}
        }
        for line in database_result:
            formated_line = {}
            competence = ''
            for key, value in line.items():
                if isinstance(value, date):
                    value = value.strftime('%d/%m/%Y')
                elif isinstance(value, time):
                    value = value.strftime('%H:%M:%S')

                formated_line[key] = value
                if key == 'date':
                    competence = get_competence(value, result_format='%d/%m/%Y')

            if competence not in response['data'].keys():
                response['data'][competence] = []

            response['data'][competence].append(formated_line)

        return response
