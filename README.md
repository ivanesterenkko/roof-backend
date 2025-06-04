Для разработки необходимо установить pre-commit командой ```pre-commit install```, теперь при комите будет выполнена автоматическая проверка всех файлов на соответствие код-стайлу проекта (PEP8)

**Деплой для development**
1. Деплой для дева осуществляется автоматически через gitlab ci/cd (ниже шаги для ручного запуска)
2. Запускаем docker-compose файл
```docker
docker-compose -f docker/docker-compose-dev.yml up --build -d
```
3. При передеплое требуется остановить контейнеры
```docker
docker-compose -f docker/docker-compose-dev.yml down
```

**Деплой для production**
1. Запускаем docker-compose файл
```docker
docker-compose -f docker/docker-compose-prod.yml up --build -d
```
2. При передеплое требуется остановить контейнеры
```docker
docker-compose -f docker/docker-compose-prod.yml down
```

**Локальный запуск в Docker**
1. Запускаем через bash команду
```bash
./start-full.sh
```

**Локальный запуск тестов (тесты в процессе)**
1. Запускаем через bash команду
```bash
./run-tests.sh
```

**Структура миграции проекта (в процессе миграции)**
- docker/ - папка для докерфайлов
- src/ - код проекта:
    - api - эндпоинты
    - configs - конфиги
    - constants - константы и часть дефолтных настроек
    - crud - круд методы для работы с бд
    - databases - настройки подключения к бд и миграции
    - legacy - код с легаси крудами, схемами
    - models - модели SQAlchemy
    - tests - папка с тестами
    - schemas - модели Pydantic
    - security - код работы с jwt и пр.
    - services - основная логика
    - utilites - вспомогательные функции

**Добавление зависимостей в приложение**
- используем команду uv add lib_name

**Для изменения переменных .env необходимо вносить изменения в переменную DEV_BACK_ENV/PROD_BACK_ENV (Settings/CI/CD variables), при локальной разработке в файл ./src/.env**