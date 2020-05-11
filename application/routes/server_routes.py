import requests
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from application.server import api
from application.database.utils import get_database, get_url


class Cidade(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help='Id da cidade', required=True)

        args = parser.parse_args()

        status = self._previsao_tempo(args.id)

        result = {'status': status}

        if status == 200:
            msg = 'Dados inseridos com sucesso'

        else:
            msg = 'Erro na inserção dos dados'

        result['msg'] = msg

        return jsonify(result)

    def _previsao_tempo(self, city_id):
        url = get_url(city_id)
        page = requests.get(url)

        status = page.status_code

        if page.status_code == 200:
            database = get_database()
            database.insert_information(page.json())

        return status


class Analise(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data_inicial',
                            help='Data inicial da analise no '
                                 'formato AAAA-MM-DD',
                            required=True)
        parser.add_argument('data_final',
                            help='Data final da analise no formato AAAA-MM-DD',
                            required=True)

        args = parser.parse_args()

        try:
            resp = self._analise_database(args.data_inicial, args.data_final)

        except Exception as e:
            resp = {
                'msg': str(e),
                'status': 400
            }

        return jsonify(resp)

    def _analise_database(self, data_inicial, data_final):
        initial_date = datetime.strptime(data_inicial, '%Y-%m-%d')
        final_date = datetime.strptime(data_final, '%Y-%m-%d')

        result = {}

        if initial_date <= final_date:
            database = get_database()

            cidade = database.get_hottest_city(data_inicial, data_final)
            precipitacao_media = database.get_average_precipitation(data_inicial, data_final)

            result['cidade'] = cidade
            result['precipitacao'] = precipitacao_media
            result['status'] = 200

        else:
            raise Exception('Data final menor que data inicial')

        return result


def init_routes():
    api.add_resource(Cidade, '/cidade')
    api.add_resource(Analise, '/analise')
