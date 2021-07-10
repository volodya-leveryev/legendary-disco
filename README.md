# Legendary Disco

## Светлое будущее

Подготовка документации для расчёта часов преподавателей на кафедре с минимальными усилиями.

## Технологические решения

Проект написан на базе фреймворка Flask.

Проект использует СУБД MongoDB.

Для упрощения редактирования данных используется Flask-Admin. Т.к. он выглядит плохо, есть желание избавиться от 
него. Но на данный момент он необходим для удержания фокуса разработки на основной функциональности.

Авторизация осуществляется с помощью аккаунтов Google и Azure.

Для оформления страниц используется [Bulma](https://bulma.io), т. к. это позволяет получить компактные и стильные 
таблицы.

## Архитектурные решения

Данные о трудоустройстве сотрудников должны меняться с течением времени.

Данные о контингенте студентов должны меняться с течением времени.

Данные о дисциплинах загружаются из PLX-файлов.

## Конфигурация

При запуске решения необходимо создать конфигурационный файл вида:

```python
# Ключ для подписывания данных сессий
SECRET_KEY = ''

# Идентификаторы для аутентификации в Azure
AZURE_CLIENT_ID = ''
AZURE_TENANT_ID = ''
AZURE_CLIENT_SECRET = ''

# Идентификаторы для аутентификации в Google
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''

# Параметры подключения к MongoDB
MONGODB_DB = ''
MONGODB_HOST = ''
```

Для подключения к MongoDB используется Flask-MongoEngine. Параметры подключения можно посмотреть в [документации](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/).

Перед запуском создайте переменную окружения `JIMMY_CONFIG`, которая указывает на этот конфигурационный файл.

## Тестирование 

Для тестирования и определения тестового покрытия выполните:

```shell
export JIMMY_CONFIG=testing.cfg
pytest --cov=jimmy tests
coverage html
```

## Разработка

Для запуска СУБД в контейнере на MacOS/Linux выполните:

```shell
docker run \
    --detach \
    --name legendary-disco \ 
    --publish 127.0.0.1:27017:27017 \
    --user $(id -u):$(id -g) \
    --volume $(pwd)/db:/data/db \
    mongo:latest
```

Создайте и установите необходимые пакеты в виртуальное окружение:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Для запуска приложения на MacOS/Linux выполните:

```shell
export FLASK_APP=jimmy
export FLASK_ENV=development
export JIMMY_CONFIG=development.cfg
flask run
```
