# REST API для управления продуктами на торговой площадке.

---

## Описание

API позволяет пользователям добавлять, обновлять, удалять и получать информацию о продуктах, а также получать информацию
о категориях и фильтровать продукты по различным параметрам.

---

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker

---

## Доменные сущности

```

+--------------------+     +--------------------+
|                    |     |                    |
|       Product      |     |       Category     |
|                    |     |                    |
+--------------------+     +--------------------+
|                    |     |                    |
| id: UUID           |     | id: UUID           |
| sku: str           |     | name: str          |
| name: str          |     |                    |
| description: str   |     |                    |
| price: float       |     |                    |
| category_id: UUID  |     |                    |
|                    |     |                    |
+--------------------+     +--------------------+
 
```

---

## Запуск проекта

* ### Docker

1. Создайте файл `.env` в папке `database` и укажите в нем переменные окружения:

    ```bash
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    ```

2. Создайте файл `settings.json` в корне проекта и заполните его в соответствии с примером `example.settings.json`. Для приложения укажите хост `0.0.0.0`, порт `8000`, а для базы данных - хост `db`, порт `5432`.


3. Запустите проект:

    ```bash
      docker compose up --build
    ```

4. Примените миграции:

    ```bash
    docker compose exec app alembic upgrade head
    ```

* ### Локально

1. Создайте виртуальное окружение и активируйте его:

    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```
   
2. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
   
3. Создайте файл `settings.json` в корне проекта и заполните его в соответствии с примером `example.settings.json`.

4. Примените миграции:

    ```bash
    alembic upgrade head
    ```

5. Запустите проект:

    ```bash
    python main.py
    ```


## Документация

Документация доступна по адресу `http://{host}:{port}/docs`. Там описаны все доступные методы и параметры, а также есть возможность их протестировать.

## Автор

- Даньшин Семён
