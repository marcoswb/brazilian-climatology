from dotenv import load_dotenv
from os import getenv


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
