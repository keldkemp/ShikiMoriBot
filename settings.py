"""
Классы для работы с настройками проекта.
Настройки берутся из файла
"""
import json
import os
import urllib.parse as urlparse
from abc import ABC


# Абстрактный класс по работе с настройками
class Settings(ABC):
    __FILE_NAME = 'settings1.json'

    def __read_file(self) -> json:
        f = open(self.__FILE_NAME)
        str = f.read()
        f.close()
        return json.loads(str)

    def __read_env(self) -> json:
        dc = {}
        dc['telegram_token'] = os.environ['telegram_token']
        if os.environ.get('db_name') is not None:
            dc['db_name'] = os.environ['db_name']
            dc['db_user'] = os.environ['db_user']
            dc['db_password'] = os.environ['db_password']
            dc['port'] = os.environ['db_port']
            dc['host'] = os.environ['host']
        else:
            url_db = urlparse.urlparse(os.environ['DATABASE_URL'])
            dc['db_name'] = url_db.path[1:]
            dc['db_user'] =url_db.username
            dc['db_password'] = url_db.password
            dc['host'] = url_db.hostname
            dc['port'] = url_db.port
        dc['client_id'] = os.environ['client_id']
        dc['client_secret'] = os.environ['client_secret']
        dc['client_name'] = os.environ['client_name']
        return dc

    def __init__(self):
        json_settings = self.__read_file() if os.path.exists(self.__FILE_NAME) else self.__read_env()
        self._token = json_settings['telegram_token']
        self._db_name = json_settings['db_name']
        self._db_user = json_settings['db_user']
        self._db_password = json_settings['db_password']
        self._host = json_settings['host']
        if 'port' in json_settings:
            self._port = json_settings['port']
        else:
            self._port = '5432'
        self._client_id = json_settings['client_id']
        self._client_secret = json_settings['client_secret']
        self._client_name = json_settings['client_name']


# класс для получения настроек для ТГ. Наследуется от базового класса
class SettingsTelegram(Settings):
    def get_settings_tg(self) -> dict:
        list = {'token': self._token}
        return list


# класс для получения настроек для БД. Наследуется от базового класса
class SettingsDb(Settings):
    def get_settings_db(self) -> dict:
        list = {'db_name': self._db_name, 'db_user': self._db_user, 'db_password': self._db_password,
                'host': self._host, 'port': self._port}
        return list


# класс для получения настроек для Шики. Наследуется от базового класса
class SettingsShiki(Settings):
    def get_settings_shiki(self) -> dict:
        ls = {'client_id': self._client_id, 'client_secret': self._client_secret, 'client_name': self._client_name}
        return ls
