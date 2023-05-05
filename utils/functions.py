from dotenv import load_dotenv
from os import getenv, mkdir
from os.path import isdir
from shutil import rmtree


def get_uf_file(path_file):
    """
    Retorna a UF a qual um arquivo é referente
    """
    with open(path_file, encoding=get_encoding_files()) as readfile:
        readfile.readline()
        line = readfile.readline().replace('\n', '')
        uf_file = line[-2:]

    return uf_file


def get_encoding_files():
    load_dotenv()
    default_encoding = getenv('DEFAULT_ENCODING')
    return default_encoding


def get_env(env_name):
    load_dotenv()
    default_encoding = getenv(env_name)
    return default_encoding


def transform_line_write(list_values):
    output_separator = getenv('OUTPUT_SEPARATOR')
    line_write = f'{output_separator}'.join(list_values)
    line_write += '\n'
    return line_write


def create_directory(directory_name):
    if isdir(directory_name):
        rmtree(directory_name)
    mkdir(directory_name)


def calc_average_values(list_values):
    average = []
    sum_values = 0
    length_main_list = len(list_values)
    length_sublists = len(list_values[0])
    print('\n')
    for i in list_values:
        print(i)
    for index_sublist in range(length_sublists):
        for index_main_list in range(length_main_list):
            sum_values += format_float(list_values[index_main_list][index_sublist])

        average.append(str(round(sum_values/length_main_list, 2)))
        sum_values = 0
    return average


def format_float(value):
    try:
        return float(value)
    except:
        return 0
