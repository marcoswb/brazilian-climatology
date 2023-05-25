from flask_restful import Resource
from flask import jsonify, request, Response

from utils.functions import *


class HistoryCity(Resource):

    @staticmethod
    def get():
        args = request.args
        init_date = args.get('init_date')
        times_of_day = args.get('times_of_day')
        city = args.get('city')

        if are_valid_values(init_date, times_of_day, city):
            if is_date(init_date):
                response = {'message': f'Pesquisar pelo cidade {city}, desde {init_date} nos seguintes horários {times_of_day}'}
                return response
            else:
                response = jsonify({'message': f"Preencha com uma data válida o argumento 'init_date'"})
                response.status_code = 400
                return response
        else:
            response = jsonify({'message': 'Algum argumento não foi informado.'})
            response.status_code = 422
            return response
