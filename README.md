## Сервис для продажи и аренды недвижимости HomeService

На данный момент реализован следующий функционал:
- Создание дома, добавление его в базу сервиса;
- Создание квартиры, связанной с домом;
- Обновление/модификация данных о квартире (модерация);
- Получение списка доступных квартир для текущего дома.


В разработке:
- Ролевая модель доступа пользователей к сервису: различный функционал для клиентов и модераторов;
- Подписка на рассылку о новых объявлениях о недвижимости.


## Технологии
- `python3.12`
- пакеты из requirements.txt
- `docker` и `docker-compose`
- `PostgreSQL 15`

## Подготовка и запуск
- склонировать репозиторий
- в Вашей системе должны быть установлены все необходимые технологии из списка выше
- использовать команду `docker-compose up --build`

## Структура проекта
```
.
├── dummyenv/             # python venv
├── HomeService/          # core 
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── house_app/            # logic
│   ├── __init__.py
│   ├── management/       # custom commands for manage.py
│   │   └── commands/
│   │       └── wait_for_db.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── api.yaml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Логика
<img src="prjct_scheme.jpg">

## API
- /api/v1/house/create POST
- /api/v1/house/{id} GET
- /api/v1/flat/create POST
- /api/v1/flat/update/{id} PATCH
