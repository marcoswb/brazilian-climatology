from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from serve_data.controllers.Root import Root
from serve_data.controllers.Station import Station
from serve_data.controllers.HistoryStation import HistoryStation
from serve_data.controllers.HistoryState import HistoryState
from serve_data.controllers.HistoryAverageStation import HistoryAverageStation
from serve_data.controllers.HistoryAverageState import HistoryAverageState

app = Flask(__name__)
CORS(app)

api = Api(app)

# gerais
api.add_resource(Root, '/')
api.add_resource(Station, '/station')

# dados históricos
api.add_resource(HistoryStation, '/history/station')
api.add_resource(HistoryState, '/history/state')
api.add_resource(HistoryAverageStation, '/history/average/station')
api.add_resource(HistoryAverageState, '/history/average/state')


if __name__ == '__main__':
    app.run()
