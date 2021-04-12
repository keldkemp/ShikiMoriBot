import threading
import sys
from DataBase.dbmanager import DataBaseManager
from DataBase.postgresql import DataBasePg
from Shikimori.shikimori import Shikimori
from Telegram.telegram import Telegram
from Utils.logging import Logging
from Utils.utils import Utils
from mainManager import MainManager
from settings import SettingsTelegram, SettingsDb, SettingsShiki
from Models.models import Users, AnimeTypes, AnimeStatus, Anime, UserRates, SettingsListAnime, Manga


def init_db(db):
    db.create_tables(command=SettingsListAnime().get_code())
    db.insert_init(command=SettingsListAnime().get_init_data_code())
    db.create_tables(command=Users().get_code())
    db.create_tables(command=AnimeTypes().get_code())
    db.insert_init(command=AnimeTypes().get_init_data_code())
    db.create_tables(command=AnimeStatus().get_code())
    db.insert_init(command=AnimeStatus().get_init_data_code())
    db.create_tables(command=Anime().get_code())
    db.create_tables(command=Manga().get_code())
    db.create_tables(command=UserRates().get_code())


def init_model():
    f = open('Models/dataModels.py', 'w')
    f.write('import datetime\n\n\n' + Users().get_data_model())
    f.write('\n\n' + AnimeTypes().get_data_model())
    f.write('\n\n' + AnimeStatus().get_data_model())
    f.write('\n\n' + Anime().get_data_model())
    f.write('\n\n' + Manga().get_data_model())
    f.write('\n\n' + UserRates().get_data_model())
    f.write('\n\n' + SettingsListAnime().get_data_model())
    f.close()


def get_value_in_dict(dc: dict, key: str):
    return str(dc.get(key))


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
        if last_text.lower().find('список аниме') != -1:
            mainManager.get_my_list_anime(tg_id=last_chat_id)
        elif last_text == 'SearchAnime//' or last_text == 'SearchManga//':
            telegram.answer_callback(call_back_id)
            mainManager.search_main_anime_or_manga(tg_id=last_chat_id, flag=last_text)
        elif last_text.lower().find('список манги') != -1:
            mainManager.get_my_list_manga(tg_id=last_chat_id)
        elif last_text == 'ListMangaWatching//' or last_text == 'ListMangaPlaned//' \
                or last_text == 'ListMangaCompleted//' or last_text == 'ListMangaAll//':
            mainManager.get_my_list_manga(tg_id=last_chat_id, flag=last_text, msg_id=message_id)
            telegram.answer_callback(call_back_id)
        elif last_text.find('anime_similar') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.get_anime_similar(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
        elif last_text.find('manga_similar') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.get_manga_similar(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
        elif last_text.find('add_user_rate_manga') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.add_manga_in_my_list(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('add_user_rate') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.add_anime_in_my_list(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('anime_search') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.search_anime_result(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('manga_search') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.search_manga_result(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
        elif last_text.find('search//+') != -1 or DBManager.get_user_search(tg_id=last_chat_id) == 'anime_search///':
            if last_text.find('search//+') != -1:
                telegram.answer_callback(call_back_id)
                mainManager.search_anime_in_shiki(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
            else:
                mainManager.search_anime_in_shiki(tg_id=last_chat_id, msg=last_text)
        elif DBManager.get_user_search(tg_id=last_chat_id) == 'manga_search///' or last_text.find('search//_') != -1:
            if last_text.find('search//_') != -1:
                telegram.answer_callback(call_back_id)
                mainManager.search_manga_in_shiki(tg_id=last_chat_id, msg_id=message_id, msg=last_text)
            else:
                mainManager.search_manga_in_shiki(tg_id=last_chat_id, msg=last_text)
        elif last_text.find('addEpisodes//') != -1 or last_text.find('removeEpisodes//') != -1 \
                or last_text.find('addVolumes//') != -1 or last_text.find('removeVolumes//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.edit_user_rates(tg_id=last_chat_id, command=last_text, message_id=message_id)
        elif last_text == 'Main//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_anime(tg_id=last_chat_id, msg_id=message_id, flag='Main')
        elif last_text == 'MainManga//':
            telegram.answer_callback(call_back_id)
            mainManager.get_my_list_manga(tg_id=last_chat_id, msg_id=message_id, flag='Main')
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
        elif last_text.find('manga_detail') != -1:
            telegram.answer_callback(call_back_id)
            ls = last_text.split(' ')
            mainManager.get_info_about_manga(tg_id=last_chat_id, msg_id=message_id,
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
        elif last_text.find('NextListMangaCompleted//') != -1 or last_text.find('PreviousListMangaCompleted//') != -1\
                or last_text.find('NextListMangaAll//') != -1 or last_text.find('PreviousListMangaAll//') != -1\
                or last_text.find('NextListMangaWatching//') != -1 or last_text.find('PreviousMangaWatching//') != -1\
                or last_text.find('NextListMangaPlaned//') != -1 or last_text.find('PreviousMangaPlaned//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.get_next_list_manga(tg_id=last_chat_id, flag=last_text, msg_id=message_id)
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
        elif last_text.find('DeleteUserRatesManga//') != -1:
            telegram.answer_callback(call_back_id)
            mainManager.delete_manga_list(tg_id=last_chat_id, msg=last_text, msg_id=message_id)
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
            mainManager.update_anime_and_manga()
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

