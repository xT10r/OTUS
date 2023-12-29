# Применение защиты для REST-API внутри микро-сервисных приложений и на back-end<br/><i>(на примере анализа Django-проекта)</i>

## Подготовительный этап

- Выполнить клонирование репозитория
- Создать docker-образ
- Запустить контейнер

```
git clone https://github.com/DJWOMS/pysonet
cd pysonet
docker-compose build
docker-compose up
```

Адрес Swagger (после запуска конейтейнера):

- [Ссылка на Swagger](http://127.0.0.1:8000/api/v1/swagger/)
- [Ссылка на Swagger (формат OpenAPI)](http://127.0.0.1:8000/api/v1/swagger/?format=openapi)

---

## Задание

### Внутренний анализ (репозиторий + settings.ру)


### Внешний анализ (OWASP ZAP)

```
docker pull owasp/zap2docker-weekly  
docker run -t owasp/zap2docker-weekly zap-api-scan.py -t http://127.0.0.1:8000/api/v1/swagger/?format=openapi -f openapi
```

```
docker run -t --network=pysonet_default owasp/zap2docker-stable zap-api-scan.py -t http://pysonet_back:8000/api/v1/swagger/?format=openapi -f openapi
```