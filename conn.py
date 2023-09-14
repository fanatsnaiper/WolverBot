import psycopg as pg
# import mysql.connector as ms


class Conn:
    def __init__(self, params):

        self.host, self.port = params[0], params[1]
        self.dbname, self.user, self.pwd = params[2], params[3], params[4]
        self.type = params[5]
        self.connection = pg.connect(host=self.host, port=int(self.port), dbname=self.dbname,
                                     user=self.user, password=self.pwd)

        self.crs = self.connection.cursor()

    def execute(self, sql):
        if self.type == 'PG':
            self.crs.execute(sql)
            self.commit()

    def fetch_next(self):
        if self.type == 'PG':
            return self.crs.fetchone()

    def fetch_all(self):
        if self.type == 'PG':
            return self.crs.fetchall()
    def commit(self):
        self.connection.commit()


def get_conn_params():
    with open('files/config.txt') as f:
        return f.readline().split(';')


db_session = Conn(get_conn_params())