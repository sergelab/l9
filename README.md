# LOT 9

## Project

Подготовка проекта
```
./project config development init
```

Сборка проекта под Python 3.7 в стадии development
```
./project build python3.7
```

Параметры БД поправить в **djangoprj/djangoprj/settings.py**.

Создание и инициализация БД
```
./bin/django migrate
```

Запуск Dev-сервера:

```
./bin/django runserver
```


# API

/api/ — схема методов

# Запуск обработчика файлов

./bin/lot9


# Events

```json
{
    "events": [
        {
            "name": "aaa",
            "pattern": "aaa \\d+$",
            "data": [
                {
                    "name": "a_numbers",
                    "pattern": "\\d+"
                }
            ],
            "id": 1
        },
        {
            "name": "line number",
            "pattern": "line \\d+$",
            "data": [
                {
                    "name": "numbers",
                    "pattern": "\\d+"
                }
            ],
            "id": 2
        },
        {
            "name": "line number and text",
            "pattern": "line \\d+ \\w+",
            "data": [
                {
                    "name": "numbers",
                    "pattern": "\\d+"
                },
                {
                    "name": "some_text",
                    "pattern": "\\w+"
                }
            ],
            "id": 3
        }
    ]
}
```