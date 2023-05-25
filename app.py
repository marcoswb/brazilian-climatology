from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from serve_data.controllers.Root import Root
from serve_data.controllers.HistoryCity import HistoryCity
from serve_data.controllers.HistoryState import HistoryState
from serve_data.controllers.HistoryAverageCity import HistoryAverageCity
from serve_data.controllers.HistoryAverageState import HistoryAverageState

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Root, '/')
api.add_resource(HistoryCity, '/history/city')
api.add_resource(HistoryState, '/history/state')
api.add_resource(HistoryAverageCity, '/history/average/city')
api.add_resource(HistoryAverageState, '/history/average/state')

if __name__ == '__main__':
    app.run()
