from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from os import listdir, rmdir
from tqdm import tqdm
import requests
from shutil import unpack_archive, move

from utils.functions import *
import utils.shared as shared
from database.Postgre import *


class ProcessHistory:

    def __init__(self, input_folder='', output_folder='', process_uf=None):
        self.__input_folder = input_folder
        self.__output_folder = output_folder
        self.__id_cities = {}
        self.__process_files = []
        self.data = {}

        if not process_uf:
            self.__process_uf = shared.uf_estados
        else:
            self.__process_uf = process_uf

    @staticmethod
    def get_links_to_download(init_year_download):
        """
        Buscar links para realizar o download
        """
        # Opção para executar o navegador no modo oculto
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # baixar driver compatível
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # buscar elemento principal da paǵina
        print('acessando a página de download')
        driver.get('https://portal.inmet.gov.br/dadoshistoricos')
        element = driver.find_element('css selector', '.cold-lg-12')

        # guardar os anos disponíveis e o link para download
        print('coletando os links para download')
        download_data = {}
        year_elements = element.find_elements('css selector', '.post-preview')
        for year_element in year_elements:
            link_element = year_element.find_element('css selector', 'a')
            year = str(link_element.text).split(' ')[1]
            link_download = link_element.get_attribute('href')

            # não baixa se for um ano anterior ao solicitado
            if int(year) >= int(init_year_download):
                download_data[year] = link_download

        driver.quit()

        return download_data

    @staticmethod
    def download_file(link, output_file):
        """
        Baixa um arquivo para um caminho específico
        """
        response = requests.get(link, stream=True)
        if response.status_code == 200:
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

    def download_data(self, init_year_download):
        """
        Baixar os dados históricos do INMET
        """
        create_directory(self.__input_folder)
        links_to_download = self.get_links_to_download(init_year_download)

        # baixa os arquivos no caminho especificado
        print('Baixando os arquivos')
        count = 0
        total_files = len(links_to_download.values())
        for year, link in links_to_download.items():
            self.download_file(link, f'{self.__input_folder}/{year}.zip')
            count += 1
            print(f'Arquivo {count} de {total_files}')

        # descompactar os arquivos baixados
        print('Descompactando os arquivos')
        count = 0
        files = listdir(self.__input_folder)
        total_files = len(files)
        for file in files:
            folder = str(file).replace('.zip', '')
            unpack_archive(f'{self.__input_folder}/{file}', f'{self.__input_folder}/{folder}')

            # as vezes os arquivos vem soltos e as vezes vem dentro da uma outra pasta
            # aqui movemos caso eles venham dentro de outra pasta
            if isdir(f'{self.__input_folder}/{folder}/{folder}'):
                for file_csv in listdir(f'{self.__input_folder}/{folder}/{folder}'):
                    move(f'{self.__input_folder}/{folder}/{folder}/{file_csv}', f'{self.__input_folder}/{folder}/{file_csv}')
                rmdir(f'{self.__input_folder}/{folder}/{folder}')

            count += 1
            print(f'Arquivo {count} de {total_files}')

    def load_files_to_process(self):
        """
        Checa quais arquivos irão ser processados.
        """
        for year in listdir(self.__input_folder):
            if isdir(f'{self.__input_folder}/{year}'):
                for file in listdir(f'{self.__input_folder}/{year}'):
                    complete_path = f'{self.__input_folder}/{year}/{file}'
                    uf_file = get_uf_file(complete_path)
                    if uf_file in self.__process_uf:
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
        old_day = ''
        old_first_day_week = ''
        old_competence = ''
        old_date = ''
        old_city = ''
        self.data = {
            'number_lines': {
                'original': 1,
                'daily': 1,
                'weekly': 1,
                'monthly': 1
            },
            'number_file': {
                'original': 1,
                'daily': 1,
                'weekly': 1,
                'monthly': 1
            },
            'daily_average': [],
            'weekly_average': [],
            'monthly_average': []
        }

        # caminhos dos arquivos
        output_path_original = self.get_name_file('original')
        output_path_daily = self.get_name_file('daily')
        output_path_weekly = self.get_name_file('weekly')
        output_path_monthly = self.get_name_file('monthly')

        # arquivos para escrever
        output_file_original = open(output_path_original, 'w', encoding=get_encoding_files())
        output_file_daily = open(output_path_daily, 'w', encoding=get_encoding_files())
        output_file_weekly = open(output_path_weekly, 'w', encoding=get_encoding_files())
        output_file_monthly = open(output_path_monthly, 'w', encoding=get_encoding_files())

        # gravar cabeçalhos
        self.print_header('original', output_file_original)
        self.print_header('daily', output_file_daily)
        self.print_header('weekly', output_file_weekly)
        self.print_header('monthly', output_file_monthly)

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

                        # abrir arquivo de saída original e gravar cabeçalho
                        if self.data.get('number_lines').get('original') > max_lines:
                            self.data['number_file']['original'] += 1
                            self.data['number_lines']['original'] = 0
                            output_file_original.close()
                            output_file_original = open(self.get_name_file('original'), 'w', encoding=get_encoding_files())
                            self.print_header('original', output_file_original)

                        # abrir arquivo de saída da média diária e gravar cabeçalho
                        if self.data.get('number_lines').get('daily') > max_lines:
                            self.data['number_file']['daily'] += 1
                            self.data['number_lines']['daily'] = 0
                            output_file_daily.close()
                            output_file_daily = open(self.get_name_file('daily'), 'w', encoding=get_encoding_files())
                            self.print_header('daily', output_file_daily)

                        # abrir arquivo de saída da média semanal e gravar cabeçalho
                        if self.data.get('number_lines').get('weekly') > max_lines:
                            self.data['number_file']['weekly'] += 1
                            self.data['number_lines']['weekly'] = 0
                            output_file_weekly.close()
                            output_file_weekly = open(self.get_name_file('weekly'), 'w', encoding=get_encoding_files())
                            self.print_header('weekly', output_file_weekly)

                        # abrir arquivo de saída da média mensal e gravar cabeçalho
                        if self.data.get('number_lines').get('monthly') > max_lines:
                            self.data['number_file']['monthly'] += 1
                            self.data['number_lines']['monthly'] = 0
                            output_file_monthly.close()
                            output_file_monthly = open(self.get_name_file('monthly'), 'w', encoding=get_encoding_files())
                            self.print_header('monthly', output_file_monthly)

                        # separar os dados conforme separador
                        original_line = line.replace('\n', '').replace(',', '.')
                        splited_line = original_line.split(get_env('INPUT_SEPARATOR'))
                        line = dict(zip(shared.original_header, splited_line))
                        line['hora'] = line.get('hora').replace(' UTC', '')

                        # iniciar variavel do dia
                        day = get_day(line.get('data'))
                        if not old_day:
                            old_day = str(day)

                        # iniciar variáveis da semana
                        first_day_week, last_day_week = get_first_and_last_day_week(line.get('data'))
                        if not old_first_day_week:
                            old_first_day_week = str(first_day_week)

                        # iniciar variavel do mês
                        competence = get_competence(line.get('data'), date_format='%Y/%m/%d')
                        if not old_competence:
                            old_competence = str(competence)

                        # iniciar variavel do código da cidade
                        if not old_city:
                            old_city = str(id_city)

                        # gravar no arquivo de saída os dados originais
                        values = list(line.values())
                        values.append(id_city)
                        output_file_original.write(transform_line_write(values))
                        self.data['number_lines']['original'] += 1

                        # limpar tudo se mudar de cidade
                        if id_city != old_city:

                            # diário
                            if self.data['daily_average']:
                                average_values = calc_average_values(self.data['daily_average'])
                                write_values = [old_date]
                                write_values.extend(average_values)
                                write_values.append(old_city)
                                output_file_daily.write(transform_line_write(write_values))
                                self.data['number_lines']['daily'] += 1
                                self.data['daily_average'].clear()

                                # salvar média diária já calculada para calcular a média semanal
                                self.data['weekly_average'].append(average_values)

                                # salvar média diária já calculada para calcular a média mensal
                                self.data['monthly_average'].append(average_values)

                            # semanal
                            if self.data['weekly_average']:
                                write_values = [old_first_day_week, old_date]
                                write_values.extend(calc_average_values(self.data['weekly_average']))
                                write_values.append(old_city)
                                output_file_weekly.write(transform_line_write(write_values))
                                self.data['number_lines']['weekly'] += 1
                                self.data['weekly_average'].clear()

                            # mensal
                            if self.data['monthly_average']:
                                average_values = [old_competence]
                                average_values.extend(calc_average_values(self.data['monthly_average']))
                                average_values.append(old_city)
                                output_file_monthly.write(transform_line_write(average_values))
                                self.data['number_lines']['monthly'] += 1
                                self.data['monthly_average'].clear()
                        else:
                            # média diária
                            if day != old_day:
                                average_values = calc_average_values(self.data['daily_average'])
                                write_values = [old_date]
                                write_values.extend(average_values)
                                write_values.append(old_city)
                                output_file_daily.write(transform_line_write(write_values))
                                self.data['number_lines']['daily'] += 1
                                self.data['daily_average'].clear()

                                # salvar média diária já calculada para calcular a média semanal
                                self.data['weekly_average'].append(average_values)

                                # salvar média diária já calculada para calcular a média mensal
                                self.data['monthly_average'].append(average_values)

                            # média semanal
                            if first_day_week != old_first_day_week:

                                write_values = [old_first_day_week, old_date]
                                average_calc = calc_average_values(self.data['weekly_average'])
                                if average_calc:
                                    write_values.extend(average_calc)
                                    write_values.append(old_city)
                                    output_file_weekly.write(transform_line_write(write_values))
                                    self.data['number_lines']['weekly'] += 1
                                    self.data['weekly_average'].clear()

                            # média mensal
                            if old_competence != competence:
                                average_calc = calc_average_values(self.data['monthly_average'])
                                if average_calc:
                                    average_values = [old_competence]
                                    average_values.extend(average_calc)
                                    average_values.append(old_city)
                                    output_file_monthly.write(transform_line_write(average_values))
                                    self.data['number_lines']['monthly'] += 1
                                    self.data['monthly_average'].clear()

                        # salvar dados para médias diárias
                        values_to_average = [line.get(key) for key in line.keys() if key not in ['data', 'hora']]
                        self.data['daily_average'].append(values_to_average)

                        # salvar dados do registro
                        old_day = str(day)
                        old_first_day_week = str(first_day_week)
                        old_competence = str(competence)
                        old_date = str(line.get('data'))
                        old_city = str(id_city)

    @staticmethod
    def print_header(type_file, object_write):
        if type_file == 'daily':
            header = list(shared.daily_header)
        elif type_file == 'weekly':
            header = list(shared.weekly_header)
        elif type_file == 'monthly':
            header = list(shared.monthly_header)
        else:
            header = list(shared.original_header)

        header.extend(['id_estacao'])
        object_write.write(transform_line_write(header))

    def get_name_file(self, type_file):
        if type_file == 'daily':
            number_file = str(self.data.get('number_file').get('daily'))
            filename = f"{self.__output_folder}/daily_averages/historico_{number_file}.txt"
        elif type_file == 'weekly':
            number_file = str(self.data.get('number_file').get('weekly'))
            filename = f"{self.__output_folder}/weekly_averages/historico_{number_file}.txt"
        elif type_file == 'monthly':
            number_file = str(self.data.get('number_file').get('monthly'))
            filename = f"{self.__output_folder}/monthly_averages/historico_{number_file}.txt"
        else:
            number_file = str(self.data.get('number_file').get('original'))
            filename = f"{self.__output_folder}/original/historico_{number_file}.txt"

        return filename

    def upload_station_data(self):
        """
        Gravar no banco os dados das estações
        """
        # limpar tabela de estações
        Station().init()

        with open(f'{self.__output_folder}/estacoes.txt', encoding=get_encoding_files()) as station_file:
            for index, line_file in enumerate(station_file.readlines()):
                splited_line = line_file.replace('\n', '').split(get_env('OUTPUT_SEPARATOR'))
                if index == 0:
                    header = list(splited_line)
                else:
                    line = dict(zip(header, splited_line))
                    Station.create(
                        id_station=line.get('id_estacao'),
                        name_station=line.get('estacao'),
                        state=line.get('estado'),
                        latitude=line.get('latitude'),
                        longitude=line.get('longitude')
                    )

    def upload_data_history(self):
        """
        Gravar no banco os dados dos históricos
        """
        # limpar tabela de dados históricos
        History().init()

        base_path = f'{self.__output_folder}/original'
        for file in tqdm(listdir(base_path)):
            temp_data = []
            with open(f'{base_path}/{file}', encoding=get_encoding_files()) as history_file:
                for index, line_file in enumerate(history_file.readlines()):
                    if index != 0:
                        splited_line = line_file.replace('\n', '').split(get_env('OUTPUT_SEPARATOR'))
                        formated_values = splited_line[:2]
                        for value in splited_line[2:-1]:
                            formated_values.append(format_float(value))
                        formated_values.append(splited_line[-1])
                        temp_data.append(formated_values)

                # inserir os dados em lote
                History.insert_many(temp_data).execute()
                temp_data.clear()

    def upload_data_daily_average_history(self):
        """
        Gravar no banco os dados do histórico de médias diárias
        """
        # limpar tabela de dados históricos
        DailyAverageHistory().init()

        base_path = f'{self.__output_folder}/daily_averages'
        for file in tqdm(listdir(base_path)):
            temp_data = []
            with open(f'{base_path}/{file}', encoding=get_encoding_files()) as history_file:
                for index, line_file in enumerate(history_file.readlines()):
                    if index != 0:
                        splited_line = line_file.replace('\n', '').split(get_env('OUTPUT_SEPARATOR'))
                        formated_values = splited_line[:2]
                        for value in splited_line[2:-1]:
                            formated_values.append(format_float(value))
                        formated_values.append(splited_line[-1])
                        temp_data.append(formated_values)

                # inserir os dados em lote
                DailyAverageHistory.insert_many(temp_data).execute()
                temp_data.clear()

    def upload_data_weekly_average_history(self):
        """
        Gravar no banco os dados do histórico de médias semanais
        """
        # limpar tabela de dados históricos
        WeeklyAverageHistory().init()

        base_path = f'{self.__output_folder}/weekly_averages'
        for file in tqdm(listdir(base_path)):
            temp_data = []
            with open(f'{base_path}/{file}', encoding=get_encoding_files()) as history_file:
                for index, line_file in enumerate(history_file.readlines()):
                    if index != 0:
                        splited_line = line_file.replace('\n', '').split(get_env('OUTPUT_SEPARATOR'))
                        formated_values = splited_line[:2]
                        for value in splited_line[2:-1]:
                            formated_values.append(format_float(value))
                        formated_values.append(splited_line[-1])
                        temp_data.append(formated_values)

                # inserir os dados em lote
                WeeklyAverageHistory.insert_many(temp_data).execute()
                temp_data.clear()

    def upload_data_monthly_average_history(self):
        """
        Gravar no banco os dados do histórico de médias mensais
        """
        # limpar tabela de dados históricos
        MonthlyAverageHistory().init()

        base_path = f'{self.__output_folder}/monthly_averages'
        for file in tqdm(listdir(base_path)):
            temp_data = []
            with open(f'{base_path}/{file}', encoding=get_encoding_files()) as history_file:
                for index, line_file in enumerate(history_file.readlines()):
                    if index != 0:
                        splited_line = line_file.replace('\n', '').split(get_env('OUTPUT_SEPARATOR'))
                        formated_values = splited_line[:2]
                        for value in splited_line[2:-1]:
                            formated_values.append(format_float(value))
                        formated_values.append(splited_line[-1])
                        temp_data.append(formated_values)

                # inserir os dados em lote
                MonthlyAverageHistory.insert_many(temp_data).execute()
                temp_data.clear()

    def download_history_data(self, init_year_download):
        self.download_data(init_year_download)

    def process_history_data(self):
        """
        Processar dados históricos
        """
        self.load_files_to_process()
        self.create_folders()
        self.load_cities_files()
        self.process_data()

    def upload_data_to_database(self):
        """
        Uppar dados para o banco de dados
        """
        self.upload_station_data()
        self.upload_data_history()
        self.upload_data_daily_average_history()
        self.upload_data_weekly_average_history()
        self.upload_data_monthly_average_history()
