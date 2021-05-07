"""
Класс для работы с Telegram.
Для инициализации необходимо передать Токен.
"""
from time import sleep
import requests
import json


class Telegram:
    __TOKEN = None
    __BASE_URL = 'https://api.telegram.org/bot'
    session = requests.session()

    def delete_msg(self, chat_id, message_id):
        data = {'chat_id': chat_id, 'message_id': message_id}
        try:
            r = self.session.post(self.__BASE_URL + 'deleteMessage', data=data)
        except requests.exceptions.ConnectionError:
            r = self.session.post(self.__BASE_URL + 'deleteMessage', data=data)
        return json.loads(r.text)

    def edit_msg(self, chat_id, message_id, msg, reply_markup=None):
        if reply_markup is None:
            data = {'chat_id': chat_id, 'message_id': message_id, 'text': msg, 'parse_mode': 'HTML'}
        else:
            data = {'chat_id': chat_id, 'message_id': message_id, 'text': msg, 'parse_mode': 'HTML',
                    'reply_markup': reply_markup}
        try:
            r = self.session.post(self.__BASE_URL + 'editMessageText', data=data)
        except requests.exceptions.ConnectionError:
            r = self.session.post(self.__BASE_URL + 'editMessageText', data=data)
        return json.loads(r.text)

    def send_msg(self, chat_id, msg, reply_markup=None):
        if reply_markup is None:
            data = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'}
        else:
            data = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML', 'reply_markup': reply_markup}
        try:
            r = self.session.post(self.__BASE_URL + 'sendMessage', data=data)
        except requests.exceptions.ConnectionError:
            r = self.session.post(self.__BASE_URL + 'sendMessage', data=data)
        return json.loads(r.text)

    def get_updates(self, timeout=30, offset=None):
        try:
            data = {'timeout': timeout, 'offset': offset}
            r = self.session.post(self.__BASE_URL + 'getUpdates', data=data)
            return json.loads(r.text)['result']
        except requests.ConnectionError:
            sleep(10)
            print('ConnectionError GetUpdates')
            pass

    def answer_callback(self, id):
        data = {'callback_query_id': id}
        try:
            r = self.session.post(self.__BASE_URL + 'answerCallbackQuery', data=data)
            return json.loads(r.text)
        except requests.exceptions.ConnectionError:
            r = self.session.post(self.__BASE_URL + 'answerCallbackQuery', data=data)
            return json.loads(r.text)

    def __init__(self, token: str):
        self.__TOKEN = token
        self.__BASE_URL = self.__BASE_URL + self.__TOKEN + '/'
