from flask_restful import Resource
from flask import jsonify, request, Response


class HistoryState(Resource):

    @staticmethod
    def get():
        args = request.args
        year = args.get('year')
        month = args.get('month')

        if year is not None:
            if month is not None:
                result = {'message': f'Pesquisar pelo ano {year} e mês {month}'}
            else:
                result = {'message': f'Pesquisar pelo ano {year}'}

            return jsonify(result)
        else:
            return Response("{'status': 'Unprocessable_Content'}", status=422, mimetype='application/json')
