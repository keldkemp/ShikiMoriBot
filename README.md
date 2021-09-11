Бот работает с сайтом https://shikimori.one/

Возможности бота:<br>
1) Показывает твой список аниме (Смотрю, просмотренные, запланированные, все)
2) Возможно ставить оценки
3) Информация о Аниме
4) Франшиза
5) Поиск аниме
6) Добавление в свой список нового аниме
<br>

Настройки:<br>
Бот работает с БД PostgreSQL<br>
1) Необходимо в корне проекта создать файл settings.json:<br>
<code>
{
  "telegram_token": "You Token",<br>
  "db_name": "DataBase_Name",<br>
   "db_user": "DataBase_User",<br>
  "db_password": "DataBase_Password",<br>
  "seed": "Seed, OLD Логика",<br>
  "host": "Host DB",<br>
  "client_id": "id client Shiki",<br>
  "client_secret": "client secret Shiki",<br>
  "client_name": "client name Shiki"
}
</code><br>
Либо использовать переменные окружения:<br>
<code>
'telegram_token'
'DATABASE_URL'
'client_id'
'client_secret'
'client_name'
</code>
   
   