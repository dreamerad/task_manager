# Task Manager API

REST API для управления задачами.

## Быстрый запуск

Эта команда запустит все сервисы и выполнит тесты автоматически.

## Быстрый запуск

Swagger доступен по адресу 
http://localhost:8000

### Пошаговый запуск
```bash
make up
make test
make down
```

### Качество кода
```bash
make format      # Форматирование кода
make lint        # Проверка линтером
make type-check  # Проверка типов
make quality     # Полная проверка качества
```

### Другие команды
```bash
make build     # Собрать Docker образы
make clean     # Очистить все контейнеры
make help      # Показать справку
```

## Архитектура

Проект построен с использованием Clean Architecture:
- **Domain Layer** - Бизнес-логика и сущности
- **Application Layer** - Use Cases и интерфейсы
- **Infrastructure Layer** - База данных и внешние сервисы
- **API Layer** - REST API и обработка запросов

## Технологии

- **FastAPI** - Веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - База данных
- **Pytest** - Тестирование
- **Docker** - Контейнеризация
- **Black/Flake8/MyPy** - Качество кода

