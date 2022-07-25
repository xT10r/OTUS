# Анализ уязвимостей в коде С/С++

## Подготовка рабочей среды

- [Установить Docker](https://docs.docker.com/engine/install/) (при необходимости)
- Скачать образ <b>sdukshis/devsecops_homework</b> с DockerHub

```
docker pull sdukshis/devsecops_homework
```

- Создать и запустить контейнер из скачанного образа

```
docker run --rm -ti sdukshis/devsecops_homework
```

- В открывшейся консоли склонировать репозиторий с примерами для практической работы

```
git clone https://github.com/sdukshis/devsecops-homework.git
```

- Перейти в каталог репозитория

```
cd devsecops-homework
```

С помощью code review, статического и динамического анализа найдите все уязвимости в директории src Используйте примеры и задания с вебинара
В чат по ДЗ скопируйте отчет в виде таблицы: имя файла | номер строки | тип уязвимости

## Статический анализ кода

### clang-tidy / cppcheck

```
cppcheck --xml --xml-version=2 --enable=all ./src/*.c --output-file=report-cppcheck.xm
```

```
clang-tidy ./src/*.c -checks=-*,clang-analyzer-*,cert-*
```

### Результаты проверок

|File name|Line number|Vulnerability<br>(CWE)|Description|
|-|-|-|-|
|src/board.c|38|401|Memory leak: board|
|src/board.c|36|563|Variable 'board' is assigned a value that is never used|
|src/free.c|8|415|Memory pointed to by 'ptr' is freed twice|
|src/html.c|36|771|Return value of allocation function 'copy_input' is not stored|
|src/html.c|38|771|Return value of allocation function 'copy_input' is not stored|
|src/packet.c|18|571|Condition 'nresp>0' is always true|
|src/packet.c|25|570|Condition 'nresp>0' is always false|
|src/packet.c|29|415|Memory pointed to by 'response' is freed twice|
|src/packet.c|19|570|Argument 'nresp*sizeof(char*)' to function malloc is always 987648|
