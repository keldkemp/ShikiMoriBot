"""
Класс для работы с БД PG
"""
import psycopg2
from psycopg2 import Error
from abc import ABC


class DataBaseStandart(ABC):
    CONN = None

    @classmethod
    def create_tables(cls, command: str):
        pass


class DataBasePg(DataBaseStandart):

    def select_all(self, table_name: str):
        self.conn_open_close(1)
        c = self.CONN.cursor()
        c.execute(f'SELECT * FROM {table_name}')
        result = c.fetchall()
        c.close()
        return result

    def select(self, command):
        self.conn_open_close(1)
        c = self.CONN.cursor()
        c.execute(command)
        result = c.fetchall()
        c.close()
        return result

    def insert_init(self, command):
        self.conn_open_close(1)
        try:
            c = self.CONN.cursor()
            c.execute(command)
            self.CONN.commit()
            c.close()
        except Error as e:
            pass

    def migration(self, command):
        self.conn_open_close(1)
        c = self.CONN.cursor()
        c.execute(command)
        self.CONN.commit()
        c.close()

    def create_tables(self, command):
        self.conn_open_close(1)
        try:
            c = self.CONN.cursor()
            c.execute(command)
            self.CONN.commit()
            c.close()
        except Error as e:
            pass

    def conn_open_close(self, stat):
        if stat == 1:
            self.CONN = psycopg2.connect(dbname=self.__dbname, user=self.__user,
                                         password=self.__password, host=self.__host,
                                         port=self.__port)
        else:
            self.CONN.close()

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int,
                 create_tables: str = None, init_date: str = None):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    def __del__(self):
        self.conn_open_close(0)
