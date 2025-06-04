# 🚀 Roof Backend

Асинхронный backend-проект на FastAPI + SQLAlchemy.

## 📦 Требования

- Python 3.12+
- Docker, Docker Compose
- pre-commit

## ⚙️ Настройка окружения

1. Клонируйте репозиторий:

```bash
git clone <repo-url>
cd roof-backend
```

2. Установите pre-commit:

```bash
pip install pre-commit
pre-commit install
```

Теперь при коммите будет выполняться автоматическая проверка всех файлов на соответствие PEP8 (ruff/black/isort).

## ⚙️ Настройка .env

Создайте файл `.env` (пример: `.env.example`) с переменными окружения:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=roof_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## 🚀 Деплой

### Development

```bash
docker-compose -f docker/docker-compose-dev.yml up --build -d
```

Перед повторным деплоем:

```bash
docker-compose -f docker/docker-compose-dev.yml down
```

### Production

```bash
docker-compose -f docker/docker-compose-prod.yml up --build -d
```

Перед повторным деплоем:

```bash
docker-compose -f docker/docker-compose-prod.yml down
```

## 🐳 Локальный запуск в Docker

```bash
./start-full.sh
```

## ✅ Миграции Alembic

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## 🧪 Запуск тестов

(тесты в процессе)

```bash
./run-tests.sh
```

## 📁 Основная структура проекта

```
src/
 ├── api/          # Эндпоинты FastAPI
 ├── services/     # Бизнес-логика
 ├── crud/         # CRUD-операции
 ├── models/       # ORM-модели
 ├── schemas/      # Pydantic-схемы
 ├── security/     # Аутентификация / авторизация
 ├── databases/    # Alembic миграции, db.py
 ├── configs/      # Конфигурации
 ├── constants/    # Константы
 ├── utilities/    # Утилиты
 ├── main.py       # Основной файл запуска
```

## 📝 Примечания

- Настройте путь к `ruff.toml` в `.pre-commit-config.yaml`.
- Проверьте, чтобы в Alembic корректно подключался `env.py` (с правильными переменными).
- Планируется расширение тестов.
