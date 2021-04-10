# Legendary Disco

## Светлое будущее

Подготовка документации для расчёта часов преподавателей на кафедре с минимальными усилиями.

## Технологические решения

Проект написан на базе фреймворка Flask.

Проект использует СУБД MongoDB.

Для упрощения редактирования данных используется Flask-Admin. Т.к. он выглядит плохо, есть желание избавиться от него. Но на данный момент он нужен чтобы удерживать фокус разработки на основной функциональности.

Авторизация осуществляется с помощью аккаунтов Google и Azure.

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
