import os
import sqlite3

DIR_SEP = os.path.sep
DATABASE_PATH = 'application{}database{}'.format(DIR_SEP, DIR_SEP)


class Database:
    def __init__(self, name):
        self.name = DATABASE_PATH+name

        self.create_tables()

    def __str__(self):
        return self.name.split(DIR_SEP)[-1]

    def create_tables(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''create table if not exists cidades
                          (id integer primary key autoincrement,
                           cidade text,
                           estado text,
                           pais text,
                           unique (cidade, estado, pais))''')

        cursor.execute('''create table if not exists clima
                          (data text,
                           probabilidade real,
                           precipitacao real,
                           maxima real,
                           minima real,
                           cidade_id integer,
                           foreign key (cidade_id) references cidades(id),
                           unique (data, cidade_id))''')

        conn.commit()
        conn.close()

    def insert_city(self, city, state, country):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''insert or ignore into cidades
                          (cidade, estado, pais) values
                          (?, ?, ?)''',
                       (city, state, country))

        cursor.execute('''select id from cidades
                          where cidade=? and estado=? and pais=?''',
                       (city, state, country))

        city_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return city_id

    def insert_clima(self, *args, **kwargs):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        conn.execute('pragma foreign_keys = 1')

        cursor.execute('''replace into clima
                          (data, probabilidade, precipitacao,
                           maxima, minima, cidade_id)
                          values (?, ?, ?, ?, ?, ?)''', args)

        conn.commit()
        conn.close()

    def insert_information(self, data):
        self.create_tables()

        city_id = self.insert_city(data['name'],
                                   data['state'],
                                   data['country'])

        for day in data['data']:
            self.insert_clima(day['date'],
                              day['rain']['probability'],
                              day['rain']['precipitation'],
                              day['temperature']['max'],
                              day['temperature']['min'],
                              city_id)

    def get_hottest_city(self, data_inicial, data_final):
        self.create_tables()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''select cidades.cidade, max(clima.maxima) from
                          clima join cidades on clima.cidade_id = cidades.id
                          where data between Date(?) and Date(?)''',
                       (data_inicial, data_final))

        cidade = cursor.fetchone()[0]

        conn.close()

        return cidade

    def get_average_precipitation(self, data_inicial, data_final):
        self.create_tables()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''select cidades.cidade, round(avg(precipitacao), 2)
                          from clima join cidades on
                          clima.cidade_id = cidades.id
                          where data between Date(?) and Date(?)
                          group by cidade_id''',
                       (data_inicial, data_final))

        result = {r[0]: r[1] for r in cursor.fetchall()}

        conn.close()

        return result
