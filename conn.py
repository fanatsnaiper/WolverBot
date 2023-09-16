import MySQLdb as ms

class Conn:
    def __init__(self,params):
        self.host,self.port = params[0], params[1]
        self.database,self.user,self.pwd = params[2],params[3],params[4]
        self.type = params[5]
        self.connection = ms.connect(host = self.host,port = int(self.port),database = self.database,
                                     user = self.user,password = self.pwd, autocommit=True)

        self.crs = self.connection.cursor()

    def execute(self,sql):
        if self.type == 'MS':
                self.crs.execute(sql)
    def fetch_next(self):
        if self.type == 'MS':
            return self.crs.fetchone()
    def fetch_all(self):
        if self.type=='MS':
            return self.crs.fetchall()
        


def get_conn_params():
    with open('./files/config.txt') as f:
        return f.readline().split(';')

db_session= Conn(get_conn_params())