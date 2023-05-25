from extract_data.process_history import ProcessHistory
from extract_data.process_forecast import ProcessForecast

download_data_history = False
init_year_download = '2020'
update_history = False
upload_data_history = True
update_forecast = False
load_counties = True
path_input = '/home/marcos/Downloads/download_files'
path_output = '/home/marcos/Downloads/novos_dados'

if update_history or upload_data_history or download_data_history:
    app = ProcessHistory(path_input, path_output)
    if download_data_history:
        app.download_history_data(init_year_download)
    if update_history:
        app.process_history_data()
    if upload_data_history:
        app.upload_data_to_database()


if update_forecast:
    app = ProcessForecast(path_input, path_output)
    app.process_forecast_data(load_counties=load_counties)
