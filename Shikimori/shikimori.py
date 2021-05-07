"""
Класс для работы с ShikiMore.
Для инициализации необходимо передать Токен.
"""
import json

from requests import Session


class Shikimori:
    __BASE_URL_V2 = 'https://shikimori.one/api/v2/'
    __BASE_URL_V1 = 'https://shikimori.one/api/'
    __BASE_URL_AUTH = 'https://shikimori.one/oauth/token'
    BASE_URL_SHIKI = 'https://shikimori.one'

    def __get_headers(self, token: str) -> dict:
        headers = {'User-Agent': self.__client_name, 'Authorization': f'Bearer {token}'}
        return headers

    def auth(self, auth_code: str = None, token: str = None, refresh_token: str = None):
        ses = Session()
        headers_auth = {'User-Agent': self.__client_name}
        if token is None and refresh_token is None:
            data = {'grant_type': 'authorization_code', 'client_id': self.__client_id,
                    'client_secret': self.__client_secret, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
                    'code': auth_code}
            s = ses.post(self.__BASE_URL_AUTH, headers=headers_auth, data=data)
        else:
            s = ses.get(self.__BASE_URL_V1 + 'users/whoami', headers=self.__get_headers(token=token))
            if s.status_code == 401:
                data = {'grant_type': 'refresh_token', 'client_id': self.__client_id,
                        'client_secret': self.__client_secret,
                        'refresh_token': refresh_token}
                s = ses.post(self.__BASE_URL_AUTH, headers=headers_auth, data=data)
        return json.loads(s.text)

    def get_info_about_users(self, token: str) -> list:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + 'users/whoami', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_and_manga_list(self, user_id: int, token: str) -> list:
        """Метод возвращает список Аниме пользователя на ShikiMori
        :param token: token user
        :param user_id: user_id in shikimori
        :return: list anime
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V2 + f'user_rates?user_id={user_id}', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_list(self, list_ids: list, token: str) -> list:
        """
        Возвращает базовую информацию по Аниме, списокм
        :param token: token user
        :param list_ids: ИД аниме. Максимум 50 значений
        :return: Список
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes?ids={",".join(str(id) for id in list_ids)}&limit=50',
                     headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_info(self, id_anime: int, token: str) -> dict:
        """Метод возвращает информацию по аниме
        :param token: token user
        :param id_anime: ia anime in ShikiMori
        :return: dict
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes/{id_anime}', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_info_not_auth(self, id_anime: int) -> dict:
        """Метод возвращает информацию по аниме
        :param id_anime: id anime in ShikiMori
        :return: dict
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes/{id_anime}', headers={'User-Agent': self.__client_name})
        return json.loads(js.text)

    def get_anime_search(self, token: str, limit: int = 50, page: int = 1, order: str = 'ranked',
                         search: str = '', franchise: str = '', timeout: int = None) -> list:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes?limit={limit}&order={order}&search={search}&page={page}'
                                          f'&franchise={franchise}',
                     headers=self.__get_headers(token=token), timeout=(timeout, timeout))
        return json.loads(js.text)

    def get_manga_search(self, search: str, token: str, limit: int = 50, page: int = 1, order: str = 'ranked') -> list:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'mangas?limit={limit}&order={order}&search={search}&page={page}',
                     headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_similar(self, id_anime: int, token: str) -> list:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes/{id_anime}/similar', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_anime_franchise(self, id_anime: int, token: str) -> dict:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'animes/{id_anime}/franchise', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_manga_similar(self, id_manga: int, token: str) -> list:
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'mangas/{id_manga}/similar', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_manga_list(self, list_ids: list, token: str) -> list:
        """
        Возвращает базовую информацию по Аниме, списокм
        :param token: token user
        :param list_ids: ИД манги. Максимум 50 значений
        :return: Список
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'mangas?ids={",".join(str(id) for id in list_ids)}&limit=50',
                     headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_manga_info(self, id_manga: int, token: str) -> dict:
        """Метод возвращает информацию по аниме
        :param token: token user
        :param id_manga: id manga in ShikiMori
        :return: dict
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'mangas/{id_manga}', headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def get_manga_info_not_auth(self, id_manga: int) -> dict:
        """Метод возвращает информацию по аниме
        :param id_manga: id anime in ShikiMori
        :return: dict
        """
        ses = Session()
        js = ses.get(self.__BASE_URL_V1 + f'mangas/{id_manga}', headers={'User-Agent': self.__client_name})
        return json.loads(js.text)

    def create_user_rates(self, user_id: int, target_id: int, target_type: str, token: str, status: str = None,
                          score: int = None, chapters: int = None, episodes: int = None, volumes: int = None,
                          rewatches: int = None, text: str = None) -> list:
        """Метод добавляет в список Аниме новое Аниме/Мангу для пользователя на ShikiMori

        :param token: token user
        :param user_id: id пользователя на Шики
        :param target_id: id аниме/манги на Шики
        :param target_type: Anime/Manga
        :param status: watching, completed, planed
        :param score: Оценка
        :param chapters: Главы
        :param episodes: кол-во просмотренных эпизодов
        :param volumes: Тома
        :param rewatches: кол-во пересмотров
        :param text: комментарий
        :return: ответ от сервера в виде json
        """

        param = '"user_id": ' + str(user_id) + \
                ', "target_id": ' + str(target_id) + \
                ', "target_type": "' + target_type + '"'
        if episodes is not None:
            param += f'"episodes": "{episodes}"'
        if status is not None:
            param += f', "status": "{status}"'
        if score is not None:
            param += f', "score": "{score}"'
        if chapters is not None:
            param += f', "chapters": "{chapters}"'
        if volumes is not None:
            param += f', "volumes": "{volumes}"'
        if rewatches is not None:
            param += f', "rewatches": "{rewatches}"'
        if text is not None:
            param += f', "text": "{text}"'

        js = '{"user_rate": {' + param + '}}'
        data = json.loads(js)
        ses = Session()
        js = ses.post(self.__BASE_URL_V2 + 'user_rates', json=data, headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def set_rates(self, id_user_rates: int, token: str, episodes: int = None, status: str = None, score: int = None,
                  chapters: int = None, volumes: int = None, rewatches: int = None, text: str = None) -> dict:
        """Метод редактирует список Аниме пользователя на ShikiMori

        :param token: token user
        :param id_user_rates: id объекта в списке аниме пользователя
        :param episodes: кол-во просмотренных эпизодов
        :param status: watching, completed, planed
        :param score: оценка
        :param chapters: -
        :param volumes: -
        :param rewatches: кол-во пересмотров
        :param text: комментарий
        :return: статус выполнения операции
        """
        param = None
        if episodes is not None:
            param = f'"episodes": "{episodes}"'
        if status is not None:
            if param is not None:
                param += f', "status": "{status}"'
            else:
                param = f'"status": "{status}"'
        if score is not None:
            if param is not None:
                param += f', "score": "{score}"'
            else:
                param = f'"score": "{score}"'
        if chapters is not None:
            if param is not None:
                param += f', "chapters": "{chapters}"'
            else:
                param = f'"chapters": "{chapters}"'
        if volumes is not None:
            if param is not None:
                param += f', "volumes": "{volumes}"'
            else:
                param = f'"volumes": "{volumes}"'
        if rewatches is not None:
            if param is not None:
                param += f', "rewatches": "{rewatches}"'
            else:
                param = f'"rewatches": "{rewatches}"'
        if text is not None:
            if param is not None:
                param += f', "text": "{text}"'
            else:
                param = f'"text": "{text}"'

        js = '{"user_rate": {' + param + '}}'
        data = json.loads(js)
        ses = Session()
        js = ses.put(self.__BASE_URL_V2 + 'user_rates/' + str(id_user_rates),
                     json=data, headers=self.__get_headers(token=token))
        return json.loads(js.text)

    def delete_user_rates(self, id_user_rates: int, token: str):
        """
        Удаялет из списка на Шики аниме
        :param token: token user
        :param id_user_rates: ID user_rate на Шики
        :return: Status code операции. 204 - успешно
        """
        ses = Session()
        js = ses.delete(self.__BASE_URL_V2 + f'user_rates/{id_user_rates}', headers=self.__get_headers(token=token))
        return js.status_code

    def __init__(self, client_id: str, client_secret: str, client_name: str):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__client_name = client_name
