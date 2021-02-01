"""
Класс для работы с логами.
В данном случае, просто пишем лог в файл. Файл создается в корне проекта
"""
import logging


class Logging:

    def input_log(self, error):
        logging.basicConfig(filename='ErrorLog.log', level=logging.ERROR)
        logging.error(error)
