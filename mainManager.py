from Caches.main_cache import MainCache
from DataBase.dbmanager import DataBaseManager
from Shikimori.shikimori import Shikimori
from Telegram.telegram import Telegram
from Models.dataModels import *
from time import sleep
from Utils.utils import Utils
import threading
import datetime
import json
import re


class MainManager:
    MAIN_KEYBOARD_TG = json.dumps({'keyboard': [[{'text': 'Мой список Аниме'}],
                                                [{'text': 'Аниме по сезонам'}],
                                                [{'text': 'Мой список Манги'}],
                                                [{'text': 'Настройки'}]],
                                   'resize_keyboard': True, 'one_time_keyboard': True})
    SETTIGNS_KEYBOARD_TG = json.dumps(
        {'inline_keyboard': [[{'text': 'Отображение списка', 'callback_data': 'ChangeListSettings//'}],
                             [{'text': ':is_notify_text', 'callback_data': 'ChangeNotify// :is_notify_param'}],
                             [{'text': 'Удалить аккаунт', 'callback_data': 'DeleteAccount//'}]]})
    MY_ANIME_LIST_KEYBOARD_TG = json.dumps(
        {'inline_keyboard': [[{'text': 'Обновить список', 'callback_data': 'UpdateListAnime//'}],
                             [{'text': 'Запланированные', 'callback_data': 'ListAnimePlaned//'}],
                             [{'text': 'Смотрю', 'callback_data': 'ListAnimeWatching//'}],
                             [{'text': 'Просмотренные', 'callback_data': 'ListAnimeCompleted//'}],
                             [{'text': 'Все', 'callback_data': 'ListAnimeAll//'}],
                             [{'text': 'Поиск Аниме', 'callback_data': 'SearchAnime//'}]]})
    MY_MANGA_LIST_KEYBOARD_TG = json.dumps(
        {'inline_keyboard': [[{'text': 'Обновить список', 'callback_data': 'UpdateListAnime//'}],
                             [{'text': 'Запланированные', 'callback_data': 'ListMangaPlaned//'}],
                             [{'text': 'Читаю', 'callback_data': 'ListMangaWatching//'}],
                             [{'text': 'Прочитанные', 'callback_data': 'ListMangaCompleted//'}],
                             [{'text': 'Все', 'callback_data': 'ListMangaAll//'}],
                             [{'text': 'Поиск Манги', 'callback_data': 'SearchManga//'}]]}
    )

    def __convert_json_to_anime(self, list_anime: list) -> list:
        ls = []
        for anime in list_anime:
            url = anime.get('url')
            if url is None or url == 'None':
                url = None
            else:
                url = self.__shiki.BASE_URL_SHIKI + url
            aried_on = anime.get('aired_on')
            if aried_on is None or aried_on == 'None':
                aried_on = None
            else:
                aried_on = datetime.datetime.strptime(anime.get('aired_on'), '%Y-%m-%d')
            released_on = anime.get('released_on')
            if released_on is None or released_on == 'None':
                released_on = None
            else:
                released_on = datetime.datetime.strptime(anime.get('released_on'), '%Y-%m-%d')
            next_episode_at = anime.get('next_episode_at')
            if next_episode_at is None or next_episode_at == 'None':
                next_episode_at = None
            else:
                next_episode_at = datetime.datetime.strptime(anime.get('next_episode_at')[:-10], '%Y-%m-%dT%H:%M:%S')
            updated_at = anime.get('updated_at')
            if updated_at is None or updated_at == 'None':
                updated_at = None
            else:
                updated_at = datetime.datetime.strptime(updated_at[:-10], '%Y-%m-%dT%H:%M:%S')
            description: str = anime.get('description')
            if description is not None and description != 'None':
                description = re.sub('\[.+?\]', ' ', description)
                description = description.replace("'", ' ')
            name_jp = anime.get('japanese')
            if name_jp is None or name_jp == 'None':
                name_jp = None
            else:
                name_jp = name_jp[0].replace("'", '')
            rating = anime.get('rating')
            if rating is None or rating == 'None':
                rating = None
            if anime.get('name').find("'") != -1:
                name = anime.get('name').replace("'", '')
            else:
                name = anime.get('name')
            if anime.get('russian').find("'") != -1:
                name_ru = anime.get('russian').replace("'", '')
            else:
                name_ru = anime.get('russian')
            if anime.get('franchise') is None or anime.get('franchise') == 'None':
                franchise = None
            else:
                franchise = anime.get('franchise')
            ls.append(Anime(id=anime.get('id'), name=name, name_ru=name_ru,
                            name_jp=name_jp, kind=anime.get('kind'), score=anime.get('score'),
                            status=anime.get('status'), episodes=anime.get('episodes'),
                            episodes_aired=anime.get('episodes_aired'), rating=rating,
                            description=description, updated_at=updated_at, aired_on=aried_on, released_on=released_on,
                            next_episode_at=next_episode_at, url=url, franchise=franchise))
        return ls

    def __convert_json_to_manga(self, list_manga: list) -> list:
        ls = []
        for manga in list_manga:
            url = manga.get('url')
            if url is None or url == 'None':
                url = None
            else:
                url = self.__shiki.BASE_URL_SHIKI + url
            aried_on = manga.get('aired_on')
            if aried_on is None or aried_on == 'None':
                aried_on = None
            else:
                aried_on = datetime.datetime.strptime(manga.get('aired_on'), '%Y-%m-%d')
            released_on = manga.get('released_on')
            if released_on is None or released_on == 'None':
                released_on = None
            else:
                released_on = datetime.datetime.strptime(manga.get('released_on'), '%Y-%m-%d')
            description: str = manga.get('description')
            if description is not None and description != 'None':
                description = re.sub('\[.+?\]', ' ', description)
                description = description.replace("'", ' ')
            name_jp = manga.get('japanese')
            if name_jp is None or name_jp == 'None':
                name_jp = None
            else:
                name_jp = name_jp[0]
            if manga.get('name').find("'") != -1:
                name = manga.get('name').replace("'", '')
            else:
                name = manga.get('name')
            status = manga.get('status')
            if status is None or status == 'None':
                status = None
            else:
                status = status
            ls.append(Manga(id=manga.get('id'), name=name, name_ru=manga.get('russian'),
                            name_jp=name_jp, kind=manga.get('kind'), score=manga.get('score'),
                            status=status, volumes=manga.get('volumes'), chapters=manga.get('chapters'),
                            description=description, aired_on=aried_on, released_on=released_on, url=url
                            )
                      )
        return ls

    def __convert_json_to_userrates(self, list_user_rates: list) -> list:
        user_rates = []
        for anime in list_user_rates:
            target_type = self.__db.get_type(anime.get('target_type'))
            status = self.__db.get_status(anime.get('status'))
            created_at = datetime.datetime.strptime(anime.get('created_at')[:-10], '%Y-%m-%dT%H:%M:%S')
            updated_at = datetime.datetime.strptime(anime.get('updated_at')[:-10], '%Y-%m-%dT%H:%M:%S')
            user_rates.append(UserRates(id=anime.get('id'), user_id=anime.get('user_id'),
                                        target_id=anime.get('target_id'), target_type=target_type.id,
                                        score=anime.get('score'), status=status.id,
                                        rewatches=anime.get('rewatches'), episodes=anime.get('episodes'),
                                        volumes=anime.get('volumes'), chapters=anime.get('chapters'),
                                        text=anime.get('text'), created_at=created_at,
                                        updated_at=updated_at))
        return user_rates

    def __auth_in_shiki(self, user: Users):
        s = self.__shiki.auth(token=user.token, refresh_token=user.refresh_token)
        if s.get('access_token') is not None:
            self.__db.add_user(tg_id=user.tg_id, token=s['access_token'], refresh_token=s['refresh_token'],
                               user_id=user.id)
            res = True
        elif s.get('id') is not None:
            res = True
        else:
            res = False
        return res

    def __not_auth_in_shiki(self, user: Users):
        self.__tg.send_msg(chat_id=user.tg_id, msg='Авторизация больше не действительна. '
                                                   'Необходимо авторизоваться заново!')
        self.__db.delete_token_user(id=user.id)

    def __generate_set_score_keyboard(self, user_rate_id: int, command: str) -> str:
        user_rate_id = str(user_rate_id)
        keyboard = '{"inline_keyboard": [[{"text": "0", "callback_data": "SetScrore/// %s 0 %s"}, ' % (
            user_rate_id, command)
        keyboard += '{"text": "1", "callback_data": "SetScrore/// %s 1 %s"}, ' % (user_rate_id, command)
        keyboard += '{"text": "2", "callback_data": "SetScrore/// %s 2 %s"}],' % (user_rate_id, command)
        keyboard += '[{"text": "3", "callback_data": "SetScrore/// %s 3 %s"},' % (user_rate_id, command)
        keyboard += '{"text": "4", "callback_data": "SetScrore/// %s 4 %s"},' % (user_rate_id, command)
        keyboard += '{"text": "5", "callback_data": "SetScrore/// %s 5 %s"}],' % (user_rate_id, command)
        keyboard += '[{"text": "6", "callback_data": "SetScrore/// %s 6 %s"},' % (user_rate_id, command)
        keyboard += '{"text": "7", "callback_data": "SetScrore/// %s 7 %s"},' % (user_rate_id, command)
        keyboard += '{"text": "8", "callback_data": "SetScrore/// %s 8 %s"}],' % (user_rate_id, command)
        keyboard += '[{"text": "9", "callback_data": "SetScrore/// %s 9 %s"},' % (user_rate_id, command)
        keyboard += '{"text": "10", "callback_data": "SetScrore/// %s 10 %s"}]]}' % (user_rate_id, command)
        return keyboard

    def __generate_3_keyboard(self, array: list[dict], param: str, all: int, is_planned: bool = False) -> str:
        keyboard = '{"inline_keyboard": [['
        i = 1
        count = 0
        for arr in array:
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            if param.lower().find('anime') != -1:
                keyboard += '{"text": %i, "callback_data": "anime_detail %i %s"},' % (
                    arr.get('text'), arr.get('id'), param)
            else:
                keyboard += '{"text": %i, "callback_data": "manga_detail %i %s"},' % (
                    arr.get('text'), arr.get('id'), param)
            i += 1
            count += 1
            if i == 10:
                break
        if all < 10:
            keyboard = keyboard[:-1] + ']]}'
        else:
            keyboard = keyboard[:-1] + '],[{"text": "Далее", "callback_data": "Next%s 9"}]]}' % param
        if is_planned:
            keyboard = keyboard[:-2] + ', [{"text": "Фильтр", "callback_data": "Filter//"}]]}'
        if param.lower().find('anime') != -1:
            keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'
        else:
            keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'MainManga//'
        return keyboard

    def __get_notify_message(self, users: list[Users], anime_list: list[Anime], manga_list: list[Manga]) -> dict:
        dc = {}

        for user in users:
            msg = ''

            for anime in anime_list:
                if self.__db.is_anime_added_user_rate(anime_id=anime.id, id_user=user.id):
                    msg += f'\n--{anime.name_ru}' if msg != '' else f'Вышли все эпизоды по Аниме:\n\n--{anime.name_ru}'

            for manga in manga_list:
                if self.__db.is_manga_added_user_rate(manga_id=manga.id, id_user=user.id):
                    if msg.find('Вышли все эпизоды по Манге') == -1:
                        msg += '\n\nВышли все эпизоды по Манге:\n'
                    msg += f'\n--{manga.name_ru}'

            dc[user.tg_id] = msg

        return dc

    def get_settings(self, tg_id: int):
        msg = 'Настройки\n'
        user = self.__db.get_user(tg_id=tg_id)
        setting_list = self.__db.get_settings_list(user.list_settings)
        msg += f'tg_id: {user.tg_id}\nuser_shiki_id: {user.id}\nОтображение списка: {setting_list[0].name}' \
               f'\nУведомлять о выходе всех серий: {True if user.is_notify == 1 else False}'
        if user.is_notify == 1:
            user_keyboard = self.SETTIGNS_KEYBOARD_TG.replace(':is_notify_text', 'Отключить уведомления')\
                .replace(':is_notify_param', '0')
        else:
            user_keyboard = self.SETTIGNS_KEYBOARD_TG.replace(':is_notify_text', 'Включить уведомления') \
                .replace(':is_notify_param', '1')
        self.__tg.send_msg(chat_id=user.tg_id, msg=msg, reply_markup=user_keyboard)

    def set_settings_list(self, tg_id: int, msg: str, msg_id: int):
        settings_list = self.__db.get_settings_list()

        if msg == 'ChangeListSettings//':
            message = 'Настройка отображения:\n'
            keyboard = '{"inline_keyboard": [['
            count = 0
            for l in settings_list:
                message += f'{l.id}) {l.name}\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "ChangeListSettings// %i"},' % (l.id, l.id)
                count += 1
            keyboard = keyboard[:-1] + '],[{"text": "Main", "callback_data": "ListAnimeWatching//"}]]}'
            message = message[:-2]
        else:
            msg = msg.split(' ')
            self.__db.set_settings_list(tg_id=tg_id, list_settings=int(msg[1]))
            message = 'Вы успешно имзенили настройки отображения!'
            keyboard = '{"inline_keyboard": [[{"text": "Main", "callback_data": "ListAnimeWatching//"}]]}'
        self.__tg.edit_msg(chat_id=tg_id, message_id=msg_id, msg=message, reply_markup=keyboard)

    def change_notify_user(self, tg_id: int, msg_id: int, is_notify: bool):
        self.__db.update_user(tg_id=tg_id, is_notify=1 if is_notify else 0)
        message = 'Вы успешно имзенили настройки уведомления!'
        keyboard = '{"inline_keyboard": [[{"text": "Main", "callback_data": "ListAnimeWatching//"}]]}'
        self.__tg.edit_msg(chat_id=tg_id, message_id=msg_id, msg=message, reply_markup=keyboard)

    def get_info_about_anime_in_shiki(self, anime_list: list, tg_id: int = None):
        ls = []
        if tg_id is not None:
            user = self.__db.get_user(tg_id=tg_id)
            if not self.__auth_in_shiki(user=user):
                self.__not_auth_in_shiki(user=user)
                return 0

            user = self.__db.get_user(tg_id=tg_id)

            for anime_id in anime_list:
                while True:
                    try:
                        anime: dict = self.__shiki.get_anime_info(id_anime=anime_id, token=user.token)
                        break
                    except Exception as e:
                        sleep(1)
                ls.append(anime)
        else:
            for anime_id in anime_list:
                while True:
                    try:
                        anime: dict = self.__shiki.get_anime_info_not_auth(id_anime=anime_id)
                        break
                    except Exception as e:
                        sleep(1)
                ls.append(anime)
        animes = self.__convert_json_to_anime(list_anime=ls)
        self.__db.insert_or_update_anime_detail(list_anime=animes)

    def get_info_about_manga_in_shiki(self, manga_list: list, tg_id: int = None):
        ls = []
        if tg_id is not None:
            user = self.__db.get_user(tg_id=tg_id)
            if not self.__auth_in_shiki(user=user):
                self.__not_auth_in_shiki(user=user)
                return 0

            user = self.__db.get_user(tg_id=tg_id)

            for manga_id in manga_list:
                while True:
                    try:
                        manga: dict = self.__shiki.get_manga_info(id_manga=manga_id, token=user.token)
                        break
                    except Exception as e:
                        sleep(1)
                ls.append(manga)
        else:
            for manga_id in manga_list:
                while True:
                    try:
                        manga: dict = self.__shiki.get_manga_info_not_auth(id_manga=manga_id)
                        break
                    except Exception as e:
                        sleep(1)
                ls.append(manga)
        mangas = self.__convert_json_to_manga(list_manga=ls)
        self.__db.insert_or_update_manga_detail(list_manga=mangas)

    def get_info_anime_similar_in_shiki(self, tg_id: int, id_anime: int):
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        anime_similar = self.__shiki.get_anime_similar(id_anime=id_anime, token=user.token)
        anime_similar = self.__convert_json_to_anime(list_anime=anime_similar)

        return anime_similar

    def get_info_manga_similar_in_shiki(self, tg_id: int, id_manga: int):
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        manga_similar = self.__shiki.get_manga_similar(id_manga=id_manga, token=user.token)
        manga_similar = self.__convert_json_to_manga(list_manga=manga_similar)

        return manga_similar

    def get_anime_similar(self, tg_id: int, msg: str, msg_id: int):
        arr = msg.split(' ')
        id = int(arr[1])
        page = int(arr[2])

        anime_list = self.get_info_anime_similar_in_shiki(tg_id=tg_id, id_anime=id)
        anime_list = anime_list[0:9]
        msg = f'Что нашел:\n'
        keyboard = '{"inline_keyboard": [['
        i = 1
        count = 0

        for anime in anime_list:
            msg += f'{i}) {anime.name}/{anime.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "anime_search %i %i"},' % (i, anime.id, 1)
            key = 'similar_anime_' + str(tg_id) + '_' + str(anime.id)
            #self.__context.add(key=key, value=anime.name)
            i += 1
            count += 1

        keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "anime_search %i %i"},' % (id, page)
        keyboard = keyboard[:-1] + ']]}'

        self.__tg.edit_msg(chat_id=tg_id, msg=msg, message_id=msg_id, reply_markup=keyboard)

    def get_manga_similar(self, tg_id: int, msg: str, msg_id: int):
        arr = msg.split(' ')
        id = int(arr[1])
        page = int(arr[2])

        manga_list = self.get_info_manga_similar_in_shiki(tg_id=tg_id, id_manga=id)
        manga_list = manga_list[0:9]
        msg = f'Что нашел:\n'
        keyboard = '{"inline_keyboard": [['
        i = 1
        count = 0

        for manga in manga_list:
            msg += f'{i}) {manga.name}/{manga.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "manga_search %i %i"},' % (i, manga.id, 1)
            i += 1
            count += 1

        keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "manga_search %i %i"},' % (id, page)
        keyboard = keyboard[:-1] + ']]}'

        self.__tg.edit_msg(chat_id=tg_id, msg=msg, message_id=msg_id, reply_markup=keyboard)

    def get_min_info_about_anime_is_shiki(self, id_list: list, tg_id: int):
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        if len(id_list) > 50:
            chunks = Utils.chunkify(items=id_list, chunk_size=50)
            animes = []
            for chunk in chunks:
                animes += self.__shiki.get_anime_list(list_ids=chunk, token=user.token)
        else:
            animes = self.__shiki.get_anime_list(list_ids=id_list, token=user.token)
        animes = self.__convert_json_to_anime(list_anime=animes)
        self.__db.insert_or_update_anime_detail(list_anime=animes)

    def get_min_info_about_manga_is_shiki(self, id_list: list, tg_id: int):
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        if len(id_list) > 50:
            chunks = Utils.chunkify(items=id_list, chunk_size=50)
            mangas = []
            for chunk in chunks:
                mangas += self.__shiki.get_manga_list(list_ids=chunk, token=user.token)
        else:
            mangas = self.__shiki.get_manga_list(list_ids=id_list, token=user.token)
        mangas = self.__convert_json_to_manga(list_manga=mangas)
        self.__db.insert_or_update_manga_detail(list_manga=mangas)

    def get_info_my_list_in_shiki(self, tg_id: int):
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        list_user_rate = self.__shiki.get_anime_and_manga_list(user_id=user.id, token=user.token)
        list_user_rate = self.__convert_json_to_userrates(list_user_rates=list_user_rate)
        ls = []
        ls2 = []

        for anime in list_user_rate:
            if not self.__db.is_anime_in_bd(anime.target_id) and anime.target_type == 1:
                ls.append(anime.target_id)
            if not self.__db.is_manga_in_bd(anime.target_id) and anime.target_type == 2:
                ls2.append(anime.target_id)

        if len(ls) != 0:
            self.get_min_info_about_anime_is_shiki(id_list=ls, tg_id=tg_id)
            threading.Thread(target=self.get_info_about_anime_in_shiki, args=(ls, tg_id)).start()
        if len(ls2) != 0:
            self.get_min_info_about_manga_is_shiki(id_list=ls2, tg_id=tg_id)
            threading.Thread(target=self.get_info_about_manga_in_shiki, args=(ls2, tg_id)).start()
        self.__db.insert_or_update_anime_list(list_anime=list_user_rate, user_id=user.id)

    def delete_anime_list(self, tg_id: int, msg: str, msg_id: int):
        user_rate_id = msg.split(' ')[1]
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        code = self.__shiki.delete_user_rates(id_user_rates=int(user_rate_id), token=user.token)
        if code == 204:
            self.__db.delete_anime_in_user_rates(user_rates_id=int(user_rate_id))
            self.get_my_list_anime(tg_id=tg_id, flag='ListAnimePlaned//', msg_id=msg_id)

    def delete_manga_list(self, tg_id: int, msg: str, msg_id: int):
        user_rate_id = msg.split(' ')[1]
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)

        code = self.__shiki.delete_user_rates(id_user_rates=int(user_rate_id), token=user.token)
        if code == 204:
            self.__db.delete_anime_in_user_rates(user_rates_id=int(user_rate_id))
            self.get_my_list_manga(tg_id=tg_id, flag='ListMangaPlaned//', msg_id=msg_id)

    def edit_user_rates(self, tg_id: int, message_id: int, command: str):
        commands = command.split(' ')
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0
        user = self.__db.get_user(tg_id=tg_id)

        if commands[0] == 'SetScrore//' and (len(commands) == 3 or len(commands) == 4):
            user_rate_id = commands[1]
            type = self.__db.get_type(id=self.__db.get_info_user_rate(id=int(user_rate_id)).target_type)
            user_rate = self.__db.get_info_user_rate(int(user_rate_id))
            if type.name == 'Anime':
                anime = self.__db.get_info_anime(user_rate.target_id)
            else:
                anime = self.__db.get_info_manga(user_rate.target_id)
            try:
                keyboard = self.__generate_set_score_keyboard(user_rate_id=int(user_rate_id),
                                                              command=commands[2] + ' ' + commands[3])
            except Exception:
                keyboard = self.__generate_set_score_keyboard(user_rate_id=int(user_rate_id), command=commands[2])
            self.__tg.edit_msg(chat_id=tg_id, message_id=message_id,
                               msg=f'Какую оценку поставите?\n{anime.name}\n{anime.name_ru}\n'
                                   f'Текущая оценка: {user_rate.score}', reply_markup=keyboard)
        elif commands[0] == 'SetScrore///' and len(commands) > 3:
            user_rate_id = int(commands[1])
            type = self.__db.get_type(id=self.__db.get_info_user_rate(id=user_rate_id).target_type)
            score = int(commands[2])
            other = ['1', ' 2 ']
            other.append(commands[3])
            try:
                other.append(' ' + commands[4])
            except:
                pass
            other = ''.join(other)

            anime = self.__shiki.set_rates(id_user_rates=user_rate_id, score=score,
                                           token=user.token)
            list_anime_data = self.__convert_json_to_userrates(list_user_rates=[anime])
            self.__db.insert_or_update_anime_list(list_anime=list_anime_data, user_id=user.id, flag='NO DELETE')
            if type.name == 'Anime':
                self.get_info_about_anime(tg_id=tg_id, msg_id=message_id, user_rate_id=user_rate_id, msg=other)
            else:
                self.get_info_about_manga(tg_id=tg_id, msg_id=message_id, user_rate_id=user_rate_id, msg=other)
        elif commands[0] == 'addVolumes//' or commands[0] == 'removeVolumes//':
            volumes = int(commands[1])
            user_rate_id = int(commands[2])
            other = ['1', ' 2 ']
            other.append(commands[3])
            try:
                other.append(' ' + commands[4])
            except:
                pass
            other = ''.join(other)
            manga = self.__shiki.set_rates(id_user_rates=user_rate_id, volumes=volumes, status='watching',
                                           token=user.token)
            list_manga_data = self.__convert_json_to_userrates(list_user_rates=[manga])
            self.__db.insert_or_update_anime_list(list_anime=list_manga_data, user_id=user.id, flag='NO DELETE')
            self.get_info_about_manga(tg_id=tg_id, msg_id=message_id, user_rate_id=user_rate_id, msg=other)
        else:
            episodes = int(commands[1])
            user_rate_id = int(commands[2])
            type = self.__db.get_type(id=self.__db.get_info_user_rate(id=user_rate_id).target_type)
            other = ['1', ' 2 ']
            other.append(commands[3])
            try:
                other.append(' ' + commands[4])
            except:
                pass
            other = ''.join(other)
            if type.name == 'Anime':
                kind = self.__db.get_info_anime(id=self.__db.get_info_user_rate(id=user_rate_id).target_id).kind
                if kind == 'movie':
                    anime = self.__shiki.set_rates(id_user_rates=user_rate_id, episodes=episodes, status='completed',
                                                   token=user.token)
                else:
                    anime = self.__shiki.set_rates(id_user_rates=user_rate_id, episodes=episodes, status='watching',
                                                   token=user.token)
            else:
                anime = self.__shiki.set_rates(id_user_rates=user_rate_id, chapters=episodes, status='watching',
                                               token=user.token)
            list_anime_data = self.__convert_json_to_userrates(list_user_rates=[anime])
            self.__db.insert_or_update_anime_list(list_anime=list_anime_data, user_id=user.id, flag='NO DELETE')
            if type.name == 'Anime':
                self.get_info_about_anime(tg_id=tg_id, msg_id=message_id, user_rate_id=user_rate_id, msg=other)
            else:
                self.get_info_about_manga(tg_id=tg_id, msg_id=message_id, user_rate_id=user_rate_id, msg=other)

    def update_anime_and_manga(self):
        animes = self.__db.get_anime_id_list_for_update()
        self.get_info_about_anime_in_shiki(anime_list=animes)
        animes_after_update = self.__db.get_anime_id_list_for_update()
        animes_list = []
        users = self.__db.get_all_user_notify()

        for anime_id in animes:
            if str(animes_after_update).find(str(anime_id)) == -1:
                anime = self.__db.get_info_anime(id=anime_id)
                animes_list.append(anime)

        mangas = self.__db.get_manga_id_list_for_update()
        self.get_info_about_manga_in_shiki(manga_list=mangas)
        mangas_after_update = self.__db.get_manga_id_list_for_update()
        mangas_list = []

        for manga_id in mangas:
            if str(mangas_after_update).find(str(manga_id)) == -1:
                manga = self.__db.get_info_manga(id=manga_id)
                mangas_list.append(manga)

        notify_dict = self.__get_notify_message(users, animes_list, mangas_list)

        for chat_id, msg in notify_dict.items():
            self.__tg.send_msg(chat_id=chat_id, msg=msg)

    def all_update_anime(self):
        animes = self.__db.get_all_anime_id()
        self.get_info_about_anime_in_shiki(anime_list=animes)

    def add_anime_in_my_list(self, tg_id: int, msg_id: int, msg: str):
        anime = self.__db.get_info_anime(id=int(msg.replace('add_user_rate ', '')))
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)
        user_rate = self.__shiki.create_user_rates(user_id=user.id, target_id=anime.id, token=user.token,
                                                   target_type='Anime')
        user_rate = self.__convert_json_to_userrates([user_rate])
        self.__db.insert_or_update_anime_list(list_anime=user_rate, user_id=user.id, flag='NO DELETE')

        self.__tg.edit_msg(chat_id=tg_id, msg='Аниме добавлено в список!',
                           message_id=msg_id, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG)

    def add_manga_in_my_list(self, tg_id: int, msg_id: int, msg: str):
        manga = self.__db.get_info_manga(id=int(msg.replace('add_user_rate_manga ', '')))
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)
        user_rate = self.__shiki.create_user_rates(user_id=user.id, target_id=manga.id, token=user.token,
                                                   target_type='Manga')
        user_rate = self.__convert_json_to_userrates([user_rate])
        self.__db.insert_or_update_anime_list(list_anime=user_rate, user_id=user.id, flag='NO DELETE')

        self.__tg.edit_msg(chat_id=tg_id, msg='Манга добавлено в список!',
                           message_id=msg_id, reply_markup=self.MY_MANGA_LIST_KEYBOARD_TG)

    def get_anime_franchise(self, tg_id: int, msg_id: int, msg: str):
        msg = msg.split(' ')
        user_rate_id = int(msg[1])
        page = int(msg[2])
        try:
            flag = msg[3] + ' ' + msg[4]
        except:
            flag = msg[3]

        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0

        user = self.__db.get_user(tg_id=tg_id)
        user_rate = self.__db.get_info_user_rate(id=user_rate_id)
        anime_id = user_rate.target_id
        anime = self.__db.get_info_anime(id=anime_id)
        anime_franchise = self.__shiki.get_anime_search(token=user.token, franchise=anime.franchise, limit=9,
                                                        page=page, order='aired_on')
        anime_franchise = self.__convert_json_to_anime(list_anime=anime_franchise)

        msg = ''
        keyboard = '{"inline_keyboard": [['
        i = 1 + (page - 1) * 9
        k = i
        count = 0

        for anime in anime_franchise:
            msg += f'{i}) {anime.name}/{anime.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "anime_franchise_d %i %i %i %s"},' % (i, anime.id,
                                                                                             user_rate_id, page, flag)
            i += 1
            count += 1

        if len(anime_franchise) == 0 and page != 1:
            msg = 'Дальше аниме нет!'
            keyboard = keyboard[
                       :-1] + '[{"text": "Назад", "callback_data": "anime_franchise %i %i %s"}]]}' % (user_rate_id,
                                                                                                      page - 1, flag)
        elif len(anime_franchise) < 9 and page != 1:
            keyboard = keyboard[
                       :-1] + '],[{"text": "Назад", "callback_data": "anime_franchise %i %i %s"}]]}' % (
                           user_rate_id, page - 1, flag)
        elif k == 1 and len(anime_franchise) >= 9:
            keyboard = keyboard[
                       :-1] + '],[{"text": "Далее", "callback_data": "anime_franchise %i %i %s"}]]}' % (user_rate_id,
                                                                                                        page + 1, flag)
        elif len(anime_franchise) < 9:
            keyboard = keyboard[:-1] + ']]}'
        else:
            keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "anime_franchise %i %i %s"},' \
                                       '{"text": "Далее", "callback_data": "anime_franchise %i %i %s"}]]}' % (
                           user_rate_id, page - 1, flag, user_rate_id, page + 1, flag)
        keyboard = keyboard[:-2] + ',[{"text": "Назад к Аниме", "callback_data": "anime_detail %i %s"}]]}' % (
            user_rate_id, flag)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'
        if msg_id is None:
            self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard)
        else:
            self.__tg.edit_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard, message_id=msg_id)

    def search_main_anime_or_manga(self, tg_id: int, flag: str) -> None:
        if flag == 'SearchAnime//':
            msg = 'Введите название Аниме'
            self.__db.update_user(tg_id=tg_id, search='anime_search///')
        else:
            msg = 'Введите название Манги'
            self.__db.update_user(tg_id=tg_id, search='manga_search///')
        self.__tg.send_msg(chat_id=tg_id, msg=msg)

    def get_anime_seasons(self, tg_id: int, year: int = None, msg_id: int = None):
        if msg_id is None:
            msg = 'Введите год:'
            self.__tg.send_msg(chat_id=tg_id, msg=msg)
        else:
            if year < 1900:
                self.__tg.send_msg(chat_id=tg_id, msg='Введите год больше 1900!')
            else:
                msg = 'Выберите сезон:\n\n'
                keyboard = '{"inline_keyboard": [[{"text": "Зимний сезон", "callback_data": "seasons// winter %i"}], ' \
                           '[{"text": "Весенний сезон", "callback_data": "seasons// spring %i"}],' \
                           '[{"text": "Летний сезон", "callback_data": "seasons// summer %i"}],' \
                           '[{"text": "Осенний сезон", "callback_data": "seasons// fall %i"}],' \
                           '[{"text": "За весь год", "callback_data": "seasons// None %i"}]]}' % (year, year, year, year, year)
                self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard)

    def get_anime_seasons_result(self, tg_id: int, msg: str, msg_id: int):
        split = msg.split(' ')
        anime_id = int(split[1])
        page = int(split[4])
        seasons = split[2]
        year = split[3]

        user = self.__db.get_user(tg_id=tg_id)
        is_anime_added = self.__db.is_anime_added_user_rate(anime_id=anime_id, id_user=user.id)

        if is_anime_added:
            keyboard = '{"inline_keyboard": [[{"text": "Похожие", "callback_data": "anime_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "seasons// %s %s %i"}]]}' % (anime_id, page, seasons, year, page)
        else:
            keyboard = '{"inline_keyboard": [[{"text": "Добавить в список", "callback_data": "add_user_rate %i"}], ' \
                       '[{"text": "Похожие", "callback_data": "anime_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "seasons// %s %s %i"}]]}' % (anime_id, anime_id, page, seasons, year, page)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'

        if not self.__db.is_anime_in_bd(anime_id=anime_id):
            self.get_info_about_anime_in_shiki(anime_list=[anime_id], tg_id=tg_id)
        anime = self.__db.get_info_anime(anime_id)
        status = anime.status

        message = f'Название: {anime.name}\nНазвание_ru: {anime.name_ru}\nСтатус: {anime.status}\n' \
                  f'Рейтинг: {anime.rating}\nТип: {anime.kind}\n'
        if status == 'ongoing':
            if anime.next_episode_at is not None:
                message += f'Дата выхода эпизода: {datetime.datetime.strftime(anime.next_episode_at, "%Y-%m-%d")}\n'
            message += f'Ко-во вышедших эпизодов: {anime.episodes_aired}\n'
        message += f'Всего эпизодов: {anime.episodes}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(anime.aired_on, "%Y-%m-%d")}\n'
        message += f'Оценка: {anime.score}\nUrl: {anime.url}\n\nОписание:\n{anime.description}'
        self.__tg.edit_msg(chat_id=tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def get_anime_seasons_in_shiki(self, tg_id: int, msg: str, msg_id: int = None):
        split = msg.split(' ')

        if split[1] == 'None':
            season = None
        else:
            season = split[1]
        year = split[2]
        if len(split) == 3:
            page = 1
        else:
            page = int(split[3])

        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0
        user = self.__db.get_user(tg_id=tg_id)

        if season is not None:
            anime_list = self.__shiki.get_anime_search(token=user.token, limit=9, page=page, season=season + '_' + year)
        else:
            anime_list = self.__shiki.get_anime_search(token=user.token, limit=9, page=page, season=year)
        anime_list = self.__convert_json_to_anime(list_anime=anime_list)
        msg = f'Сезон: {season}, Год: {year}\n\nЧто нашел:\n'
        keyboard = '{"inline_keyboard": [['
        if msg_id is not None:
            i = 1 + (page - 1) * 9
        else:
            i = 1
        k = i
        count = 0

        for anime in anime_list:
            msg += f'{i}) {anime.name}/{anime.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "anime_seasons %i %s %s %i"},' % (i, anime.id, season, year, page)
            i += 1
            count += 1

        if len(anime_list) == 0:
            msg = 'Дальше аниме нет'
            keyboard = keyboard[
                       :-1] + '[{"text": "Назад", "callback_data": "seasons// %s %s %i"}]]}' % (season, year, page - 1)
        elif k == 1:
            keyboard = keyboard[
                       :-1] + '],[{"text": "Далее", "callback_data": "seasons// %s %s %i"}]]}' % (season, year, page + 1)
        else:
            keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "seasons// %s %s %i"},' \
                                       '{"text": "Далее", "callback_data": "seasons// %s %s %i"}]]}' % (
                           season, year, page - 1, season, year, page + 1)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'
        if msg_id is None:
            self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard)
        else:
            self.__tg.edit_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard, message_id=msg_id)

    def search_anime_in_shiki(self, tg_id: int, msg: str, msg_id: int = None):
        key = 'search_anime_' + str(tg_id)
        if msg_id is not None:
            st = msg.index('search//+')
            page = int(msg[0:st - 1])
            anime_name = self.__context.get(key=key)
        else:
            page = 1
            counter = 1
            anime_name = msg
            self.__context.add(key=key, value=msg)

        self.__db.update_user(tg_id=tg_id)
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0
        user = self.__db.get_user(tg_id=tg_id)

        if anime_name is None:
            msg = 'Воспользуйтесь поиском аниме заново'
            if msg_id is None:
                self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG)
            else:
                self.__tg.edit_msg(chat_id=tg_id, msg=msg, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG,
                                   message_id=msg_id)
            return 0

        anime_list = self.__shiki.get_anime_search(token=user.token, search=anime_name, limit=9, page=page)
        anime_list = self.__convert_json_to_anime(list_anime=anime_list)
        msg = f'Поиск: {anime_name}\n\nЧто нашел:\n'
        keyboard = '{"inline_keyboard": [['
        if msg_id is not None:
            i = 1 + (page - 1) * 9
        else:
            i = 1
        k = i
        count = 0

        for anime in anime_list:
            msg += f'{i}) {anime.name}/{anime.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "anime_search %i %i"},' % (i, anime.id, page)
            i += 1
            count += 1

        if len(anime_list) == 0:
            msg = 'Дальше аниме нет'
            keyboard = keyboard[
                       :-1] + '[{"text": "Назад", "callback_data": "%i search//+"}]]}' % (page - 1)
        elif k == 1:
            keyboard = keyboard[
                       :-1] + '],[{"text": "Далее", "callback_data": "%i search//+"}]]}' % (page + 1)
        else:
            keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "%i search//+"},' \
                                       '{"text": "Далее", "callback_data": "%i search//+"}]]}' % (
                           page - 1, page + 1)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'
        if msg_id is None:
            self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard)
        else:
            self.__tg.edit_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard, message_id=msg_id)

    def search_manga_in_shiki(self, tg_id: int, msg: str, msg_id: int = None):
        key = 'search_manga_' + str(tg_id)
        if msg_id is not None:
            st = msg.index('search//_')
            page = int(msg[0:st - 1])
            manga_name = self.__context.get(key=key)
        else:
            page = 1
            manga_name = msg
            self.__context.add(key=key, value=manga_name)

        self.__db.update_user(tg_id=tg_id)
        user = self.__db.get_user(tg_id=tg_id)
        if not self.__auth_in_shiki(user=user):
            self.__not_auth_in_shiki(user=user)
            return 0
        user = self.__db.get_user(tg_id=tg_id)

        manga_list = self.__shiki.get_manga_search(token=user.token, search=manga_name, limit=9, page=page)
        manga_list = self.__convert_json_to_manga(list_manga=manga_list)
        msg = f'Поиск: {manga_name}\n\nЧто нашел:\n'
        keyboard = '{"inline_keyboard": [['
        if msg_id is not None:
            i = 1 + (page - 1) * 9
        else:
            i = 1
        k = i
        count = 0

        for manga in manga_list:
            msg += f'{i}) {manga.name}/{manga.name_ru}\n'
            if count == 3:
                keyboard = keyboard[:-1] + '],['
                count = 0
            keyboard += '{"text": %i, "callback_data": "manga_search %i %i"},' % (i, manga.id, page)
            i += 1
            count += 1

        if len(manga_list) == 0:
            msg = 'Дальше манги нет'
            keyboard = keyboard[
                       :-1] + '[{"text": "Назад", "callback_data": "%i search//_"}]]}' % (page - 1)
        elif k == 1:
            keyboard = keyboard[
                       :-1] + '],[{"text": "Далее", "callback_data": "%i search//_"}]]}' % (page + 1)
        else:
            keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "%i search//_"},' \
                                       '{"text": "Далее", "callback_data": "%i search//_"}]]}' % (
                           page - 1, page + 1)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'MainManga//'
        if msg_id is None:
            self.__tg.send_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard)
        else:
            self.__tg.edit_msg(chat_id=tg_id, msg=msg, reply_markup=keyboard, message_id=msg_id)

    def search_anime_result(self, tg_id: int, msg_id: int, msg: str):
        arr = msg.split(' ')
        id = int(arr[1])
        page = int(arr[2])

        key = 'search_anime_' + str(tg_id)
        key_similar = 'similar_anime_' + str(tg_id) + '_' + str(id)

        user = self.__db.get_user(tg_id=tg_id)
        is_anime_added = self.__db.is_anime_added_user_rate(anime_id=id, id_user=user.id)

        if is_anime_added:
            keyboard = '{"inline_keyboard": [[{"text": "Похожие", "callback_data": "anime_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "%i search//+"}]]}' % (id, page, page)
        else:
            keyboard = '{"inline_keyboard": [[{"text": "Добавить в список", "callback_data": "add_user_rate %i"}], ' \
                       '[{"text": "Похожие", "callback_data": "anime_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "%i search//+"}]]}' % (id, id, page, page)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'

        if not self.__db.is_anime_in_bd(anime_id=id):
            self.get_info_about_anime_in_shiki(anime_list=[id], tg_id=tg_id)
        anime = self.__db.get_info_anime(id)
        status = anime.status

        #self.__context.add(key=key, value=anime.name)

        message = f'Название: {anime.name}\nНазвание_ru: {anime.name_ru}\nСтатус: {anime.status}\n' \
                  f'Рейтинг: {anime.rating}\nТип: {anime.kind}\n'
        if status == 'ongoing':
            message += f'Дата выхода эпизода: {datetime.datetime.strftime(anime.next_episode_at, "%Y-%m-%d")}\n'
            message += f'Ко-во вышедших эпизодов: {anime.episodes_aired}\n'
        message += f'Всего эпизодов: {anime.episodes}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(anime.aired_on, "%Y-%m-%d")}\n'
        message += f'Оценка: {anime.score}\nUrl: {anime.url}\n\nОписание:\n{anime.description}'
        self.__tg.edit_msg(chat_id=tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def search_manga_result(self, tg_id: int, msg_id: int, msg: str):
        arr = msg.split(' ')
        id = int(arr[1])
        page = int(arr[2])

        key = 'search_manga_' + str(tg_id)
        key_similar = 'similar_manga_' + str(tg_id) + '_' + str(id)

        user = self.__db.get_user(tg_id=tg_id)
        is_manga_added = self.__db.is_anime_added_user_rate(anime_id=id, id_user=user.id)

        if is_manga_added:
            keyboard = '{"inline_keyboard": [[{"text": "Похожие", "callback_data": "manga_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "%i search//_"}]]}' % (id, page, page)
        else:
            keyboard = '{"inline_keyboard": [[{"text": "Добавить в список", "callback_data": "add_user_rate_manga %i"}], ' \
                       '[{"text": "Похожие", "callback_data": "manga_similar %i %i"}],' \
                       '[{"text": "Назад", "callback_data": "%i search//_"}]]}' % (id, id, page, page)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'MainManga//'

        if not self.__db.is_manga_in_bd(manga_id=id):
            self.get_info_about_manga_in_shiki(manga_list=[id], tg_id=tg_id)
        manga = self.__db.get_info_manga(id)
        status = manga.status

        message = f'Название: {manga.name}\nНазвание_ru: {manga.name_ru}\nСтатус: {manga.status}\n' \
                  f'Рейтинг: {manga.score}\nТип: {manga.kind}\n'
        message += f'Ко-во вышедших глав: {manga.chapters}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(manga.aired_on, "%Y-%m-%d")}\n'
        message += f'Url: {manga.url}\n\nОписание:\n{manga.description}'
        self.__tg.edit_msg(chat_id=tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def get_info_about_anime_franchise(self, tg_id: int, msg_id: int, msg: str):
        msg = msg.split(' ')
        anime_id = int(msg[1])
        user_rate_id = int(msg[2])
        page = int(msg[3])
        try:
            flag = msg[4] + ' ' + msg[5]
        except:
            flag = msg[4]

        user = self.__db.get_user(tg_id=tg_id)
        self.get_info_about_anime_in_shiki(anime_list=[anime_id], tg_id=tg_id)

        anime = self.__db.get_info_anime(id=anime_id)
        is_my_list = self.__db.is_anime_added_user_rate(anime_id=anime_id, id_user=user.id)

        status = anime.status
        message = f'Название: {anime.name}\nНазвание_ru: {anime.name_ru}\nСтатус: {anime.status}\n' \
                  f'Рейтинг: {anime.rating}\nТип: {anime.kind}\n'
        if status == 'ongoing':
            message += f'Дата выхода эпизода: {datetime.datetime.strftime(anime.next_episode_at, "%Y-%m-%d")}\n'
            message += f'Ко-во вышедших эпизодов: {anime.episodes_aired}\n'
        message += f'Всего эпизодов: {anime.episodes}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(anime.aired_on, "%Y-%m-%d")}\n'
        message += f'Оценка: {anime.score}\nUrl: {anime.url}\n\nОписание:\n{anime.description}'

        if not is_my_list:
            keyboard = '{"inline_keyboard": [[{"text": "Добавить в список", "callback_data": "add_user_rate %i"}],' % \
                       anime_id
        else:
            keyboard = '{"inline_keyboard": ['
        keyboard = keyboard + '[{"text": "Назад", "callback_data": "anime_franchise %i %i %s"}]]}' % (user_rate_id,
                                                                                                           page, flag)
        self.__tg.edit_msg(chat_id=user.tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def get_info_about_anime(self, tg_id: int, msg_id: int, user_rate_id: int, msg: str):
        msg = msg.split(' ')
        user = self.__db.get_user(tg_id=tg_id)
        user_rate = self.__db.get_info_user_rate(id=user_rate_id)
        anime = self.__db.get_info_anime(id=user_rate.target_id)
        anime_franchise = self.__shiki.get_anime_search(token=user.token, franchise=anime.franchise, limit=9,
                                                        page=1, order='aired_on', timeout=3)
        status = anime.status
        message = f'Название: {anime.name}\nНазвание_ru: {anime.name_ru}\nСтатус: {anime.status}\n' \
                  f'Рейтинг: {anime.rating}\nТип: {anime.kind}\n'
        if status == 'ongoing':
            message += f'Дата выхода эпизода: {datetime.datetime.strftime(anime.next_episode_at, "%Y-%m-%d")}\n'
            message += f'Ко-во вышедших эпизодов: {anime.episodes_aired}\n'
        message += f'Просмотренно эпизодов: {user_rate.episodes}\n' \
                   f'Всего эпизодов: {anime.episodes}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(anime.aired_on, "%Y-%m-%d")}\n'
        message += f'Оценка Ваша: {user_rate.score}\n' \
                   f'Оценка: {anime.score}\nUrl: {anime.url}\n\nОписание:\n{anime.description}'

        if status != 'anons':
            try:
                p = 'addEpisodes// ' + str(user_rate.episodes + 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + msg[
                    3]
                m = 'removeEpisodes// ' + str(user_rate.episodes - 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + \
                    msg[3]
            except:
                p = 'addEpisodes// ' + str(user_rate.episodes + 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
                m = 'removeEpisodes// ' + str(user_rate.episodes - 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
            if user_rate.episodes == anime.episodes:
                keyboard = '{"inline_keyboard": [[{"text": "-", "callback_data": "%s"}],yy' % (m)
            elif user_rate.episodes != 0:
                keyboard = '{"inline_keyboard": [[{"text": "-", "callback_data": "%s"},' \
                           '{"text": "+", "callback_data": "%s"}],yy' % (m, p)
            else:
                keyboard = '{"inline_keyboard": [[{"text": "+", "callback_data": "%s"}],yy' % (p)
            if user_rate.status == 3:
                keyboard = keyboard[
                           :-2] + '[{"text": "Удалить из списка", "callback_data": "DeleteUserRates// %s"}],yy' % user_rate.id
            else:
                try:
                    set_score = 'SetScrore// %s %s' % (user_rate.id, msg[2] + ' ' + msg[3])
                except Exception:
                    set_score = 'SetScrore// %s %s' % (user_rate.id, msg[2])
                keyboard = keyboard[
                           :-2] + '[{"text": "Поставить оценку", "callback_data": "%s"}],yy' % set_score
        else:
            keyboard = '{"inline_keyboard": [[['
        if len(anime_franchise) > 0:
            try:
                keyboard = keyboard[:-2] + '[{"text": "Франшиза", "callback_data": "anime_franchise %s %i %s"}], yy' % (
                    user_rate_id, 1, msg[2] + ' ' + msg[3])
            except:
                keyboard = keyboard[:-2] + '[{"text": "Франшиза", "callback_data": "anime_franchise %s %i %s"}], yy' % (
                    user_rate_id, 1, msg[2])
        #keyboard = keyboard[:-2] + '[{"text": "Похожие", "callback_data": "anime_similar %i"}], yy' % anime.id
        try:
            keyboard = keyboard[:-2] + '[{"text": "Назад", "callback_data": "%s"}]]}' % (msg[2] + ' ' + msg[3])
        except:
            keyboard = keyboard[:-2] + '[{"text": "Назад", "callback_data": "%s"}]]}' % (msg[2])
        self.__tg.edit_msg(chat_id=user.tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def get_info_about_manga(self, tg_id: int, msg_id: int, user_rate_id: int, msg: str):
        msg = msg.split(' ')
        user = self.__db.get_user(tg_id=tg_id)
        user_rate = self.__db.get_info_user_rate(id=user_rate_id)
        manga = self.__db.get_info_manga(id=user_rate.target_id)
        status = manga.status

        message = f'Название: {manga.name}\nНазвание_ru: {manga.name_ru}\nСтатус: {manga.status}\n' \
                  f'Тип: {manga.kind}\n'
        if status == 'ongoing':
            message += f'Ко-во вышедших томов: {manga.volumes}\n'
            message += f'Ко-во вышедших глав: {manga.chapters}\n'
        message += f'Прочитано томов: {user_rate.volumes}\n' \
                   f'Всего томов: {manga.volumes}\n' \
                   f'Прочитано глав: {user_rate.chapters}\n' \
                   f'Всего глав: {manga.chapters}\n'
        if status != 'anons':
            message += f'Дата выхода: {datetime.datetime.strftime(manga.aired_on, "%Y-%m-%d")}\n'
        message += f'Оценка Ваша: {user_rate.score}\n' \
                   f'Оценка: {manga.score}\nUrl: {manga.url}\n\nОписание:\n{manga.description}'

        if status != 'anons':
            try:
                p = 'addEpisodes// ' + str(user_rate.chapters + 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + msg[
                    3]
                m = 'removeEpisodes// ' + str(user_rate.chapters - 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + \
                    msg[3]
                t = 'addVolumes// ' + str(user_rate.volumes + 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + \
                    msg[3]
                k = 'removeVolumes// ' + str(user_rate.volumes - 1) + ' ' + str(user_rate.id) + ' ' + msg[2] + ' ' + \
                    msg[3]
            except:
                p = 'addEpisodes// ' + str(user_rate.chapters + 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
                m = 'removeEpisodes// ' + str(user_rate.chapters - 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
                t = 'addVolumes// ' + str(user_rate.volumes + 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
                k = 'removeVolumes// ' + str(user_rate.volumes - 1) + ' ' + str(user_rate.id) + ' ' + msg[2]
            if user_rate.volumes == manga.volumes:
                keyboard = '{"inline_keyboard": [[{"text": "Том -", "callback_data": "%s"}],yy' % (k)
            elif user_rate.volumes != 0:
                keyboard = '{"inline_keyboard": [[{"text": "Том -", "callback_data": "%s"},' \
                           '{"text": "Том +", "callback_data": "%s"}],yy' % (k, t)
            else:
                keyboard = '{"inline_keyboard": [[{"text": "Том +", "callback_data": "%s"}],yy' % (t)
            if user_rate.chapters == manga.chapters:
                keyboard = keyboard[:-2] + '[{"text": "Глава -", "callback_data": "%s"}],yy' % (m)
            elif user_rate.chapters != 0:
                keyboard = keyboard[:-2] + '[{"text": "Глава -", "callback_data": "%s"},' \
                                           '{"text": "Глава +", "callback_data": "%s"}],yy' % (m, p)
            else:
                keyboard = keyboard[:-2] + '[{"text": "Глава +", "callback_data": "%s"}],yy' % (p)
            if user_rate.status == 3:
                keyboard = keyboard[
                           :-2] + '[{"text": "Удалить из списка", "callback_data": "DeleteUserRatesManga// %s"}],yy' % user_rate.id
            else:
                try:
                    set_score = 'SetScrore// %s %s' % (user_rate.id, msg[2] + ' ' + msg[3])
                except Exception:
                    set_score = 'SetScrore// %s %s' % (user_rate.id, msg[2])
                keyboard = keyboard[
                           :-2] + '[{"text": "Поставить оценку", "callback_data": "%s"}],yy' % set_score
        else:
            keyboard = '{"inline_keyboard": [[['
        try:
            keyboard = keyboard[:-2] + '[{"text": "Назад", "callback_data": "%s"}]]}' % (msg[2] + ' ' + msg[3])
        except:
            keyboard = keyboard[:-2] + '[{"text": "Назад", "callback_data": "%s"}]]}' % (msg[2])
        self.__tg.edit_msg(chat_id=user.tg_id, msg=message, message_id=msg_id, reply_markup=keyboard)

    def get_next_list_anime(self, tg_id: int, flag: str, msg_id: int):
        user = self.__db.get_user(tg_id=tg_id)
        message = ''
        keyboard = ''
        flag = flag.split(' ')
        if flag[0] == 'NextListAnimeCompleted//':
            spisok = self.__db.get_my_list_anime(status='completed', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Аниме просмотренно {len_spisok}:\nНазвание\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_anime_9_rows(status='completed', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0

            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "anime_detail %i NextListAnimeCompleted// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1

            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeCompleted// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListAnimeCompleted// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeCompleted// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListAnimeCompleted// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListAnimeAll//':
            spisok = self.__db.get_my_list_anime(status='all', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Все аниме {len_spisok}:\nНазвание\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_anime_9_rows(status='all', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0

            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "anime_detail %i NextListAnimeAll// %s"},' % (
                    i + 1, anime[4], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeAll// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListAnimeAll// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeAll// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListAnimeAll// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListAnimeWatching//':
            spisok = self.__db.get_my_list_anime(status='watching', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Аниме смотрю {len(spisok)}:\nНазвание - Кол-во просмотренных эпизодов\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_anime_9_rows(status='watching', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0
            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "anime_detail %i NextListAnimeWatching// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeWatching// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListAnimeWatching// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListAnimeWatching// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListAnimeWatching// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListAnimePlaned//':
            spisok = self.__db.get_my_list_anime(status='planned', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Аниме запланировано {len(spisok)}:\nНазвание - Кол-во всего эпизодов\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_anime_9_rows(status='planned', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0
            for anime in spisok:
                message += str(i + 1) + ') <b>' + anime[4] + '</b>: ' + anime[0] + '\n\b' + anime[1] + ' - ' + str(
                    anime[2]) + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "anime_detail %i NextListAnimePlaned// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListAnimePlaned// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListAnimePlaned// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListAnimePlaned// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListAnimePlaned// %i"}]]}' % (
                               k, i)
            keyboard = keyboard[:-2] + ', [{"text": "Фильтр", "callback_data": "Filter//"}]]}'
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'Main//'
        self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=keyboard,
                           message_id=msg_id)

    def get_next_list_manga(self, tg_id: int, flag: str, msg_id: int):
        user = self.__db.get_user(tg_id=tg_id)
        message = ''
        keyboard = ''
        flag = flag.split(' ')
        if flag[0] == 'NextListMangaCompleted//':
            spisok = self.__db.get_my_list_manga(status='completed', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Манги прочитано {len_spisok}:\nНазвание\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_manga_9_rows(status='completed', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0

            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "manga_detail %i NextListMangaCompleted// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1

            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListMangaCompleted// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListMangaCompleted// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListMangaCompleted// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListMangaCompleted// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListMangaAll//':
            spisok = self.__db.get_my_list_anime(status='all', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Вся манга {len_spisok}:\nНазвание\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_manga_9_rows(status='all', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0

            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "manga_detail %i NextListMangaAll// %s"},' % (
                    i + 1, anime[4], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListMangaAll// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListMangaAll// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListMangaAll// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListMangaAll// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListMangaWatching//':
            spisok = self.__db.get_my_list_anime(status='watching', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Манги читаю {len(spisok)}:\nНазвание - Кол-во просмотренных эпизодов\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_manga_9_rows(status='watching', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0
            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "manga_detail %i NextListMangaWatching// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListMangaWatching// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListMangaWatching// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListMangaWatching// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListMangaWatching// %i"}]]}' % (
                               k, i)
        elif flag[0] == 'NextListMangaPlaned//':
            spisok = self.__db.get_my_list_anime(status='planned', user_id=user.id)
            len_spisok = len(spisok)
            message = f'Манги запланировано {len(spisok)}:\nНазвание - Кол-во всего эпизодов\n\n'

            i = int(flag[1])
            j = i
            if i < 0:
                i = 0
            spisok = self.__db.get_my_list_anime_9_rows(status='planned', user_id=user.id, index=i)
            keyboard = '{"inline_keyboard": [['
            count = 0
            for anime in spisok:
                message += str(i + 1) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                if count == 3:
                    keyboard = keyboard[:-1] + '],['
                    count = 0
                keyboard += '{"text": %i, "callback_data": "manga_detail %i NextListMangaPlaned// %s"},' % (
                    i + 1, anime[3], flag[1])
                i += 1
                count += 1
            if len(spisok) < 9:
                k = j + 9 - 18
            else:
                k = i - 18
            if i == len_spisok:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Назад", "callback_data": "NextListMangaPlaned// %i"}]]}' % (k)
            elif k < 0:
                keyboard = keyboard[
                           :-1] + '],[{"text": "Далее", "callback_data": "NextListMangaPlaned// %i"}]]}' % (i)
            else:
                keyboard = keyboard[:-1] + '],[{"text": "Назад", "callback_data": "NextListMangaPlaned// %i"},' \
                                           '{"text": "Далее", "callback_data": "NextListMangaPlaned// %i"}]]}' % (
                               k, i)
        keyboard = keyboard[:-2] + ',[{"text": "Main", "callback_data": "%s"}]]}' % 'MainManga//'
        self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=keyboard,
                           message_id=msg_id)

    def get_my_list_anime(self, tg_id: int, flag: str = None, msg_id: int = None):
        user = self.__db.get_user(tg_id=tg_id)
        message = ''
        arr = []
        if flag is None or flag == 'ListAnimeWatching//' or flag == 'Main':
            spisok = self.__db.get_my_list_anime(status='watching', user_id=user.id)
            message = f'Аниме смотрю {len(spisok)}:\nНазвание - Кол-во просмотренных эпизодов\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListAnimeWatching//', all=len(spisok))
        elif flag == 'ListAnimePlaned//':
            spisok = self.__db.get_my_list_anime(status='planned', user_id=user.id)
            message = f'Аниме запланировано {len(spisok)}:\nНазвание - Кол-во всего эпизодов\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') <b>' + anime[4] + '</b>: ' + anime[0] + '\n\b' + anime[1] + ' - ' + str(
                    anime[2]) + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListAnimePlaned//', all=len(spisok), is_planned=True)
        elif flag == 'ListAnimeCompleted//':
            spisok = self.__db.get_my_list_anime(status='completed', user_id=user.id)
            message = f'Аниме просмотренно {len(spisok)}:\nНазвание\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListAnimeCompleted//', all=len(spisok))
        elif flag == 'ListAnimeAll//':
            spisok = self.__db.get_my_list_anime(user_id=user.id, status='all')
            message = f'Все аниме {len(spisok)}:\nНазвание\n\n'
            i = 1
            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + '\n'
                arr.append({'text': i, 'id': anime[4]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListAnimeAll//', all=len(spisok))
        if msg_id is None:
            self.__tg.send_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG)
        elif flag == 'Main':
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG,
                               message_id=msg_id)
        elif len(spisok) == 0:
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_ANIME_LIST_KEYBOARD_TG,
                               message_id=msg_id)
        else:
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=keyboard,
                               message_id=msg_id)

    def filter_planned_anime(self, tg_id: int, msg_id: int, param: str):
        if len(param.split()) == 1:
            message = 'Фильтр Аниме:\n1) Сначала Anons\n2) Сначала Ongoing\n3) Сначала Released\n4) Убрать фильтр'
            keyboard = json.dumps({'inline_keyboard': [[{'text': '1', 'callback_data': 'Filter// 1'}],
                                 [{'text': '2', 'callback_data': 'Filter// 2'}],
                                 [{'text': '3', 'callback_data': 'Filter// 3'}],
                                 [{'text': '4', 'callback_data': 'Filter// 4'}]]})
            self.__tg.edit_msg(chat_id=tg_id, msg=message, reply_markup=keyboard,
                               message_id=msg_id)
        else:
            param = int(param.split()[1])
            if param == 4:
                self.__db.update_user(tg_id=tg_id)
            else:
                self.__db.update_user(tg_id=tg_id, filter_anime=param)
            self.get_my_list_anime(tg_id=tg_id, flag='ListAnimePlaned//', msg_id=msg_id)

    def get_my_list_manga(self, tg_id: int, flag: str = None, msg_id: int = None):
        user = self.__db.get_user(tg_id=tg_id)
        message = ''
        arr = []
        if flag is None or flag == 'ListMangaWatching//' or flag == 'Main':
            spisok = self.__db.get_my_list_manga(status='watching', user_id=user.id)
            message = f'Манга читаю {len(spisok)}:\nНазвание - Кол-во прочитанных глав\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListMangaWatching//', all=len(spisok))
        elif flag == 'ListMangaPlaned//':
            spisok = self.__db.get_my_list_manga(status='planned', user_id=user.id)
            message = f'Манга запланировано {len(spisok)}:\nНазвание - Кол-во всего эпизодов\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + ' - ' + str(anime[2]) + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListMangaPlaned//', all=len(spisok))
        elif flag == 'ListMangaCompleted//':
            spisok = self.__db.get_my_list_manga(status='completed', user_id=user.id)
            message = f'Манга прочитано {len(spisok)}:\nНазвание\n\n'
            i = 1

            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + '\n'
                arr.append({'text': i, 'id': anime[3]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListMangaCompleted//', all=len(spisok))
        elif flag == 'ListMangaAll//':
            spisok = self.__db.get_my_list_manga(user_id=user.id, status='all')
            message = f'Вся Манга {len(spisok)}:\nНазвание\n\n'
            i = 1
            for anime in spisok:
                message += str(i) + ') ' + anime[0] + '/' + anime[1] + '\n'
                arr.append({'text': i, 'id': anime[4]})
                i += 1
                if i == 10:
                    break

            keyboard = self.__generate_3_keyboard(array=arr, param='ListMangaAll//', all=len(spisok))
        if msg_id is None:
            self.__tg.send_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_MANGA_LIST_KEYBOARD_TG)
        elif flag == 'Main':
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_MANGA_LIST_KEYBOARD_TG,
                               message_id=msg_id)
        elif len(spisok) == 0:
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=self.MY_MANGA_LIST_KEYBOARD_TG,
                               message_id=msg_id)
        else:
            self.__tg.edit_msg(chat_id=user.tg_id, msg=message, reply_markup=keyboard,
                               message_id=msg_id)

    def add_users(self, tg_id: int, auth_code: str):
        js: dict = self.__shiki.auth(auth_code=auth_code)
        if not js.get('access_token'):
            self.__tg.send_msg(chat_id=tg_id, msg='Введен неверный Код!')
        else:
            user = self.__shiki.get_info_about_users(js['access_token'])
            self.__db.add_user(tg_id=tg_id, token=js['access_token'], refresh_token=js['refresh_token'],
                               user_id=user['id'])

            self.get_info_my_list_in_shiki(tg_id=tg_id)
            self.__tg.send_msg(chat_id=tg_id, msg='Пользователь добавлен\nВаш список Аниме обновлен!',
                               reply_markup=self.MAIN_KEYBOARD_TG)

    def __init__(self, db: DataBaseManager, tg: Telegram, shiki: Shikimori, context: MainCache):
        self.__db = db
        self.__tg = tg
        self.__shiki = shiki
        self.__context = context
