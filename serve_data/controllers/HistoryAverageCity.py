from flask_restful import Resource
from flask import jsonify, request
from peewee import SQL
from datetime import time

from database.Postgre import Station, DailyAverageHistory, WeeklyAverageHistory, MonthlyAverageHistory
from utils.functions import *


class HistoryAverageCity(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        station = args.get('station')
        frequency = args.get('frequency')

        if not are_valid_values(init_date, station, frequency):
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response

        if not is_date(init_date):
            response = jsonify({'message': f"Preencha com uma data válida o argumento 'init_date'"})
            response.status_code = 400
            return response

        if not station.isdigit():
            response = jsonify({'message': f"Preencha com um valor válido o argumento 'station'"})
            response.status_code = 400
            return response

        stations = Station.select(Station.id_station)
        list_stations = [station_db.id_station for station_db in stations]

        if int(station) not in list_stations:
            response = jsonify({'message': f"Valor do argumento 'station' não consta no banco de dados."})
            response.status_code = 400
            return response

        if frequency not in ['daily', 'weekly', 'monthly']:
            response = jsonify({'message': f"Valor do argumento 'frequency' não é permitido."})
            response.status_code = 400
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
