from os import listdir
from tqdm import tqdm

from utils.functions import *


process_uf = ['SC', 'RS', 'PR']


class Main:

    def __init__(self, input_folder, output_folder):
        self.__input_folder = input_folder
        self.__output_folder = output_folder
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

    def load_files_to_process(self):
        """
        Checa quais arquivos irão ser processados.
        (Processa somente arquivos da região Sul)
        """
        for folder_of_the_year in listdir(self.__input_folder):
            for file in listdir(f'{self.__input_folder}/{folder_of_the_year}'):
                complete_path = f'{self.__input_folder}/{folder_of_the_year}/{file}'
                uf_file = get_uf_file(complete_path)
                if uf_file in process_uf:
                    self.__process_files.append(complete_path)

    def process_data(self):
        """
        Lê os dados baixados, calcula as médias dos campos e
        grava as médias e arquivos originais limpos em arquivos
        txt
        """
        output_separator = getenv('OUTPUT_SEPARATOR')
        with open(f'{self.__output_folder}/output.txt', 'w', encoding=get_encoding_files()) as output_file:
            # for path_file in tqdm(self.__process_files):
            for path_file in self.__process_files:
                print(path_file)
                with open(path_file, encoding=get_encoding_files()) as readfile:
                    for index, line in enumerate(readfile.readlines()):
                        if index >= 9:
                            line = line.replace('\n', '').replace(',', '.')
                            splited_line = line.split(get_env('INPUT_SEPARATOR'))
                            data = dict(zip(self.__header_file, splited_line))

                            data['hora'] = data.get('hora').replace(' UTC', '')

                            output_file.write(f"{f'{output_separator}'.join(data.values())}\n")

                            if index == 9:
                                print(data)
                break


if __name__ == '__main__':
    app = Main('/home/marcos/Downloads/dados_historicos', '/home/marcos/Downloads/novos_dados')

    app.download_data()
    app.load_files_to_process()
    app.process_data()
