import requests
import xmltodict
from tqdm import tqdm

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
        result_data = []

        # previsão dos próximos 7 dias
        for latitude_float, longitude_float, id_city in cities:
            latitude = format(latitude_float, '.2f')
            longitude = format(longitude_float, '.2f')
            result_xml = requests.get(f"{get_env('BASE_URL_CPTEC')}/cidade/7dias/{latitude}/{longitude}/previsaoLatLon.xml").text
            data = xmltodict.parse(result_xml)

            for line in data.get('cidade').get('previsao'):
                data_append = list(line.values())
                data_append.append(id_city)
                result_data.append(data_append)

        # previsão dos 7 dias posteriores
        for latitude_float, longitude_float, id_city in cities:
            latitude = str(latitude_float).format('.2f')
            longitude = str(longitude_float).format('.2f')
            result_xml = requests.get(f"{get_env('BASE_URL_CPTEC')}/cidade/{latitude}/{longitude}/estendidaLatLon.xml").text
            data = xmltodict.parse(result_xml)

            for line in data.get('cidade').get('previsao'):
                data_append = list(line.values())
                data_append.append('')
                data_append.append(id_city)
                result_data.append(data_append)

        return result_data

    def process_forecast_data(self, load_counties=True):
        """
        Processar dados de previsão do tempo
        """
        if not load_counties:
            self.get_cities_uf()
            self.get_cities_forecast()

        data = self.get_data_forecast_cities()
        print(data)
