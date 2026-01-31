# Finance Workflows API

Демонстрационный backend-сервис для управления финансовыми workflow  
(шаги, статусы, лог событий).

Проект предназначен как **пример FastAPI-приложения**:
- без внешнего фронтенда
- без сложной инфраструктуры
- всё работает локально из коробки

---

## Стек

- Python 3.10+
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Pytest
- Swagger / OpenAPI

---

## Возможности

- CRUD для workflow
- Workflow состоит из шагов (steps)
- Завершение шагов (`complete`)
- Логирование событий (events)
- Автодокументация API (Swagger)

---

## Структура проекта

```
fastapi-finance-workflows-api/
├─ app/
│  ├─ main.py    # FastAPI приложение и эндпоинты
│  ├─ db.py      # SQLite + SQLAlchemy
│  ├─ models.py  # ORM модели
│  ├─ schemas.py # Pydantic схемы
│  └─ seed.py    # демо-данные
│
├─ tests/
│  └─ test_health.py  # базовый тест
│
├─ requirements.txt
└─ README.md
```

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd fastapi-finance-workflows-api
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 3. Активировать окружение

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

### Запуск сервера

```bash
uvicorn app.main:app --reload
```
