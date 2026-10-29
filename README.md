# Журнал выхода учеников через КПП

Версия на React + Python + Telegram вместо Google Таблиц + Apps Script.

Готово: этап 1 — ядро (модели, поиск, разбор времени, загрузка списка).

## Запуск тестов (через Docker, без локального Python)

```bash
docker run --rm -v "D:\Git\kpp-journal:/repo" -w /repo/backend python:3.12-slim sh -c "pip install -q -e '.[dev]' && pytest -q -p no:cacheprovider"
```

## Загрузка списка учеников

Файл xlsx с листом «Для журнала» (ФИО | Класс | Эдвайзери) кладите в `data/` — эта папка не попадает в git.

```bash
alembic upgrade head
python -m app.importer ../data/spisok_dlya_zhurnala.xlsx          # предпросмотр
python -m app.importer ../data/spisok_dlya_zhurnala.xlsx --apply  # применить
```

База по умолчанию — `sqlite:///./kpp.db`, другую задайте через `DATABASE_URL`
(например `postgresql+psycopg://user:pass@host/kpp`).

## Структура

- `backend/app/services/` — нормализация ФИО, поиск, разбор времени
- `backend/app/importer.py` — загрузка и сверка списка
- `backend/app/models.py` — схема БД, миграции в `backend/alembic/`
- `shared/search_cases.json` — общие примеры поиска для backend и frontend
