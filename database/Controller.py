import psycopg2
from os.path import isfile
import os
import subprocess

from utils.functions import *


class ControllerDatabase:
    def restore(self, database):
        if isfile(database):
            self.create_database()

            print('Restaurando banco de dados')
            os.environ['PGPASSWORD'] = get_env('DATABASE_PASSWORD')
            pg_restore_cmd = [
                "pg_restore",
                "-h", get_env('DATABASE_HOST'),
                "-p", get_env('DATABASE_PORT'),
                "-U", get_env('DATABASE_USER'),
                "-d", get_env('DATABASE_NAME'),
                "-Fc", database
            ]

            try:
                subprocess.run(pg_restore_cmd, check=True)
                print("Banco de dados restaurado com sucesso!")
            except subprocess.CalledProcessError as e:
                print("Erro ao restaurar o banco de dados:", e)

    @staticmethod
    def create_database():
        conn = psycopg2.connect(
            host=get_env('DATABASE_HOST'),
            port=get_env('DATABASE_PORT'),
            user=get_env('DATABASE_USER'),
            password=get_env('DATABASE_PASSWORD'),
            database="postgres"
        )

        conn.autocommit = True
        cursor = conn.cursor()
        create_database_query = f"CREATE DATABASE {get_env('DATABASE_NAME')};"
        cursor.execute(create_database_query)
