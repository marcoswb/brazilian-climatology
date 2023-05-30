from flask import jsonify

from database.Postgre import Station, City
from utils.functions import *


class ValidationRequest:

    def __init__(self, *args):
        self.__all_arguments = list(args)
        self.__date_arguments = []
        self.__state_history_arguments = []
        self.__station_arguments = []
        self.__frequency_arguments = []
        self.__number_arguments = []
        self.__city_arguments = []
        self.__state_forecast_arguments = []
        self.__period_arguments = []

    def validate(self):
        if len(self.__all_arguments):
            for arg in self.__all_arguments:
                if not are_valid_values(arg):
                    response = jsonify({'message': 'Algum argumento não foi informado.'})
                    response.status_code = 422
                    return True, response

        if len(self.__date_arguments):
            for arg in self.__date_arguments:
                if not is_date(arg):
                    response = jsonify({'message': f"Preencha com uma data válida o argumento 'init_date'"})
                    response.status_code = 400
                    return True, response

        if len(self.__state_history_arguments):
            for arg in self.__state_history_arguments:
                if len(arg) != 2:
                    response = jsonify({'message': f"Preencha com um valor válido o argumento 'state'"})
                    response.status_code = 400
                    return True, response

                states = Station.select(Station.state)
                list_states = [str(state_obj.state).upper() for state_obj in states]

                if arg not in list_states:
                    response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
                    response.status_code = 400
                    return True, response

        if len(self.__station_arguments):
            for arg in self.__station_arguments:
                if not arg.isdigit():
                    response = jsonify({'message': f"Preencha com um valor válido o argumento 'station'"})
                    response.status_code = 400
                    return True, response

                stations = Station.select(Station.id_station)
                list_stations = [station_db.id_station for station_db in stations]

                if int(arg) not in list_stations:
                    response = jsonify({'message': f"Valor do argumento 'station' não consta no banco de dados."})
                    response.status_code = 400
                    return True, response

        if len(self.__frequency_arguments):
            for arg in self.__frequency_arguments:
                if arg not in ['daily', 'weekly', 'monthly']:
                    response = jsonify({'message': f"Valor do argumento 'frequency' não é permitido."})
                    response.status_code = 400
                    return True, response

        if len(self.__number_arguments):
            for arg in self.__number_arguments:
                if not arg.isdigit():
                    response = jsonify({'message': f"Preencha com um valor válido o argumento 'days'"})
                    response.status_code = 400
                    return True, response

        if len(self.__city_arguments):
            for arg in self.__city_arguments:
                cities = City.select(City.id)
                list_cities = [city_db.id for city_db in cities]

                if int(arg) not in list_cities:
                    response = jsonify({'message': f"Valor do argumento 'city' não consta no banco de dados."})
                    response.status_code = 400
                    return True, response

        if len(self.__state_forecast_arguments):
            for arg in self.__state_forecast_arguments:
                states = City.select(City.state)
                list_states = [state_db.state for state_db in states]

                if arg not in list_states:
                    response = jsonify({'message': f"Valor do argumento 'state' não consta no banco de dados."})
                    response.status_code = 400
                    return True, response

        if len(self.__period_arguments):
            for arg in self.__period_arguments:
                if arg not in ['7', '14']:
                    response = jsonify({'message': f"Preencha com um valor válido o argumento 'period_day'"})
                    response.status_code = 400
                    return True, response

        return False, ''

    def set_date_argument(self, value):
        self.__date_arguments.append(value)

    def set_state_history_argument(self, value):
        self.__state_history_arguments.append(value)

    def set_state_forecast_argument(self, value):
        self.__state_forecast_arguments.append(value)

    def set_station_argument(self, value):
        self.__station_arguments.append(value)

    def set_frequency_argument(self, value):
        self.__frequency_arguments.append(value)

    def set_number_argument(self, value):
        self.__number_arguments.append(value)

    def set_city_argument(self, value):
        self.__city_arguments.append(value)

    def set_period_argument(self, value):
        self.__period_arguments.append(value)
