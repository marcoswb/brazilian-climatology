from extract_data.process_history import ProcessHistory
from extract_data.process_forecast import ProcessForecast
from API import API
from utils.functions import *


class Main:

    @staticmethod
    def print_options_menu():
        options = {
            '1': 'Baixar dados históricos',
            '2': 'Processar dados históricos',
            '3': 'Cadastrar dados históricos processados no banco de dados',
            '4': 'Atualizar dados de previsão do tempo',
            '5': 'Iniciar servidor da API'
        }
        print('\nMenu de opções')
        for number_option, description in options.items():
            print(f'{number_option} - {description}')

        option_user = question_user('\nSelecione uma opção para prosseguir', limit_response=list(options.keys()))
        return option_user

    def execute_task(self, option_user):
        match option_user:
            case '1':
                self.download_historical_data()
            case '2':
                self.process_historical_data()
            case '3':
                self.upload_historical_data()
            case '4':
                self.update_forecast_data()
            case '5':
                self.init_api()

    @staticmethod
    def download_historical_data():
        input_path = question_user('Informe o caminho onde os dados serão salvos', response_is_dir=True)

        valid_year = ''
        current_year = datetime.now().year
        while not valid_year:
            init_year_download = question_user('Informe o ano de início dos downloads(a partir de 2000)', int_response=True)

            if init_year_download < 2000:
                print('Informe um ano a partir de 2000')
            elif init_year_download > current_year:
                print('Informe um ano menor ou igual o ano atual')
            else:
                valid_year = init_year_download

        process = ProcessHistory(input_path)
        process.download_history_data(valid_year)

    @staticmethod
    def process_historical_data():
        input_path = question_user('Informe o caminho onde os dados históricos foram baixados', response_is_dir=True)
        output_path = question_user('Informe o caminho onde os dados processados serão salvos', response_is_dir=True)
        process = ProcessHistory(input_path, output_path)
        process.process_history_data()

    @staticmethod
    def upload_historical_data():
        output_path = question_user('Informe o caminho onde os dados históricos processados estão salvos', response_is_dir=True)
        process = ProcessHistory(output_folder=output_path)
        process.upload_data_to_database()

    @staticmethod
    def update_forecast_data():
        response_load_counties = question_user('Deseja utilizar os dados das cidades que já estão no banco de dados?(S-SIM/N-NÃO)', limit_response=['S', 'N'])

        # não carregar as cidades novamente
        load_counties = False
        if response_load_counties == 'S':
            load_counties = True

        process = ProcessForecast()
        process.process_forecast_data(load_counties=load_counties)

    @staticmethod
    def init_api():
        print('\nPressione CTRL + C para encerrar...\n')
        API().run()


if __name__ == '__main__':
    app = Main()
    option = app.print_options_menu()
    app.execute_task(option)
