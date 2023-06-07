from dotenv import load_dotenv
from os import getenv, makedirs
from os.path import isdir
from shutil import rmtree
from datetime import datetime, timedelta, date
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
    makedirs(directory_name)


def calc_average_values(list_values):
    average = []
    sum_values = 0
    length_main_list = len(list_values)
    if len(list_values) > 0:
        length_sublists = len(list_values[0])
        for index_sublist in range(length_sublists):
            for index_main_list in range(length_main_list):
                sum_values += format_float(list_values[index_main_list][index_sublist], default_value=0)

            average.append(str(round(sum_values/length_main_list, 2)))
            sum_values = 0
        return average
    else:
        return []


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


def format_float(value, default_value=None):
    try:
        return float(value)
    except:
        return default_value


def format_int(value):
    try:
        return int(value)
    except:
        return None


def convert_date_format(date_str, date_format='%Y/%m/%d'):
    try:
        new_date = datetime.strptime(date_str, date_format)
        return new_date
    except:
        return None


def separate_date(date_str):
    converted_date = convert_date_format(date_str)
    if converted_date:
        year = converted_date.year
        month = converted_date.month
        day = converted_date.day
        return year, month, day
    else:
        return [None, None, None]


def get_competence(date_str, date_format='%d/%m/%Y', result_format='%Y/%m/%d'):
    converted_date = convert_date_format(date_str, date_format)
    if converted_date:
        competence = converted_date.replace(day=1)
        return competence.strftime(result_format)
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


def are_valid_values(*args):
    for value in args:
        if value is None:
            return False
    return True


def is_date(value, format_date='%d/%m/%Y'):
    try:
        datetime.strptime(value, format_date)
        return True
    except:
        return False


def is_valid_time(time):
    try:
        if str(time).isdigit():
            if int(time) < 0 or int(time) > 23:
                return False
            else:
                return True
        else:
            return False
    except:
        return False


def convert_time_days(value):
    """
    Processa o horário do dia solicitado
    """
    result = []
    for sublist in str(value).split(','):
        if '-' in sublist:
            range_sublist = str(sublist).split('-')
            if len(range_sublist) == 2:
                init_range = range_sublist[0]
                end_range = range_sublist[1]
                if is_valid_time(init_range) and is_valid_time(end_range):
                    range_times = range(int(init_range), int(end_range)+1)
                else:
                    return []
            else:
                return []
        else:
            range_times = [sublist]

        for time in range_times:
            if is_valid_time(time):
                result.append(int(time))
            else:
                return []

    result = list(set(result))
    result.sort()
    return result


def format_int_to_time(value):
    string_time = f'{str(value).zfill(2)}:00:00'
    # return datetime.strptime(string_time, '%H:%M:%S').time()
    return string_time


def format_str_to_date(value):
    return datetime.strptime(value, '%d/%m/%Y').date()


def get_future_day(number_of_days):
    current_day = datetime.now()
    future_day = current_day + timedelta(days=int(number_of_days))
    return future_day.strftime('%d/%m/%Y')


def get_current_day():
    current_day = datetime.now()
    return current_day.strftime('%d/%m/%Y')


def question_user(message, limit_response=None, response_is_dir=False, int_response=False):
    option = ''
    while not option:
        if limit_response:
            response = input(f'{message} => ')

            if int_response:
                response = format_int(response)

            if response in limit_response:
                option = response
            else:
                print('Informe uma opção válida!')
        elif response_is_dir:
            response = input(f'{message} => ')
            if isdir(response):
                option = response
            else:
                print('Informe um caminho válido!')
        elif int_response:
            response = input(f'{message} => ')
            if format_int(response):
                option = format_int(response)
            else:
                print('Informe um valor válido válido!')
        else:
            option = input(f'{message} => ')
            break

    return option
