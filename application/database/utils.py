from application.database.database_class import Database

TOKEN = ''
URL = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/ID_DA_CIDADE/days/15?token='
URL += TOKEN
DATABASE = Database('banco.db')


def get_database():
    return DATABASE


def get_url(city_id):
    return URL.replace('ID_DA_CIDADE', city_id)
