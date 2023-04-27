from os import listdir
from tqdm import tqdm

from utils.functions import *


process_uf = ['SC', 'RS', 'PR']


class Main:

    def __init__(self, input_folder, output_folder):
        self.__input_folder = input_folder
        self.__output_folder = output_folder
        self.__id_cities = {}
        self.__process_files = []
        self.__header_file = ['data',
                              'hora',
                              'precipitacao',
                              'pressao_atmosferica',
                              'presao_atmosferica_maxima',
                              'pressao_atmosferica_minima',
                              'radiacao_global',
                              'temperatura_ar',
                              'temperatura_ponto_orvalho',
                              'temperatura_maxima',
                              'temperatura_minima',
                              'temperatura_orvalho_maxima',
                              'temperatura_orvalho_minima',
                              'umidade_relativa_maxima',
                              'umidade_relativa_minima',
                              'umidade_relativa_ar',
                              'direcao_horaria_ventos',
                              'velocidade_maxima_ventos',
                              'velocidade_horaria_ventos']

    @staticmethod
    def download_data():
        """
        Baixar os dados históricos do INMET
        """
        print('Baixando os dados')
        print('Baixar dados daqui: https://portal.inmet.gov.br/dadoshistoricos')

    def load_files_to_process(self):
        """
        Checa quais arquivos irão ser processados.
        (Processa somente arquivos da região Sul)
        """
        for year in listdir(self.__input_folder):
            for file in listdir(f'{self.__input_folder}/{year}'):
                complete_path = f'{self.__input_folder}/{year}/{file}'
                uf_file = get_uf_file(complete_path)
                if uf_file in process_uf:
                    self.__process_files.append(complete_path)

    def load_cities_files(self):
        """
        Gera um arquivo txt com as cidades que existem nos arquivos a serem processados
        """
        output_separator = getenv('OUTPUT_SEPARATOR')
        cities = []
        id_cities = 1
        with open(f'{self.__output_folder}/estacoes.txt', 'w', encoding=get_encoding_files()) as output_file:
            for path_file in self.__process_files:
                with open(path_file, encoding=get_encoding_files()) as readfile:
                    readfile.readline()

                    uf = readfile.readline().replace('\n', '').upper()[4:]
                    estacao = readfile.readline().replace('\n', '').upper()[9:]
                    readfile.readline()

                    latitude = readfile.readline().replace('\n', '').replace(',', '.')[10:]
                    longitude = readfile.readline().replace('\n', '').replace(',', '.')[11:]
                    if (uf, estacao) not in cities:
                        output_file.write(f'{id_cities}{output_separator}{estacao}{output_separator}{uf}{output_separator}{latitude}{output_separator}{longitude}\n')
                        cities.append((uf, estacao))
                        self.__id_cities[(uf, estacao)] = id_cities
                        id_cities += 1

    def process_data(self):
        """
        Lê os dados baixados, calcula as médias dos campos e
        grava as médias e arquivos originais limpos em arquivos
        txt
        """
        count = 0
        output_separator = getenv('OUTPUT_SEPARATOR')
        with open(f'{self.__output_folder}/historico.txt', 'w', encoding=get_encoding_files()) as output_file:
            for path_file in tqdm(self.__process_files):
                with open(path_file, encoding=get_encoding_files()) as readfile:
                    for index, line in enumerate(readfile.readlines()):
                        if index == 1:
                            uf = line.replace('\n', '').upper()[4:]
                        elif index == 2:
                            estacao = line.replace('\n', '').upper()[9:]
                        elif index >= 9:
                            id_city = self.__id_cities.get((uf, estacao))

                            line = line.replace('\n', '').replace(',', '.')
                            splited_line = line.split(get_env('INPUT_SEPARATOR'))
                            data = dict(zip(self.__header_file, splited_line))

                            data['hora'] = data.get('hora').replace(' UTC', '')

                            output_file.write(f"{f'{output_separator}'.join(data.values())}{output_separator}{id_city}\n")
                count += 1
                if count == 4:
                    break


if __name__ == '__main__':
    app = Main('/home/marcos/Downloads/dados_historicos', '/home/marcos/Downloads/novos_dados')

    # app.download_data()
    app.load_files_to_process()
    app.load_cities_files()
    app.process_data()
