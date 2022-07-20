# Анализ уязвимостей в коде Python

### Недочеты в примерах кода

Первым делом автоматически проверю исходный код на наличие уязвимостей
Всего было найдено 2 уязвимости в <b>примере 1</b> ([example-01.py](.\examples\example-01.py))

|tool|filename|test_name|test_id|issue_severity|issue_confidence|issue_cwe|issue_text|line_number|col_offset|line_range|more_info|
|-|-|-|-|-|-|-|-|-|-|-|-|
<b>Bandit</b>|[example-01.py](.\examples\example-01.py)|hardcoded_password_string|B105|LOW|MEDIUM|https://cwe.mitre.org/data/definitions/259.html|Possible hardcoded password: 'F0cUzh8BgYJSLXAU8qDmClM0dE8GJTpsiyVEl3BCqQMCABp1U$f%'|9|11|[9]|https://bandit.readthedocs.io/en/1.7.4/plugins/b105_hardcoded_password_string.html|
<b>SonarCloud</b>|[example-01.py](.\examples\example-01.py)|*Cross-Site Request Forgery (CSRF)||||https://cwe.mitre.org/data/definitions/352|app = Flask('vuln_app') --> app = Flask(\_\_name\_\_)|8|12|-|https://rules.sonarsource.com/python/RSPEC-4502|

---

#### > Пример 1

```python
# Исходный фрагмент кода 1:

from flask import Flask
from mod_api import mod_api

app = Flask('vuln_app')
app.config['SECRET_KEY'] = 'F0cUzh8BgYJSLXAU8qDmClM0dE8GJTpsiyVEl3BCqQMCABp1U$f%'
app.register_blueprint(mod_api, url_prefix='/api')
```

Найденные недостатки:

- секретный ключ передается в открытом виде,
- хардкод для имени экземпляра Flask (<b>'vuln_app'</b>)

В качестве мер противодействия могу предложить следующее:

- спрятать секретный ключ в переменные окружения.
- вместо 'vuln_app' использовать переменную <b>'\_\_name\_\_'</b>

```python
# Исправленный фрагмент кода 1:

from flask import Flask
from mod_api import mod_api

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.register_blueprint(mod_api, url_prefix='/api')
```

---

#### > Пример 2

```python
#!/usr/bin/env python3

# Исходный фрагмент кода 2:

from flask_wtf import Form
from wtforms import TextField

class LoginForm(Form):

    username = TextField('username')
    password = TextField('password')
```

Недостаток заключается в том, что класс <b>TextField</b> отсутствует в библиотке <b>wtforms</b>. Помимо этого пароль не маскируется.
В качестве мер противодейтсвия нужно использовать другие классы для "логина" и "пароля", а именно <b>StringField</b> и <b>PasswordField</b>

```python
#!/usr/bin/env python3

# Исправленный фрагмент кода 2:

from flask_wtf import Form
from wtforms import StringField, PasswordField

class LoginForm(Form):

    username = StringField("username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=6, max=55)])
```

---

#### > Пример 3

```python
#!/usr/bin/env python3

# Исходный фрагмент кода 3:

def post(self):
    username = self.get_argument('username')
    password = self.get_argument('password').encode('utf-8')
    email = self.get_argument('mail')
    try:
        username = username.lower()
        email = email.strip().lower()
        user = User({'username': username, 'password': password, 'email': email, 'date_joined': curtime()})
        user.validate()
        save_user(self.db_conn, user)

    except Exception, e:

        return self.render_template("success_create.html")

```

Недостатки данного фрагмента кода заключаются в следующем:

- пароль записывается в явном виде,
- в исключении (после указания типа исключения; через запятую) присутствует лишняя переменная <b>e</b>,
- при вызове исключения вызывается шаблон страницы о "удачном создании пользователя" (<b>success_create.html</b>)
- получение аргументов из класса <b>self</b> выполнятся вне блока <b>try</b>


В качестве мер противодействия могу предложить:

- (возможно) стоит отказаться от хранения пароля в открытом виде и хранить лишь хэш пароля,
- (возможно) убрать дополнительное изменение кодировки пароля, чтобы сохранить персистентность данных
- (возможно) требуется перенести получение аргументов из класса <b>self</b> в блок <b>try</b>
- при исключении необходимо вызывать шаблон страницы о "не удачном создании пользователя" (<b>failed_create.html</b>)

```python
#!/usr/bin/env python3

# Исправленный фрагмент кода 3:

def post(self):
    try:
        username = self.get_argument('username')
        password = self.get_argument('password')
        email = self.get_argument('mail')
        
        username = username.lower()
        email = email.strip().lower()
        user = User({'username': username, 'password': password, 'email': email, 'date_joined': curtime()})
        user.validate()
        save_user(self.db_conn, user)

    except Exception:

        return self.render_template("failed_create.html")

```

---

#### Django. Предотвращение атак

В фреймворке Django учтены аспекты безопасности:

- Имеет встроенную защиту от большинства типов CSRF-атак
- Имеет функции защиты от XSS-атак
- Имеет функцию автоматического экранирования HTML
- Функция Escape Django экранирует одинарные и двойные кавычки
- Наборы запросов Django защищены от SQL-инъекций, поскольку их запросы создаются с использованием параметризации запросов
- Django содержит защиту от кликджекинга, которая в поддерживающем браузере может предотвратить отображение сайта внутри фрейма
- Для безопасности всегда лучше развернуть веб-приложение или сайт через HTTPS
- Django использует Host-заголовок, предоставленный клиентом, для создания URL-адресов в определенных случаях

#### Описать, как устроено управление пользовательскими сессиями в Django

Django позволяет использовать Session Framework (SF). SF поддерживает, как пользовательские, так и анонимные сессии. Каркас сеанса позволяет (SF) хранить произвольные пользовательские данных для всех пользователей. Данные сеансов хранятся на стороне сервера, а файлы cookie содержат в себе только "session ID" в случае, если не используется обработчик сессий на основе файлов cookie (1). Промежуточное ПО в свою очередь управляет отправкой и получением файлов cookie. Обработчик сессий по-умолчанию хранит данные сессии в БД (2).

Промежуточное ПО позволяет:

- управлять сессиями
- выполнять защиту от подделки межсайтовых запросов
- использовать аутентификацию
- содержание Gzipping

<i>(1) Чтобы использовать сеансы на основе файлов cookie, установите для параметра SESSION_ENGINE значение "django.contrib.sessions.backends.signed_cookies". Данные сеанса будут храниться с использованием инструментов криптографической подписи Django и параметра SECRET_KEY.</i>

<i>(2) Если нужно использовать сеанс, поддерживаемый БД, вам нужно добавить 'django.contrib.sessions' в настройку INSTALLED_APPS.
После настройки установки запустите [manage.py migrate](https://www.geeksforgeeks.org/django-manage-py-migrate-command-python/), чтобы установить единую таблицу базы данных, в которой хранятся данные сеанса.</i>