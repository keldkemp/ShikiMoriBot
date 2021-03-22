import abc


class BaseModel(abc.ABC):
    INT = 'INTEGER '
    BIGINT = 'BIGINT '
    __VARCHAR = 'VARCHAR'
    TEXT = 'TEXT '
    BOOL = 'BOOLEAN '
    DATE = 'DATE '
    DATETIME = 'TIMESTAMP '
    PK = 'PRIMARY KEY '
    __FK = 'FOREIGN KEY '
    __REFERENCES = 'REFERENCES '
    AUTOINCREMENT = 'AUTOINCREMENT '
    DEFAULT = 'DEFAULT '

    __DICT_TYPE_DATA = {'INTEGER': 'int', 'BIGINT': 'int', 'VARCHAR': 'str', 'TEXT': 'str', 'BOOL': 'int', 'DATE': 'datetime',
                        'TIMESTAMP': 'datetime'}

    def VARCHAR(self, n) -> str:
        return self.__VARCHAR + '(' + str(n) + ') '

    def FK(self, attr_name: str, table_name: str, attr_fk_name: str = 'id') -> str:
        return self.__FK + '(' + attr_name + ') ' + self.__REFERENCES + ' ' + table_name + ' (' + attr_fk_name + ') '

    def get_attr(self) -> dict:
        return vars(self)

    def get_data_model(self) -> str:
        attrs = self.get_attr()
        class_name = self.__class__.__name__
        text = f'class {class_name}:\n    def __init__(self, '
        i = 0
        for k, v in attrs.items():
            if k.find('init_data') != -1 or k.find('FK') != -1:
                continue
            attr_type = ''.join(c for c in v if c.isalpha())
            attr_type = attr_type.replace('PRIMARYKEY', '')
            attr_type = self.__DICT_TYPE_DATA.get(attr_type)
            if i == 3:
                text += k + ': ' + attr_type + ' = None,\n                '
                i = 0
            else:
                text += k + ': ' + attr_type + ' = None, '
            i += 1
        text = text[:-2] + '):\n'

        for k, v in attrs.items():
            if k.find('init_data') != -1 or k.find('FK') != -1:
                continue
            text += '        self.' + k + ' = ' + k + '\n'
        return text

    def get_code(self) -> str:
        attr = self.get_attr()
        table_name = self.__class__.__name__
        command = f'CREATE TABLE {table_name} ('
        for k, v in attr.items():
            if k.find('init_data') != -1:
                continue
            if k.find('FK') != -1:
                command += v + ', '
            else:
                command += k + ' ' + v + ', '
        command = command[:-2] + ')'
        return command

    def get_init_data_code(self):
        attr = self.get_attr()
        table_name = self.__class__.__name__
        command = ''
        init_data = attr.get('init_data')
        if init_data is None:
            return None
        for k, v in init_data.items():
            command += f"INSERT INTO {table_name} VALUES ({k}, '{v}'); "
        return command


class SettingsListAnime(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.name = self.VARCHAR(512)
        self.init_data = {1: 'Сортировка по названию', 2: 'Сортировка по дате добавления',
                          3: 'Сортировка по кол-ву просмотренных эпизодов', 4: 'Сортировка по оценкам',
                          5: 'Сортировка по Вашим оценкам', 6: 'Сортировка по дате обновления записей'}


class Users(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.token = self.VARCHAR(512)
        self.refresh_token = self.VARCHAR(512)
        self.tg_id = self.BIGINT
        self.list_settings = self.INT
        self.search = self.VARCHAR(512)
        self.__FK = self.FK(attr_name='list_settings', table_name='SettingsListAnime')


class AnimeTypes(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.name = self.VARCHAR(256)
        self.init_data = {1: 'Anime', 2: 'Manga'}


class AnimeStatus(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.name = self.VARCHAR(256)
        self.init_data = {1: 'completed', 2: 'watching', 3: 'planned'}


class Anime(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.name = self.VARCHAR(4096)
        self.name_ru = self.VARCHAR(4096)
        self.name_jp = self.VARCHAR(4096)
        self.kind = self.VARCHAR(256)
        self.score = self.VARCHAR(128)
        self.status = self.VARCHAR(256)
        self.episodes = self.INT
        self.episodes_aired = self.INT
        self.aired_on = self.DATE
        self.released_on = self.DATE
        self.rating = self.VARCHAR(64)
        self.updated_at = self.DATETIME
        self.next_episode_at = self.DATETIME
        self.description = self.TEXT
        self.url = self.VARCHAR(1024)


class Manga(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.name = self.VARCHAR(4096)
        self.name_ru = self.VARCHAR(4096)
        self.name_jp = self.VARCHAR(4096)
        self.kind = self.VARCHAR(256)
        self.score = self.VARCHAR(128)
        self.status = self.VARCHAR(256)
        self.volumes = self.INT
        self.chapters = self.INT
        self.aired_on = self.DATE
        self.released_on = self.DATE
        self.description = self.TEXT
        self.url = self.VARCHAR(1024)


class UserRates(BaseModel):
    def __init__(self):
        self.id = self.INT + self.PK
        self.user_id = self.INT
        self.target_id = self.INT
        self.target_type = self.INT
        self.score = self.INT
        self.status = self.INT
        self.rewatches = self.INT
        self.episodes = self.INT
        self.volumes = self.INT
        self.chapters = self.INT
        self.text = self.TEXT
        self.created_at = self.DATETIME
        self.updated_at = self.DATETIME
        self.__FK1 = self.FK(attr_name='user_id', table_name='Users')
        self.__FK2 = self.FK(attr_name='target_type', table_name='AnimeTypes')
        self.__FK3 = self.FK(attr_name='status', table_name='AnimeStatus')

