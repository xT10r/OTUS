## Анализ уязвимостей в коде Python

#### Инструменты для поиска уязвимостей


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
После настройки установки запустите manage.py migrate, чтобы установить единую таблицу базы данных, в которой хранятся данные сеанса.</i>