from flask_restful import Resource
from flask import jsonify, request

from serve_data.classes.ValidationRequest import ValidationRequest
from serve_data.classes.Database import Database
from serve_data.classes.FormatResponse import FormatData
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

        format_data = FormatData()

        formated_list_times = format_data.format_times_to_query(list_times)
        database_result = Database().get_history_station(station, init_date, formated_list_times)

        formated_int_times = format_data.format_times_to_response(list_times)
        response = {'station': station, 'init_date': init_date, 'list_times': formated_int_times, 'data': {}}
        for line in database_result:
            formated_line, date_value = format_data.format_line(line, 'date')
            competence = get_competence(date_value, result_format='%d/%m/%Y')

            if competence not in response['data'].keys():
                response['data'][competence] = []

            response['data'][competence].append(formated_line)

        return response
