from dotenv import load_dotenv
from os import getenv, mkdir
from os.path import isdir
from shutil import rmtree
from datetime import datetime, timedelta
from collections import Counter
from multiprocessing import cpu_count


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
    for index_sublist in range(length_sublists):
        for index_main_list in range(length_main_list):
            sum_values += format_float(list_values[index_main_list][index_sublist])

        average.append(str(round(sum_values/length_main_list, 2)))
        sum_values = 0
    return average


def calc_average_values_forecast(list_values):
    average = []
    sum_values = 0
    sum_values_string = []
    length_main_list = len(list_values)
    length_sublists = len(list_values[0])
    for index_sublist in range(length_sublists):
        for index_main_list in range(length_main_list):
            if index_sublist == 0:
                sum_values_string.append(list_values[index_main_list][index_sublist])
            else:
                sum_values += format_float(list_values[index_main_list][index_sublist])

        if index_sublist == 0:
            average.append(Counter(sum_values_string).most_common(1)[0][0])
            sum_values_string.clear()
        else:
            average.append(str(round(sum_values/length_main_list, 2)))
            sum_values = 0
    return average


def format_float(value):
    try:
        return float(value)
    except:
        return 0


def convert_date_format(date, format_date='%Y/%m/%d'):
    try:
        new_date = datetime.strptime(date, format_date)
        return new_date
    except:
        return None


def separate_date(date):
    converted_date = convert_date_format(date)
    if converted_date:
        year = converted_date.year
        month = converted_date.month
        day = converted_date.day
        return year, month, day
    else:
        return [None, None, None]


def get_competence(date):
    converted_date = convert_date_format(date)
    if converted_date:
        competence = converted_date.replace(day=1)
        return competence.strftime('%Y/%m/%d')
    else:
        return None


def get_month(str_date):
    converted_date = convert_date_format(str_date)
    if converted_date:
        return str(converted_date.month)
    else:
        return ''


def get_day(str_date):
    converted_date = convert_date_format(str_date)
    if converted_date:
        return str(converted_date.day)
    else:
        return ''


def get_first_and_last_day_week(str_date):
    converted_date = convert_date_format(str_date)
    number_days = timedelta(days=converted_date.weekday() + 1)

    if number_days.days == 7:
        start = converted_date
        end = start + timedelta(days=6)
    else:
        start = converted_date - timedelta(days=converted_date.weekday() + 1)
        end = start + timedelta(days=6)

    return str(start.strftime('%Y/%m/%d')), str(end.strftime('%Y/%m/%d'))


def get_number_free_threads():
    """
    Retorna a metade da quantidade de theads disponíveis na maquina
    """
    try:
        return cpu_count()/2
    except:
        return 1
