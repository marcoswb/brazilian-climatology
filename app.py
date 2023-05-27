from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from serve_data.controllers.Root import Root
from serve_data.controllers.Station import Station
from serve_data.controllers.WeatherType import WeatherType
from serve_data.controllers.City import City
from serve_data.controllers.HistoryStation import HistoryStation
from serve_data.controllers.HistoryState import HistoryState
from serve_data.controllers.HistoryAverageStation import HistoryAverageStation
from serve_data.controllers.HistoryAverageState import HistoryAverageState
from serve_data.controllers.ForecastCity import ForecastCity
from serve_data.controllers.ForecastState import ForecastState
from serve_data.controllers.ForecastAverageCity import ForecastAverageCity
from serve_data.controllers.ForecastAverageState import ForecastAverageState

app = Flask(__name__)
CORS(app)

api = Api(app)

# gerais
api.add_resource(Root, '/')
api.add_resource(Station, '/station')
api.add_resource(City, '/city')
api.add_resource(WeatherType, '/weather-type')

# dados históricos
api.add_resource(HistoryStation, '/history/station')
api.add_resource(HistoryState, '/history/state')
api.add_resource(HistoryAverageStation, '/history/average/station')
api.add_resource(HistoryAverageState, '/history/average/state')

# previsão do tempo
api.add_resource(ForecastCity, '/forecast/city')
api.add_resource(ForecastState, '/forecast/state')
api.add_resource(ForecastAverageCity, '/forecast/average/city')
api.add_resource(ForecastAverageState, '/forecast/average/state')


if __name__ == '__main__':
    app.run()
