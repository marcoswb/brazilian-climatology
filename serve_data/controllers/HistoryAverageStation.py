from flask_restful import Resource
from flask import request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
from utils.functions import *


class HistoryAverageStation(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        station = args.get('station')
        frequency = args.get('frequency')

        validation = ValidationRequest(init_date, station, frequency)
        validation.set_date_argument(init_date)
        validation.set_station_argument(station)
        validation.set_frequency_argument(frequency)

        invalid_data, response = validation.validate()
        if invalid_data:
            return response

        match frequency:
            case 'daily':
                database_result = Database().get_daily_average_history_station(station, init_date)
            case 'weekly':
                database_result = Database().get_weekly_average_history_station(station, init_date)
            case 'monthly':
                database_result = Database().get_monthly_average_history_station(station, init_date)

        response = {
            'station': station,
            'init_date': init_date,
            'frequency': frequency,
            'data': {}
        }
        for line in database_result:
            formated_line = {}
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

            if competence not in response['data'].keys():
                response['data'][competence] = []

            response['data'][competence].append(formated_line)

        return response
