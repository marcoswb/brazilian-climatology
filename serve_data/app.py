from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from source.controllers.Root import Root

app = Flask(__name__)
CORS(app)

api = Api(app)

api.add_resource(Root, '/')
api.add_resource(Root, '/history')
api.add_resource(Root, '/forecast')

if __name__ == '__main__':
    app.run()
