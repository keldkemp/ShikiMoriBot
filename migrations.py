import json
import Models
import os
from DataBase.postgresql import DataBasePg
from Models.migrationsDto import MigrationsDto


class MigrationsDb:
    __TABLE_NAME = 'migrations'
    __FOLDER = './Migrations'
    __MODELS = 'Models.models'
    __ALL = False

    @staticmethod
    def generate_migration_file():
        base_structure = '{\n "name": "",\n "author": "",\n "type": "class/sql",\n "command": ' \
                         '"all/classes/class/sql"\n} '
        folder = './Migrations'
        file_name = ''
        time = 0.0
        for file in os.listdir(folder):
            if time < os.path.getmtime(folder + '/' + file):
                time = os.path.getmtime(folder + '/' + file)
                file_name = file
        if file_name == '':
            file_name = '____-1____migrations.json'
        num = file_name.replace('____', '')
        num = num.replace('migrations.json', '')
        num = str(int(num) + 1)

        while len(num) < 4:
            num = '0' + num

        migration_name = f'____{num}____migrations.json'
        file = open(folder + '/' + migration_name, 'w')
        file.write(base_structure)
        file.close()
        pass

    def __init_data_model(self):
        f = open('Models/dataModels.py', 'w')
        f.write('import datetime\n')
        for _, model in Models.list_models.items():
            f.write('\n\n' + model.get_data_model())
        f.close()

    def run(self):
        migrations = self.__get_all_migrations()
        for migration in migrations:
            if not self.__ALL:
                self.__run_migrate(migration)
            else:
                self.__put_migrate(migration)
        if len(migrations) > 0:
            self.__init_data_model()

    def __json_to_dto(self, json: dict, file_name: str) -> MigrationsDto:
        return MigrationsDto(file_name=file_name, name=json.get('name'), author=json.get('author'),
                             type=json.get('type'), command=json.get('command'))

    def __migrations_is_not_run(self, migrations: list):
        pass

    def __get_migrations_db(self) -> list[MigrationsDto]:
        dto_list = []
        ls = self.__db.select_all(self.__TABLE_NAME)
        for l in ls:
            dto_list.append(MigrationsDto(file_name=l[0], name=l[1], author=l[2], type=l[3], status=l[4]))
        return dto_list

    def __get_migrations_in_os(self) -> list[MigrationsDto]:
        dto_list = []
        for file in os.listdir(self.__FOLDER):
            f = open(self.__FOLDER + '/' + file)
            dto_list.append(self.__json_to_dto(json.loads(f.read()), file))
            f.close()
        return dto_list

    def __get_all_migrations(self) -> list:
        migrations_in_db = self.__get_migrations_db()
        migrations_in_os = self.__get_migrations_in_os()
        name_db = [item.file_name for item in migrations_in_db]
        uniq_migrations = [item for item in migrations_in_os if item.file_name not in name_db]
        return uniq_migrations

    def __get_new_column(self):
        pass

    def __run_class_migrate(self, migration: MigrationsDto):
        if migration.command == 'all':
            if self.__db.select("select count(*) from information_schema.tables where table_name = 'users'")[0][0] == 1:
                return 1
            self.__ALL = True
            for _, model in Models.list_models.items():
                self.__db.migration(model.get_code())
        else:
            self.__db.migration(Models.list_models.get(migration.command).get_code())

    def __run_sql_migrate(self, migration: MigrationsDto):
        self.__db.migration(migration.command)

    def __put_migrate(self, migration: MigrationsDto):
        self.__db.insert_init(f"INSERT INTO {self.__TABLE_NAME} VALUES ('{migration.file_name}', '{migration.name}', "
                              f"'{migration.author}', '{migration.type}', 1);")

    def __run_migrate(self, migration: MigrationsDto):
        if migration.type == 'class':
            self.__run_class_migrate(migration)
        elif migration.type == 'sql':
            self.__run_sql_migrate(migration)
        else:
            raise Exception(f'Migration {migration.file_name} type is incorrect')
        self.__put_migrate(migration)
        return 1

    def __create_table_migrations(self):
        self.__db.create_tables(f'CREATE TABLE IF NOT EXISTS {self.__TABLE_NAME} '
                                f'(file_name varchar(1024) NOT NULL, name varchar(1024) NOT NULL, '
                                f'author varchar(1024) NOT NULL, type varchar(1024) NOT NULL, '
                                f'status integer NOT NULL DEFAULT 0)')

    def get_table_name(self):
        return self.__TABLE_NAME

    def __init__(self, db: DataBasePg):
        self.__db = db
        self.__create_table_migrations()
