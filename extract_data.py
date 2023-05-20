from extract_data.process_history import ProcessHistory
from extract_data.process_forecast import ProcessForecast

update_history = False
update_forecast = True
load_counties = False
path_input = '/home/marcos/Downloads/dados_historicos'
path_output = '/home/marcos/Downloads/novos_dados'

if update_history:
    app = ProcessHistory(path_input, path_output)
    app.process_history_data()


if update_forecast:
    app = ProcessForecast(path_input, path_output)
    app.process_forecast_data(load_counties=load_counties)
