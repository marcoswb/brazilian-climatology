import requests
import xmltodict
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from utils.functions import *
from classes.CustomHttpAdapter import get_legacy_session
from database.Postgre import *

process_uf = ['SC', 'RS', 'PR']
max_number_files = 2


class ProcessForecast:

    def __init__(self, input_folder, output_folder):
        self.__input_folder = input_folder
        self.__output_folder = output_folder
        self.__id_cities = {}
        self.__process_files = []
        self.data = {}
        self.number_threads = 5

    @staticmethod
    def get_cities_uf():
        """
        Buscar a lista de municipios que cada estado possui
        """
        # limpar tabela de cidades
        City().init()

        # busca todas as cidades do estado com base na API do IBGE
        for uf in process_uf:
            response = get_legacy_session().get(f"{get_env('BASE_URL_IBGE')}/localidades/estados/{uf}/distritos")
            for line in response.json():
                city = line.get('nome')

                # salvar o registro no banco de dados
                register = City(city=city, state=uf)
                register.save()

    @staticmethod
    def get_cities_forecast():
        """
        Buscar latitude e longitude das cidades
        """
        # Limpar tabela de posições
        PositionCity().init()

        # extrair latitudes e longitudes da API do Google Maps
        result = City().select().dicts()
        for line in tqdm(result):
            id_city = line.get('id')
            city = line.get('city')
            state = line.get('state')

            params = {
                'address': f'{city}, {state}',
                'key': get_env('API_KEY_GEOCODING')
            }

            response = requests.get(get_env('BASE_URL_GEOCODING'), params=params)
            data = response.json()

            # Extrair a latitude e longitude da resposta da API
            if data['status'] == 'OK':
                result = data['results'][0]
                location = result['geometry']['location']
                latitude = format(location['lat'], '.2f')
                longitude = format(location['lng'], '.2f')

                # salvar o registro no banco de dados
                register = PositionCity(latitude=latitude, longitude=longitude, id_city=id_city)
                register.save()

    def get_data_forecast_cities(self):
        """
        Buscar dados de previsão do tempo das cidades
        """
        # Divide a lista em listas menores para serem processadas paralelamente
        result = PositionCity().select().order_by(PositionCity.id_city).dicts()
        data = self.split_data_process(result)

        # limpar tabela de previsão de tempo
        Forecast().init()

        # previsão dos próximos 7 dias
        executor = ThreadPoolExecutor()
        results = [executor.submit(self.get_forecast_last_seven_days, sublist) for sublist in data]
        for future in tqdm(results):
            future.result()

        # previsão estendida de mais 7 dias
        executor = ThreadPoolExecutor()
        results = [executor.submit(self.get_extended_forecast, sublist) for sublist in data]
        for future in tqdm(results):
            future.result()

    @staticmethod
    def get_forecast_last_seven_days(data):
        for line in tqdm(data, leave=True):
            latitude = str(line.get('latitude')).replace('-', '')
            longitude = str(line.get('longitude')).replace('-', '')
            id_city = line.get('id_city')

            # fazer a requisição
            result_xml = requests.get(f"{get_env('BASE_URL_CPTEC')}/cidade/7dias/-{latitude}/-{longitude}/previsaoLatLon.xml").text
            data = xmltodict.parse(result_xml)

            for forecast_line in data.get('cidade').get('previsao'):
                # salvar o registro no banco de dados
                register = Forecast(
                    day=forecast_line.get('dia'),
                    weather_condition=forecast_line.get('tempo'),
                    maximum_temperature=forecast_line.get('maxima'),
                    minimum_temperature=forecast_line.get('minima'),
                    ultra_violet_index=forecast_line.get('iuv'),
                    id_city=id_city)
                register.save()

    @staticmethod
    def get_extended_forecast(data):
        for line in tqdm(data, leave=True):
            latitude = str(line.get('latitude')).replace('-', '')
            longitude = str(line.get('longitude')).replace('-', '')
            id_city = line.get('id_city')

            # fazer a requisição
            result_xml = requests.get(f"{get_env('BASE_URL_CPTEC')}/cidade/{latitude}/{longitude}/estendidaLatLon.xml").text
            data = xmltodict.parse(result_xml)

            for forecast_line in data.get('cidade').get('previsao'):
                # salvar o registro no banco de dados
                register = Forecast(
                    day=forecast_line.get('dia'),
                    weather_condition=forecast_line.get('tempo'),
                    maximum_temperature=forecast_line.get('maxima'),
                    minimum_temperature=forecast_line.get('minima'),
                    ultra_violet_index=forecast_line.get('iuv'),
                    id_city=id_city)
                register.save()

    def split_data_process(self, data):
        """
        Separa os dados em listas menores conforme o numero de threads disponíveis para processar
        """
        len_sublists = int((len(data)) / self.number_threads)
        new_data = [data[i:i + len_sublists] for i in range(0, len(data), len_sublists)]

        return new_data

    def process_forecast_data(self, load_counties=True):
        """
        Processar dados de previsão do tempo
        """
        if not load_counties:
            self.get_cities_uf()
            self.get_cities_forecast()

        self.get_data_forecast_cities()
