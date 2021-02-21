import threading
import sys
from time import sleep
from DataBase.dbmanager import DataBaseManager
from DataBase.postgresql import DataBasePg
from Shikimori.shikimori import Shikimori
from Telegram.telegram import Telegram
from Utils.logging import Logging
from Utils.utils import Utils
from mainManager import MainManager
from settings import SettingsTelegram, SettingsDb, SettingsShiki
from Models.models import Users, AnimeTypes, AnimeStatus, Anime, UserRates, SettingsListAnime


def init_db(db):
    db.create_tables(command=SettingsListAnime().get_code())
    db.insert_init(command=SettingsListAnime().get_init_data_code())
    db.create_tables(command=Users().get_code())
    db.create_tables(command=AnimeTypes().get_code())
    db.insert_init(command=AnimeTypes().get_init_data_code())
    db.create_tables(command=AnimeStatus().get_code())
    db.insert_init(command=AnimeStatus().get_init_data_code())
    db.create_tables(command=Anime().get_code())
    db.create_tables(command=UserRates().get_code())


def init_model():
    f = open('Models/dataModels.py', 'w')
    f.write('import datetime\n\n\n' + Users().get_data_model())
    f.write('\n\n' + AnimeTypes().get_data_model())
    f.write('\n\n' + AnimeStatus().get_data_model())
    f.write('\n\n' + Anime().get_data_model())
    f.write('\n\n' + UserRates().get_data_model())
    f.write('\n\n' + SettingsListAnime().get_data_model())
    f.close()


def get_value_in_dict(dc: dict, key: str):
    return str(dc.get(key))


def anime_insert_or_update(anime: dict):
    id = get_value_in_dict(anime, 'id')
    name = get_value_in_dict(anime, 'name')
    russian = get_value_in_dict(anime, 'russian')
    japanese = get_value_in_dict(anime, 'japanese')[2:-2]
    kind = get_value_in_dict(anime, 'kind')
    score = get_value_in_dict(anime, 'score')
    status = get_value_in_dict(anime, 'status')
    episodes = get_value_in_dict(anime, 'episodes')
    episodes_aired = get_value_in_dict(anime, 'episodes_aired')
    aired_on = get_value_in_dict(anime, 'aired_on')
    released_on = get_value_in_dict(anime, 'released_on')
    rating = get_value_in_dict(anime, 'rating')
    updated_at = get_value_in_dict(anime, 'updated_at')
    if updated_at != 'None':
        updated_at = updated_at[:-6]
    next_episode_at = get_value_in_dict(anime, 'next_episode_at')
    if next_episode_at != 'None':
        next_episode_at = next_episode_at[:-6]
    description = get_value_in_dict(anime, 'description').replace("'", ' ')

    command = "INSERT INTO anime VALUES ("
    command += id + ", "
    command += f"'{name}', "
    command += f"'{russian}', "
    command += f"'{japanese}', "
    command += f"'{kind}', "
    command += f"'{score}', "
    command += f"'{status}', "
    command += f"{episodes}, "
    command += f"{episodes_aired}, "
    if aired_on == 'None':
        command += "null, "
    else:
        command += f"to_date('{aired_on}', 'YYYY-mm-dd'), "
    if released_on == 'None':
        command += "null, "
    else:
        command += f"to_date('{released_on}', 'YYYY-mm-dd'), "
    command += f"'{rating}', "
    command += f"to_timestamp('{updated_at}', 'YYYY-mm-ddTHH24:MI:SS.MS')::timestamp without time zone, "
    if next_episode_at == 'None':
        command += "null, "
    else:
        command += f"to_timestamp('{next_episode_at}', 'YYYY-mm-ddTHH24:MI:SS.MS')::timestamp without time zone, "
    command += f"'{description}'"
    command += f") ON CONFLICT (id) DO UPDATE SET name = '{name}', name_ru = '{russian}', name_jp = '{japanese}', " \
               f"kind = '{kind}', status = '{status}', episodes = {episodes}, episodes_aired = {episodes_aired}, "
    if aired_on != 'None':
        command += f"aired_on = to_date('{aired_on}', 'YYYY-mm-dd'), "
    if released_on != 'None':
        command += f"released_on = to_date('{released_on}', 'YYYY-mm-dd'), "
    command += f"rating = '{rating}', updated_at = to_timestamp('{updated_at}', 'YYYY-mm-ddTHH24:MI:SS.MS')::timestamp without time zone, "
    if next_episode_at != 'None':
        command += f"next_episode_at = to_timestamp('{next_episode_at}', 'YYYY-mm-ddTHH24:MI:SS.MS')::timestamp without time zone, "
    command += f"description = '{description}';"
    return command


def insert_or_update_anime_list(db, shiki, anime_list):
    command_user_rates = ''
    command_anime_detail = ''
    for obj in anime_list:
        if obj.get('target_type') == 'Manga':
            continue
        try:
            anime_detail = shiki.get_anime_info(id_anime=obj.get('target_id'))
            command_anime_detail += anime_insert_or_update(anime_detail)
        except Exception as e:
            sleep(1)
            while True:
                try:
                    anime_detail = shiki.get_anime_info(id_anime=obj.get('target_id'))
                    command_anime_detail += anime_insert_or_update(anime_detail)
                    break
                except Exception as e:
                    sleep(60)
    db.insert_init(command_anime_detail)
    db.insert_init(command_user_rates)


