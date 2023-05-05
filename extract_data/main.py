from os import listdir
from tqdm import tqdm

from utils.functions import *
import utils.shared as shared

process_uf = ['SC', 'RS', 'PR']
max_number_files = 3


class Main:

    def __init__(self, input_folder, output_folder):
        self.__input_folder = input_folder
        self.__output_folder = output_folder
        self.__id_cities = {}
        self.__process_files = []

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

    def create_folders(self):
        """
        Cria as pastas onde os arquivos de históricos serão salvos
        """
        create_directory(f'{self.__output_folder}/original')
        create_directory(f'{self.__output_folder}/daily_averages')
        create_directory(f'{self.__output_folder}/weekly_averages')
        create_directory(f'{self.__output_folder}/monthly_averages')

    def load_cities_files(self):
        """
        Gera um arquivo txt com as estações que existem nos arquivos a serem processados
        """
        output_separator = getenv('OUTPUT_SEPARATOR')
        cities = []
        id_cities = 1
        with open(f'{self.__output_folder}/estacoes.txt', 'w', encoding=get_encoding_files()) as output_file:
            header_columns = ['id_estacao', 'estacao', 'estado', 'latitude', 'longitude']
            output_file.write(transform_line_write(header_columns))
            for path_file in self.__process_files:
                with open(path_file, encoding=get_encoding_files()) as readfile:
                    readfile.readline()

                    # ler informações do arquivo
                    uf = readfile.readline().replace('\n', '').upper()[4:]
                    estacao = readfile.readline().replace('\n', '').upper()[9:]
                    readfile.readline()
                    latitude = readfile.readline().replace('\n', '').replace(',', '.')[10:]
                    longitude = readfile.readline().replace('\n', '').replace(',', '.')[11:]

                    if (uf, estacao) not in cities:
                        line_values = [str(id_cities), estacao, uf, latitude, longitude]
                        output_file.write(transform_line_write(line_values))
                        cities.append((uf, estacao))
                        self.__id_cities[(uf, estacao)] = id_cities
                        id_cities += 1

    def process_data(self):
        """
        Lê os dados baixados, calcula as médias dos campos e
        grava as médias e arquivos originais limpos em arquivos
        txt
        """
        max_lines = int(getenv('MAX_LINES_OUTPUT_FILES'))
        number_lines = {
            'original': 1,
            'daily': 1
        }
        number_file = {
            'original': 1,
            'daily': 1
        }
        daily_average = []

        # caminhos dos arquivos
        output_path_original = f"{self.__output_folder}/original/historico_{str(number_file['original'])}.txt"
        output_path_daily = f"{self.__output_folder}/daily_averages/historico_{str(number_file['original'])}.txt"

        # arquivos para escrever
        output_file_original = open(output_path_original, 'w', encoding=get_encoding_files())
        output_file_daily = open(output_path_daily, 'w', encoding=get_encoding_files())

        # gravar cabeçalho inicial no arquivo original
        header_file = list(shared.original_header)
        header_file.extend(['id_estacao'])
        output_file_original.write(transform_line_write(header_file))

        # gravar cabeçalho inicial no arquivo de média diária
        header_file = list(shared.daily_header)
        header_file.extend(['id_estacao'])
        output_file_daily.write(transform_line_write(header_file))

        # percorrer cada arquivo que contém dados
        for path_file in tqdm(self.__process_files):
            # ler dados do arquivo original
            with open(path_file, encoding=get_encoding_files()) as readfile:
                for index, line in enumerate(readfile.readlines()):
                    if index == 1:
                        uf = line.replace('\n', '').upper()[4:]
                    elif index == 2:
                        estacao = line.replace('\n', '').upper()[9:]
                    elif index >= 9:
                        id_city = str(self.__id_cities.get((uf, estacao)))

                        # abrir arquivo de saída original
                        if number_lines['original'] > max_lines:
                            number_file['original'] += 1
                            output_path_original = f"{self.__output_folder}/original/historico_{str(number_file['original'])}.txt"
                            output_file_original.close()
                            output_file_original = open(output_path_original, 'w', encoding=get_encoding_files())
                            number_lines['original'] = 0

                            # gravar cabeçalho no arquivo original
                            header_file = list(shared.original_header)
                            header_file.extend(['id_estacao'])
                            output_file_original.write(transform_line_write(header_file))

                        # abrir arquivo de saída da média diária
                        if number_lines['daily'] > max_lines:
                            number_file['daily'] += 1
                            output_path_daily = f"{self.__output_folder}/daily_averages/historico_{str(number_file['daily'])}.txt"
                            output_file_daily.close()
                            output_file_daily = open(output_path_daily, 'w', encoding=get_encoding_files())
                            number_lines['daily'] = 0

                            # gravar cabeçalho no arquivo original
                            header_file = list(shared.daily_header)
                            header_file.extend(['id_estacao'])
                            output_file_daily.write(transform_line_write(header_file))

                        # separar os dados conforme separador
                        line = line.replace('\n', '').replace(',', '.')
                        splited_line = line.split(get_env('INPUT_SEPARATOR'))
                        data = dict(zip(shared.original_header, splited_line))

                        data['hora'] = data.get('hora').replace(' UTC', '')

                        # gravar no arquivo de saída original
                        values = list(data.values())
                        values.extend(id_city)
                        output_file_original.write(transform_line_write(values))
                        number_lines['original'] += 1

                        # gravar no arquivo de saída de médias diárias
                        average_daily_values = [data.get(key) for key in data.keys() if key not in ['data', 'hora']]
                        daily_average.append(average_daily_values)
                        if len(daily_average) == 24:
                            average_values = [data.get('data')]
                            average_values.extend(calc_average_values(daily_average))
                            average_values.append(id_city)
                            output_file_daily.write(transform_line_write(average_values))
                            number_lines['daily'] += 1
                            daily_average.clear()
                            if number_lines['daily'] == 4:
                                exit()

                if number_file['original'] == max_number_files:
                    break


if __name__ == '__main__':
    app = Main('/home/marcos/Downloads/dados_historicos', '/home/marcos/Downloads/novos_dados')

    update_history = True
    update_forecast = True

    if update_history:
        app.download_data()
        app.load_files_to_process()
        app.create_folders()
        app.load_cities_files()
        app.process_data()
