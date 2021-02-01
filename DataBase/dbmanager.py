from DataBase.postgresql import DataBasePg
from Models.dataModels import *
import hashlib


class DataBaseManager:
    def get_attr_by_sort(self, user_id: int):
        res = self.__db.select(f'SELECT list_settings FROM users WHERE id = {user_id}')[0]
        if res[0] == 1:
            attr = 'a.name'
        elif res[0] == 2:
            attr = 'r.created_at desc'
        elif res[0] == 3:
            attr = 'r.episodes desc'
        elif res[0] == 4:
            attr = 'a.score desc'
        elif res[0] == 5:
            attr = 'r.score desc'
        else:
            attr = None
        return attr

    def get_settings_list(self, id: int = None) -> list[SettingsListAnime]:
        ls = []
        if id is None:
            res = self.__db.select('SELECT * FROM settingslistanime')
            for l in res:
                ls.append(SettingsListAnime(id=l[0], name=l[1]))
            return ls
        else:
            res = self.__db.select(f'SELECT * FROM settingslistanime WHERE id = {id}')
            for l in res:
                ls.append(SettingsListAnime(id=l[0], name=l[1]))
            return ls

    def set_settings_list(self, tg_id: int, list_settings: int):
        self.__db.insert_init(f'UPDATE users SET list_settings = {list_settings} WHERE tg_id = {tg_id}')

    def get_anime_id_list_for_update(self) -> list:
        res = self.__db.select("SELECT id FROM anime WHERE status <> 'released'")
        ls = []
        for l in res:
            ls.append(l[0])
        return ls

    def delete_token_user(self, id: int):
        self.__db.insert_init(f'UPDATE users SET token = null, refresh_token = null WHERE id = {id}')

    def delete_anime_in_user_rates(self, user_rates_id: int):
        self.__db.insert_init(f'DELETE FROM userrates WHERE id = {user_rates_id}')

    def get_info_anime(self, id: int) -> Anime:
        res = self.__db.select(f'SELECT * FROM anime WHERE id = {id}')[0]
        return Anime(id=res[0], name=res[1], name_ru=res[2], name_jp=res[3], kind=res[4], score=res[5], status=res[6],
                     episodes=res[7], episodes_aired=res[8], aired_on=res[9], released_on=res[10], rating=res[11],
                     updated_at=res[12], next_episode_at=res[13], description=res[14])

    def get_info_user_rate(self, id: int) -> UserRates:
        res = self.__db.select(f'SELECT * FROM userrates WHERE id = {id}')[0]
        return UserRates(id=res[0], user_id=res[1], target_id=res[2], target_type=res[3], score=res[4],
                         status=res[5], rewatches=res[6], episodes=res[7], volumes=res[8], chapters=res[9],
                         text=res[10], created_at=res[11], updated_at=res[12])

    def get_my_list_anime(self, user_id: int, status: str = None):
        attr = self.get_attr_by_sort(user_id=user_id)
        if status is None:
            res = self.__db.select(f'SELECT a.name, a.name_ru, r.episodes, r.id '
                                   f'FROM userrates r, animestatus s, anime a '
                                   f'WHERE r.user_id = {user_id} '
                                   f'and a.id = r.target_id '
                                   f'and r.status = s.id '
                                   f'order by {attr}')
        elif status == 'watching':
            res = self.__db.select(f"SELECT a.name, a.name_ru, r.episodes, r.id "
                                   f"FROM userrates r, animestatus s, anime a "
                                   f"WHERE a.id = r.target_id and r.user_id = {user_id} "
                                   f"and r.status = s.id and s.name = '{status}' "
                                   f"order by {attr}")
        elif status == 'planned':
            res = self.__db.select(f"SELECT a.name, a.name_ru, a.episodes, r.id "
                                   f"FROM userrates r, animestatus s, anime a "
                                   f"WHERE a.id = r.target_id and r.user_id = {user_id} "
                                   f"and r.status = s.id and s.name = '{status}' "
                                   f"order by {attr}")
        elif status == 'completed':
            res = self.__db.select(f"SELECT a.name, a.name_ru, a.episodes, r.id "
                                   f"FROM userrates r, animestatus s, anime a "
                                   f"WHERE a.id = r.target_id and r.user_id = {user_id} "
                                   f"and r.status = s.id and s.name = '{status}' "
                                   f"order by {attr}")
        else:
            res = self.__db.select(f"SELECT a.name, a.name_ru, a.episodes, r.episodes, r.id "
                                   f"FROM userrates r, animestatus s, anime a "
                                   f"WHERE a.id = r.target_id and r.user_id = {user_id} "
                                   f"and r.status = s.id "
                                   f"order by {attr}")
        return res

    def is_anime_in_bd(self, anime_id: int) -> bool:
        res = self.__db.select(f"SELECT * FROM anime where id = {anime_id}")
        if not res:
            return False
        else:
            return True

    def insert_or_update_anime_detail(self, list_anime: list):
        command = ''
        for anime in list_anime:
            command += f"INSERT INTO anime VALUES ({anime.id}, '{anime.name}', '{anime.name_ru}', '{anime.name_jp}', " \
                       f"'{anime.kind}', '{anime.score}', '{anime.status}', {anime.episodes}, {anime.episodes_aired}, "
            if anime.aired_on is None:
                command += "null, "
            else:
                command += f"to_date('{anime.aired_on}', 'YYYY-mm-dd'), "
            if anime.released_on is None:
                command += "null, "
            else:
                command += f"to_date('{anime.released_on}', 'YYYY-mm-dd'), "
            command += f"'{anime.rating}', "
            if anime.updated_at is None:
                command += "null, "
            else:
                command += f"to_timestamp('{anime.updated_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone,"
            if anime.next_episode_at is None:
                command += "null, "
            else:
                command += f"to_timestamp('{anime.next_episode_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone,"
            command += f"'{anime.description}') ON CONFLICT (id) DO UPDATE SET " \
                       f"name = '{anime.name}', name_ru = '{anime.name_ru}', name_jp = '{anime.name_jp}', " \
                       f"kind = '{anime.kind}', score = '{anime.score}', status = '{anime.status}', " \
                       f"episodes = {anime.episodes}, episodes_aired = {anime.episodes_aired}, rating = '{anime.rating}', " \
                       f"description = '{anime.description}'"
            if anime.updated_at is not None:
                command += f", updated_at = to_timestamp('{anime.updated_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone"
            if anime.aired_on is not None:
                command += f", aired_on = to_date('{anime.aired_on}', 'YYYY-mm-dd')"
            if anime.released_on is not None:
                command += f", released_on = to_date('{anime.released_on}', 'YYYY-mm-dd')"
            if anime.next_episode_at is not None:
                command += f", next_episode_at = to_timestamp('{anime.next_episode_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone"
            command += ";"
        self.__db.insert_init(command)

    def insert_or_update_anime_list(self, list_anime: list, flag: str = None):
        command = ''
        ids = '('
        for anime in list_anime:
            ids += f"{anime.id},"
            command += f"INSERT INTO userrates VALUES ({anime.id}, {anime.user_id}, {anime.target_id}, " \
                       f"{anime.target_type}, {anime.score}, {anime.status}, {anime.rewatches}, {anime.episodes}, " \
                       f"{anime.volumes}, {anime.chapters},"
            if anime.text is None or anime.text == 'None':
                command += " null, "
            else:
                command += f"'{anime.text}', "
            command += f"to_timestamp('{anime.created_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone, " \
                       f"to_timestamp('{anime.updated_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone) " \
                       f"ON CONFLICT (id) DO UPDATE SET " \
                       f"score = {anime.score}, status = {anime.status}, rewatches = {anime.rewatches}, " \
                       f"volumes = {anime.volumes}, chapters = {anime.chapters}, episodes = {anime.episodes}, "
            if anime.text is not None and anime.text != 'None':
                command += f"text = '{anime.text}', "
            command += f"created_at = to_timestamp('{anime.created_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone, " \
                       f"updated_at = to_timestamp('{anime.updated_at}', 'YYYY-mm-dd HH24:MI:SS')::timestamp without time zone;"
        ids = ids[:-1] + ')'
        if flag is None:
            ids_to_delete = self.__db.select(f'SELECT * FROM userrates where id not in {ids}')
            if len(ids_to_delete) != 0:
                ids = ''
                for id_u in ids_to_delete:
                    ids += str(id_u[0]) + ','
                ids = ids[:-1]
                self.__db.insert_init(f'DELETE FROM userrates where id in ({ids})')
        self.__db.insert_init(command)

    def get_type(self, name) -> AnimeTypes:
        res = self.__db.select(f"SELECT * FROM animetypes WHERE name = '{name}'")[0]
        return AnimeTypes(id=res[0], name=res[1])

    def get_status(self, name) -> AnimeStatus:
        res = self.__db.select(f"SELECT * FROM animestatus WHERE name = '{name}'")[0]
        return AnimeStatus(id=res[0], name=res[1])

    def is_user(self, tg_id: int) -> bool:
        user: list = self.__db.select(f'SELECT * FROM USERS where tg_id = {tg_id} and token is not null')
        if not user:
            return False
        else:
            return True

    def get_user(self, tg_id: int = None, user_id: int = None) -> Users:
        if tg_id is not None:
            res = self.__db.select(f'SELECT id, token, refresh_token, tg_id, list_settings FROM USERS WHERE tg_id = {tg_id}')[0]
        else:
            res = self.__db.select(f'SELECT id, token, refresh_token, tg_id, list_settings FROM USERS WHERE id = {user_id}')[0]
        return Users(id=res[0], token=res[1], refresh_token=res[2], tg_id=res[3], list_settings=res[4])

    def add_user(self, tg_id: int, token: str, refresh_token: str, user_id: int):
        self.__db.insert_init(f'INSERT INTO USERS (id, token, refresh_token, tg_id, list_settings) VALUES '
                              f"({user_id}, '{token}', '{refresh_token}', {tg_id}, 2) ON CONFLICT (id) DO UPDATE SET "
                              f"token = '{token}', refresh_token = '{refresh_token}'")

    def __init__(self, db: DataBasePg):
        self.__db = db
