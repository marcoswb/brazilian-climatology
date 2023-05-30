from flask_restful import Resource
from flask import request
from peewee import SQL

from database.Postgre import DailyAverageHistory, WeeklyAverageHistory, MonthlyAverageHistory
from serve_data.classes.ValidationRequest import ValidationRequest
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
                database_result = DailyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                                     SQL(f"date >= '{init_date}'")).order_by(DailyAverageHistory.date).dicts()
            case 'weekly':
                database_result = WeeklyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                                      SQL(f"init_date >= '{init_date}'")).order_by(WeeklyAverageHistory.init_date).dicts()
            case 'monthly':
                database_result = MonthlyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                                       SQL(f"competence >= '{init_date}'")).order_by(MonthlyAverageHistory.competence).dicts()

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
