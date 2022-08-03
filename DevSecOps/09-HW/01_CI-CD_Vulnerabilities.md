# Обеспечение безопасности CI/CD тулчейна и DevOps процесса

В ходе практической работы необходимо выявить все секреты из репозитория GIT
Адрес репо: https://github.com/OtusTeam/DevSecOps_secret-finding.git

---

### > Установлю для выполнения практической работы инструмент TruffleHog

Домашняя страница [ссылка 1](https://github.com/dxa4481/truffleHog), [ссылка 2](https://github.com/trufflesecurity/trufflehog)

><i>Данный инструмент выполняет поиск паролей, ключей и других чувствительных данных по репозиториям <b>git</b>.
Для идентификации секретов ищет строки с высокой энтропией, анализирует историю изменений кода и ветви.
Этот инструмент эффективен для поиска случайно сохранённых в исходном коде паролей и ключей, даже если впоследствии они были убраны.
<b>TruffleHog</b> пройдёт по всей истории изменений (комитов) каждой ветви и проверит каждое различие (diff) от каждого изменения кода и будет искать в них пароли и ключи.
Поиск выполняется как по регулярным выражениям, так и с расчётом энтропии. Для проверок энтропии, truffleHog будет вычислять [энтропию Шэннона (Shannon)](https://ru.wikipedia.org/wiki/%D0%AD%D0%BD%D1%82%D1%80%D0%BE%D0%BF%D0%B8%D1%8F) для набора символов base64 и набора шестнадцатеричных символов для каждого фрагмента текста более длиной более 20 символов, состоящего из этих наборов символов в каждом diff (различии текста). Если на любой точке выявлена строка с высокой энтропией и длиной более 20 символов, то она будет выведена на экран.</i>

### > Подготовлю Dockerfile для создания образа с необходимыми пакетами

Этот файл образа упрощает подготовку к выполнению практической работе
В данном варианте будет установлен пакет [truffleHog 2.2.1](https://pypi.org/project/truffleHog/2.2.1/) через Pip, т.к. на момент выполнения практической работы этот пакет является последней версией

```Dockerfile
FROM python:buster

ENV PATH /home/trufflehog/.local/bin:$PATH

LABEL authors="HW-09" \
   description="Docker python image"

RUN apt-get update; \
    update-ca-certificates; \
    apt-get install -qq -y nano git \
    && apt-get install -qq -f \
    && apt-get clean; \
    rm -f /var/lib/apt/lists/* 2> /dev/null; \
    pip install --upgrade pip

RUN groupadd -g 2000 trufflehog; \
    useradd -rm -d /home/trufflehog -s /bin/bash -g trufflehog -u 2001 trufflehog

USER trufflehog

RUN pip install truffleHog -q --exists-action i

EXPOSE 8080
```

### > Подготовлю (временный) sh-скрипт для создания образа и запуска контейнера

Задачи скрипта:

- создать временный каталог (с полными правами, 777; /tmp/hw9-otus)
- собирать образ,
- запустить контейнер,
- выполнить маппинг порта 8080 на порт 8080 внутри контейнера,
- смонтировать volume с хоста в контейнер (по пути /tmp/hw9-otus)

```bash
#!/bin/bash

mkdir -p /tmp/hw9-otus
chmod 777 /tmp/hw9-otus

docker build --rm -t "hw9-otus:v1" .
docker run --rm --name "hw9-otus" -ti -p 8080:8080 -v /tmp/hw9-otus:/tmp/hw9-otus/ hw9-otus:v1 /bin/bash
```

### > Вариант 1. Запущу sh-скрипт и в консоли bash запущенного контейнера выполню сканирование репозитория

Из команды ниже будет получен большой объем данных, который необходимо проанализировать (файл /tmp/hw9-otus/log.txt)

```bash
trufflehog https://github.com/OtusTeam/DevSecOps_secret-finding.git | tee -a /tmp/hw9-otus/log.txt
```

### > Вариант 2. Запущу подготовленный образ с trufflehog последней версии (переписанной на Go)

Из команды ниже с будет получен не большой объём данных (в основном пароли и ключи) для дальнейшего анализа (файл /tmp/hw9-otus2/log.txt)

```bash
sudo docker run --rm -it -v /tmp/hw9-otus2:/tmp/hw9-otus2/ trufflesecurity/trufflehog:latest git --concurrency=10 https://github.com/OtusTeam/DevSecOps_secret-finding.git | tee -a /tmp/hw9-otus2/log.txt
```

### > Найденные секреты

1. Раскрыт приватный ключ
Ключи в явном виде должны храниться в хранилищах (например Vault by HashiCorp), так же можно использовать любое другое хранилище секретов

```log
Detector Type: PrivateKey
Raw result: -----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCpuOH6AnMc/xdJ
Fo/8z5j+MTLS1yVHANOgQgAxrIczt9uS9vi9UtE0377fL0TQs5Uo97rSuS6ZJ0ac
WKhNEMBFhR3unINs1FC9PzEjI7UDnSacZNg19eCsAn8hdO88TTt5YhIsPZyg0E29
KbzuLiBhSaKFmnmGbh+T4l9ZIy/t1BcOfzFOpvhEMIriRgA3asZpg8CnNosvbO2A
lZ6Z7nFOibJ1hrzQQgl2Ev+nf5VRxo34UGGbF+65mCGFmBvOYn+IbsciADT+2/4T
gr3aVWD5zwn2NRQI5FKpFePVArpfI85Lxt4eHYzpTWI5dYd++H1BesjoT0ZEM0DP
IVfvMN4XAgMBAAECggEAfkD6WXDZEQjx2XzfP8FunikbFZzWLit/QgfW/RzKtr5e
qMTv5GZnGl4XLw+KsXXlz8P5RihbcbK15DhPeoSrgwuzaH0lhx+psB4B/5HgZf/R
aSXbcMiniU2SJOFH1iPdyj4aJq7uhPJv4ffag5PsonKUY662GDpzYx9SroxuawvU
kUyHGnXP+QN3obFbHUqVx72GhwbyvKUXU4wMdQob+QRmB1excNCGVoGDfKVVOev6
S38+rDCbHo0gK+4UF4ljlJAhbZwQTvv7LoXJu27kUlAvGObjFY8hfbs9T2BStnmh
8D87TMp77gAhymqB+OS6OQrbnO/4HG7L+hgougmfgQKBgQDXYycFMwRoR4qyeKNa
mGxQghvsfJdaWO2axS5RikPi5YkpIfYwuUKLL/niRwCslBz20iFihIJS2dWuOLYD
OqAXUbUDAMbjYioWoMNDp6D3Y3eqSkmMAU3Ra+qBusQmp0Ffcr0GNL5xnsu1nmO+
jOOBZ7YD5Hry5oIjvfDmBMTumwKBgQDJuXQbGYz/0d12Feg616zyqDUXcLSQWK7F
nz1140VPdwfvWHMYWomUats5yMxycuGGDe/DH779rKJHT9U9xGsjlSQvLex0QMy8
ddn7vvfLoPzhQx6NAVvobaobY2+MSgJmOedrd2n7p/RGTTSAwdIsghy2BNxdYgZD
P4uBMf3oNQKBgQDIS7OQuTXDB6yqdVdru00WvTfcfqx9Xy9ueymsuEiTKuOXdbas
7ss8Bpx5WY/97SrWOOjE5fcPtvVoM+LHM/CGXvxW05UhBTugmVWch7k/9ablnHmy
kc/dDV8hzx3z2BwJ9/hiWhA0Nvi3Z5jYLcqvn1N7YTEYy1WAiXUJYqwEOwKBgQCM
m3D7pr6qXi1Arxp1UXoile6TzSJ+7uG7rDhZ4LWiIzTrtzpaglkdk7IFQBqJt9vM
5g/2cT1ecqOWk2XurOeFIOLc4+TKT5Sl1HvBxyXP0QITPgaggI8AntgQSSoqnje3
66qMNOsx16skCZKMIQ2Pqo26rf6wNLBq1XM29ZKm9QKBgGeefgyYgirI1TdjpqVk
B5GhVf+D4wozBvJFAwmVBAQFFU1wCJV7aiwT/RL9KP21Ahfil5Ll7OHE80S4yRU2
g5Y5/F3ExwrIUWdnnMgsO3VtmpgBR5ADBbMQ2Wyo8VF9+tENtlFfnRDRFZl09x1H
oX44T7mclitCYaOuoRnC2V5H
-----END PRIVATE KEY-----
File: webgoat-server/privatekey.key
Email: lookatshow.a@yandex.ru
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2021-11-22 23:20:34 +0700 +0700
Line: 1
Commit: 34f1faad298b13e515a62330f593dac142506789
```

2. Раскрыт логин/пароль подключения к БД postgresql (webgoat/webgoat)
Лучше хранить логин/пароль в качестве параметров к запросу и заполнять их на момент обращения к БД

```log
Detector Type: JDBC
Raw result: jdbc:postgresql://webgoat_db:5432/webgoat?user=webgoat&password=webgoat
File: docker-compose-postgres.yml
Email: syl20j@gmail.com
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2019-05-13 11:25:38 +0200 +0200
Line: 10
Commit: bc0d803123f5cd5e3f3e857398b8f2b0c4aad5b9
---

Detector Type: JDBC
Raw result: jdbc:postgresql://webgoat_db:5432/webgoat
      - spring.datasource.username=webgoat
      - spring.datasource.password=webgoat
File: docker-compose-postgres.yml
Email: nanne.baars@owasp.org
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2018-05-01 21:58:43 +0200 +0200
Line: 1
Commit: 0e160c19f5b047c4f416548dacca74852c5eb166
```

3. Раскрыт логин/пароль подключения к БД mysql (root/без пароля, sa/без пароля)

Лучше хранить логин/пароль в качестве параметров к запросу и заполнять их на момент обращения к БД
Помимо этого странно, что вообще пользователь <b>root/sa</b> не имеют пароля

```log
Detector Type: JDBC
Raw result: jdbc:mysql://localhost/testdb",\n   "user" : "root",\n   "password" : ""\n
File: src/main/webapp/js/ace/worker-xquery.js
Email: dave.cowden@gmail.com
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2014-08-24 13:25:41 -0400 -0400
Line: 1
Commit: 0c28f06d63d6e8f15c95737dc0c17da67a3111cf

---

Detector Type: JDBC
Raw result: jdbc:sqlserver://192.168.1.1;databaseName=testdb",\n   "user" : "sa",\n   "password" : ""\n
File: src/main/webapp/js/ace/worker-xquery.js
Email: dave.cowden@gmail.com
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2014-08-24 13:25:41 -0400 -0400
Line: 1
Commit: 0c28f06d63d6e8f15c95737dc0c17da67a3111cf
```

4. Раскрыт логин/пароль подключения к БД mysql (test/test)

```log
Detector Type: JDBC
Raw result: jdbc:mysql://localhost/authority"
         connectionName="test" connectionPassword="test"
File: webgoat-5.4/src/main/scripts/server_8080.xml
Email: mayhew64@gmail.com@4033779f-a91e-0410-96ef-6bf7bf53c507
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2012-09-09 21:53:44 +0000 UTC
Line: 1
Commit: 68b80fa14f8c2ece71df20ac0a3e3e710bbcd368
```

5. Раскрыт логин/пароль к web-ресурсу attack (guest/guest)

Возможно так и было задумано, что web-ресурс attack должен использоваться исключительно учеткой guest.
Но лучше использовать стандартные методы авторизации (API ключи, Basic, HMAC, OAuth 2.0...), использовать заголовки запросов

```log
Detector Type: URI
Raw result: http://guest:guest@127.0.0.1/WebGoat/attack
File: webgoat-5.4/src/main/scripts/webgoat.sh
Email: mayhew64@gmail.com@4033779f-a91e-0410-96ef-6bf7bf53c507
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2012-09-09 21:53:44 +0000 UTC
Line: 43
Commit: 68b80fa14f8c2ece71df20ac0a3e3e710bbcd368
```

6. Раскрыт токен для Github

Могу предположить, что это просто невнимальность программиста.
Можно изменить токен Github, чтобы текущий потерял актуальность.

```log
Detector Type: High Entropy
Raw result:              Team WebGoat
         env:
-          GITHUB_TOKEN: cee3257f0e59d1d4975a35429cffc3d8b5fabe15ca2e9d47243cbc446d4894a5
+          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

       - name: "Set up QEMU"
         uses: docker/setup-qemu-action@v1.1.0


File: .github/workflows/release.yml
Branch: origin/develop
Repository: https://github.com/OtusTeam/DevSecOps_secret-finding.git
Timestamp: 2021-11-22 16:20:34 +0000 UTC
Line: 75
Commit: 34f1faad298b13e515a62330f593dac142506789
```

7. Раскрыт токен
  
Возможно это токен для "завершения процесса". Используется в тестах.
Скорее всего ничего критичного, но лучше токен генерировать в начале сессии программы, чтобы затем его использовать во всех процессах

```log
Detector Type: High Entropy
Raw result: 
     @Test
-    void wrongVersion() throws Exception {
+    public void wrongVersion() throws Exception {
         String token = "rO0ABXNyADFvcmcuZHVtbXkuaW5zZWN1cmUuZnJhbWV3b3JrLlZ1bG5lcmFibGVUYXNrSG9sZGVyAAAAAAAAAAECAANMABZyZXF1ZXN0ZWRFeGVjdXRpb25UaW1ldAAZTGphdmEvdGltZS9Mb2NhbERhdGVUaW1lO
0wACnRhc2tBY3Rpb250ABJMamF2YS9sYW5nL1N0cmluZztMAAh0YXNrTmFtZXEAfgACeHBzcgANamF2YS50aW1lLlNlcpVdhLobIkiyDAAAeHB3DgUAAAfjCR4GIQgMLRSoeHQACmVjaG8gaGVsbG90AAhzYXlIZWxsbw";
         mockMvc.perform(MockMvcRequestBuilders.post("/InsecureDeserialization/task")
+                .header("x-request-intercepted", "true")
                 .param("token", token))
                 .andExpect(status().isOk())
                 .andExpect(jsonPath("$.feedback", CoreMatchers.is(messages.getMessage("insecure-deserialization.invalidversion"))))
@@ -60,22 +64,27 @@ class DeserializeTest extends AssignmentEndpointTest {
     }
File: webgoat-lessons/insecure-deserialization/src/test/java/org/owasp/webgoat/deserialization/DeserializeTest.java
Branch: origin/develop
Timestamp: 2021-11-16 15:33:36 +0000 UTC
Line: 54
Commit: 20d7015dff255683ef76252e2bcd7a51a0bc67b8 / Move unit test to JUnit 5
```