def private_msg(result):
    call_back_id = None
    try:
        last_text = result[0]['message']['text']
        last_chat_id = result[0]['message']['chat']['id']
        message_id = result[0]['message']['message_id']
    except:
        try:
            last_text = result[0]['callback_query']['data']
        except:
            return 0
        last_chat_id = result[0]['callback_query']['message']['chat']['id']
        call_back_id = result[0]['callback_query']['id']
        message_id = result[0]['callback_query']['message']['message_id']

    # Запускаем потоки
    threading.Thread(target=razbor, args=(last_chat_id, call_back_id, last_text, message_id)).start()


def razbor(last_chat_id, call_back_id, last_text, message_id):
    if DBManager.is_user(tg_id=int(last_chat_id)):
        if last_text.lower().find('список') != -1:
            mainManager.get_my_list_anime(tg_id=last_chat_id)
        elif last_text.find('anime_similar') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.get_anime_similar(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
        elif last_text.find('add_user_rate') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.add_anime_in_my_list(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('anime_search') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.search_anime_result(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('search') != -1 or last_text.find('Search') != -1:
            if last_text.find('search//') != -1:
                telegram.answer_callback(call_back_id)
                mainManager.search_anime_in_shiki(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
            else:
                mainManager.search_anime_in_shiki(tg_id=last_chat_id, msg=last_text)
        elif last_text.find('addEpisodes//') != -1 or last_text.find('removeEpisodes//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.edit_user_rates(tg_id=last_chat_id, command=last_text, message_id=message_id)
        elif last_text == 'Main//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, msg_id=message_id, flag='Main')
        elif last_text == 'ListAnimePlaned//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, flag='ListAnimePlaned//', msg_id=message_id)
        elif last_text == 'ListAnimeWatching//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, msg_id=message_id)
        elif last_text == 'ListAnimeCompleted//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, flag='ListAnimeCompleted//', msg_id=message_id)
        elif last_text == 'ListAnimeAll//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, flag='ListAnimeAll//', msg_id=message_id)
        elif last_text.find('anime_detail') != -1:
            telegram.answer_callback(call_back_id)
            ls = last_text.split(' ')
            mainManager.get_info_about_anime(tg_id=last_chat_id, msg_id=message_id,
                                             user_rate_id=int(ls[1]), msg=last_text)
        elif last_text.find('SetScrore//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.edit_user_rates(tg_id=last_chat_id, command=last_text, message_id=message_id)
        elif last_text.find('NextListAnimeCompleted//') != -1 or last_text.find('PreviousListAnimeCompleted//') != -1\
                or last_text.find('NextListAnimeAll//') != -1 or last_text.find('PreviousListAnimeAll//') != -1\
                or last_text.find('NextListAnimeWatching//') != -1 or last_text.find('PreviousAnimeWatching//') != -1\
                or last_text.find('NextListAnimePlaned//') != -1 or last_text.find('PreviousAnimePlaned//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.get_next_list_anime(tg_id=last_chat_id, flag=last_text, msg_id=message_id)
        elif last_text == 'UpdateListAnime//':
            telegram.answer_callback(call_back_id)
            telegram.send_msg(chat_id=last_chat_id, msg='Список аниме обновляется!')
            mainManager.get_info_my_list_in_shiki(tg_id=last_chat_id)
            telegram.edit_msg(chat_id=last_chat_id, message_id=message_id+1, msg='Список аниме обновлен!')
            telegram.delete_msg(chat_id=last_chat_id, message_id=message_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id)
        elif last_text.find('DeleteUserRates//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.delete_anime_list(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
        elif last_text.lower().find('настройки') != -1:
            mainManager.get_settings(tg_id=last_chat_id)
        elif last_text.find('ChangeListSettings//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.set_settings_list(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
        else:
            telegram.send_msg(chat_id=last_chat_id, msg='main', reply_markup=mainManager.MAIN_KEYBOARD_TG)
    elif len(last_text) > 30:
        mainManager.add_users(tg_id=last_chat_id, auth_code=last_text)
    else:
        telegram.send_msg(last_chat_id, f'Необходимо привязать учетку ShikiMori.\nПерейдите по ссылке и '
                                        f'введите авторизационный код:'
                                        f'\n{shiki_url} '
                                        f'\nID: {last_chat_id}')


if __name__ == '__main__':
    threading.stack_size(128 * 1024)
    settings_tg = SettingsTelegram().get_settings_tg()
    settings_db = SettingsDb().get_settings_db()
    settings_shiki = SettingsShiki().get_settings_shiki()
    shiki_url = f'https://shikimori.one/oauth/authorize?client_id={settings_shiki["client_id"]}' \
                f'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=user_rates'
    log = Logging()

    db = DataBasePg(dbname=settings_db['db_name'], user=settings_db['db_user'],
                    password=settings_db['db_password'], host=settings_db['host'])
    telegram = Telegram(token=settings_tg['token'])

    init_db(db=db)
    init_model()

    DBManager = DataBaseManager(db=db)
    mainManager = MainManager(db=DBManager, tg=telegram, shiki=Shikimori(client_id=settings_shiki['client_id'],
                                                                         client_secret=settings_shiki['client_secret'],
                                                                         client_name=settings_shiki['client_name']))

    if (len(sys.argv)) > 1:
        if sys.argv[1] == 'update_anime':
            mainManager.update_anime()
            print('SUCCSES')
            sys.exit()

    offset = None
    call_back_id = None
    admin_id = 453256909

    while True:
        try:
            result = telegram.get_updates(offset=offset)
            if not result:
                continue
            last_update_id = result[0]['update_id']
            offset = last_update_id + 1
        except:
            continue

        try:
            threading.Thread(target=private_msg, args=(result,)).start()
        except Exception as e:
            log.input_log(Utils.get_date_now_sec() + ' ' + str(e))
            continue

