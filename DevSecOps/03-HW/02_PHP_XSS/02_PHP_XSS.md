## PHP XSS Vulnerabilities

### > Запущу образ
docker run -d --name "otus-devsecops-xss" -p 8080:80 ket9/otus-devsecops-xss:latest

### > Посмотрю функционал приложения
http://localhost:8080/

на главной странице доступно 2 ссылки


- <a href="http://localhost:8080/XSS-1">XSS-1</a>
- <a href="http://localhost:8080/index.php">index.php</a>

<br/>при переходе по ссылке "XSS-1" открывается страница с добавлением комментариев
<br/>при переходе по ссылке "index.php" открывается страница по-умолчанию "localhost:8080"

### > Проверю возможность ввода различных комментариев

|#|Комментарий|Результат|
|-|-|-|
|1|комментарий123|комментарий добавлен|
|2|<>&'"|экранирования нет, спец. сиволы отображаются|
|3|\>\<style\>p {color: red}\<\/style\>|возможна модификация стилей html-страницы!<br/><b>Важно!</b> <i>Первая левая угловая скобка необходима для того, чтобы закрыть html-тег, в котором выводится текст комментария</i>|
|4|>\<script>var script = document.createElement('script'); script.type = 'text/javascript'; script.innerHTML = "function load_bro() { document.querySelectorAll('p, hr, script').forEach(item => item.remove()); document.querySelectorAll('input').forEach(item => item.disabled = true); } window.onload=load_bro;"; script.id = "jsxss"; document.head.appendChild(script);\</script>|добавляет скрипт в комментарий, который, в свою очередь будет интегрироваться в head html и при загрузке страницы будет очищать/отключать комментарии...<br/><b>Важно!</b> <i>Первая левая угловая скобка необходима для того, чтобы закрыть html-тег, в котором выводится текст комментария</i>|

### > Примеры CVE с данной уязвимостью


```
<script>alert("This is XSS");</script>
```

Их много...

|#|Code|
|-|-|
|1*|[CVE-2020-5497](https://nvd.nist.gov/vuln/detail/CVE-2020-5497)|
|2|[CVE-2021-46709](https://nvd.nist.gov/vuln/detail/CVE-2021-46709)|
|3|[CVE-2021-32671](https://nvd.nist.gov/vuln/detail/CVE-2021-32671)|
|4|[CVE-2021-3441](https://nvd.nist.gov/vuln/detail/CVE-2021-3441)|
|5*|[CVE-2022-1816](https://nvd.nist.gov/vuln/detail/CVE-2022-1816)|

<br/>

---

### > Предотвращение атаки

- использовать правильное HTML-кодирование спец. символов, в нашем случае (PHP) можно использовать <b>htmlspecialchars</b>
- преобразовать спец. символы, такие как ?, &, /, и пробелы <, > в их соответствующие эквиваленты в кодировке HTML или URL.
- разрешить пользователям отключать клиентские сценарии
- перенаправлять недействительные запросы
- использовать и применять политику безопасности контента (Content Security Policy) для отключения любых функций, которыми можно манипулировать для осуществления атак XSS