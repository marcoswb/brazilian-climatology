from flask_restful import Resource
from flask import jsonify, request

from database.Postgre import City as CityDatabase
from utils.functions import *


class City(Resource):

    @staticmethod
    def get():
        args = request.args
        filter_state = args.get('state')

        if filter_state is not None:
            if len(filter_state) != 2:
                response = jsonify({'message': f"Preencha com um valor válido o argumento 'state'"})
                response.status_code = 400
                return response

            states = CityDatabase.select(CityDatabase.state)
            list_states = [str(state_obj.state).upper() for state_obj in states]

            if filter_state not in list_states:
                response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
                response.status_code = 400
                return response

        if filter_state is not None:
            database_result = CityDatabase.select().where(CityDatabase.state == str(filter_state).upper()).order_by(CityDatabase.state, CityDatabase.city).dicts()
        else:
            database_result = CityDatabase.select().order_by(CityDatabase.state, CityDatabase.city).dicts()

        response = {}
        for line in database_result:
            state = line.get('state')
            if state not in response.keys():
                response[state] = []

            response[state].append(line)

        return response
