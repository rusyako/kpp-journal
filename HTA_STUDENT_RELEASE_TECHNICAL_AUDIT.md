# HTA Student Release — Technical Audit

Дата аудита: 2026-11-03 · Ветка: `test_connection_of_turnstiles` (совпадает с `origin/main`, коммит `2077ee7 0.0.1v`) · Рабочее дерево чистое.
Репозиторий: `kpp-journal` (в README система называется «Журнал выхода учеников через КПП»; это и есть проект, который заказчик называет HTA Student Release).

Обозначения: `path:line` — ссылка на исходный код. **NOT VERIFIED** — вывод не подтверждён запуском или оборудованием. Секреты, пароли и персональные данные в отчёт не включены.

---

## 0. Краткая сводка

**Что уже работает (подтверждено автотестами в изолированной копии, in-memory SQLite):**
- Ученики: импорт из xlsx с предпросмотром, ручное добавление и редактирование, деактивация выбывших.
- Поиск ученика при наборе (казахские буквы, ё/е, апострофы) — одинаковый алгоритм в Python и TypeScript.
- Разовое разрешение эдвайзера **на сегодня** («разрешено с ЧЧ:ММ» + причина), отмена разрешения.
- Ручная отметка «Вышел» охраной и её отмена; статусы OK / EARLY / NO_PERMISSION; защита от двойной отметки.
- Роли admin / guard / advisor / viewer; эдвайзер видит и меняет только свои группы.
- Журнал действий (частично), отчёт за день, WebSocket-обновления, вход через Telegram Mini App (подпись initData).
- Результаты: backend `75 passed`, frontend `19 passed`, `tsc + vite build` успешно, `alembic upgrade head` + `alembic check` — «No new upgrade operations detected».

**Что не работает / отсутствует:**
- Нет никакого кода интеграции с оборудованием (Hikvision, ISAPI, турникеты, устройства) — поиск по репозиторию пуст.
- Нет повторяющихся разрешений, нет разрешений на будущие даты, нет верхней границы времени («до»).
- Нет модели родителей/уполномоченных лиц и нет поля «кем подтверждено».
- Нет функции принятия решения «можно ли выпустить» — система только **классифицирует уже совершённый выход** (журнал, а не СКУД).
- Нет внешнего идентификатора ученика (номер карты, employeeNo) — только внутренний `students.id` и пара ФИО+класс.
- Подтверждённые проверкой дефекты безопасности: подделка cookie сессии при пустом/дефолтном `SECRET_KEY`; демо-логины и общий пароль отображаются на странице входа; сессии не отзываются; административные изменения не журналируются; разрешение, выданное после выхода, задним числом превращает «без разрешения» в «по разрешению».

**Что не проверено:** работа на PostgreSQL, Docker-сборка и compose (Docker daemon на машине аудита не был запущен), Telegram-бот (polling), SMTP, планировщик отчёта, резервное копирование, офлайн-очередь КПП и Service Worker в браузере, любое взаимодействие с Hikvision.

**Что можно использовать:** модели и миграции (как основа), сервисы `day.py` / `exits.py` / `advisor.py` / `audit.py`, авторизацию по ролям, импорт, поиск, WebSocket-хаб, frontend КПП, docker-compose-структуру (добавляется отдельный сервис адаптера по образцу `bot`).

**Что мешает интеграции Hikvision (блокеры):**
1. CRITICAL: подделка сессии при незаполненном `SECRET_KEY` (`backend/app/config.py:11`, `deploy/.env.example`).
2. Нет устойчивого идентификатора ученика для терминала.
3. Нет доменной функции «решение о выходе» с учётом окна времени, отмены и момента выдачи.
4. Нет таблиц устройств, событий устройств и синхронизации; `exits` не умеет хранить источник, устройство, направление и id события.
5. Неизвестны возможности конкретного терминала (поддержка remote verification, схема подключения турникета, тип идентификации) — нужен read-only опрос capabilities.

**Граф зависимостей:** построен Graphify (AST, 560 узлов / 1534 связи / 17 сообществ, циклов импорта нет) — `graphify-out/graph.json`, `graphify-out/graph.html`, `graphify-out/GRAPH_REPORT.md`; разбор — в `HTA_STUDENT_RELEASE_GRAPHIFY_ANALYSIS.md`, кратко — раздел 5.1.

**С чего продолжить:** Этап 1, задача 1.1 — запретить запуск API без надёжного `SECRET_KEY` и убрать демо-логины со страницы входа; параллельно — read-only скрипт опроса capabilities тестового терминала (только `GET`), см. раздел 17 и HANDOFF.

---

## 1. Executive Summary

Проект — зрелый по качеству кода, небольшой (~6 100 строк вместе с frontend) веб-журнал КПП: FastAPI + SQLAlchemy + PostgreSQL, React PWA, Telegram-бот. Код чистый, покрыт осмысленными приёмочными тестами (сценарии ТЗ П-3…П-13), миграция согласована с моделями.

Однако проект решает **другую задачу**, чем целевая система: он **фиксирует** факт выхода, отмеченный охранником вручную, и **после этого** раскрашивает его (по разрешению / раньше времени / без разрешения). Охрана может отметить выход любого ученика без разрешения — это штатное поведение (`backend/app/services/exits.py:48-79`). Для турникета требуется обратная логика: **до прохода** принять решение «разрешено / запрещено» и надёжно учесть отмену.

Готовность по компонентам (оценка аудитора):

| Компонент | Готовность для текущей задачи (журнал) | Готовность для Hikvision-интеграции |
|---|---|---|
| Ученики, импорт, поиск | Высокая | Средняя — нет внешнего ID / карт |
| Разрешения | Средняя (только «на сегодня, с ЧЧ:ММ») | Низкая — нет окна, повторов, подтверждения, версии |
| Журнал выходов | Высокая (ручной) | Низкая — нет источника, устройства, направления, события |
| Авторизация и роли | Средняя (есть дефекты конфигурации) | Низкая — нет сервисной (машинной) авторизации |
| Аудит | Частичная | Низкая — не журналируются админ-операции |
| Надёжность/эксплуатация | Средняя | Низкая — нет outbox, ретраев, мониторинга |
| Интеграция с оборудованием | — | Отсутствует (0%) |

**Вывод:** к разработке Hikvision Adapter можно приступать **только после Этапа 1** (исправление CRITICAL/HIGH) и **Этапа 2** (минимальное расширение схемы и доменная функция решения). Параллельно и безопасно можно делать read-only исследование тестового терминала.

---

## 2. Project Overview

- Назначение (README.md:1-20): журнал выхода учеников через КПП взамен Google Таблиц + Apps Script. Охрана ищет ученика и отмечает «Вышел», эдвайзер (куратор группы) вписывает разрешённое время и причину, руководство получает отчёт в Telegram в 16:50, администратор ведёт списки и пользователей.
- Ссылки на ТЗ в коде: «Ф-1…Ф-25» и сценарии «П-3…П-13» (README.md:4). Самого ТЗ в репозитории **нет**.
- «Лист дня» — это выборка по дате, а не копия (`backend/app/models.py:1`, `backend/app/services/day.py:1`).
- История: 4 коммита (Stage 1 core → Stages 2-4 backend → Stages 5-6 frontend+Docker → `0.0.1v` с демо-логинами и доступом из LAN). Ветка `test_connection_of_turnstiles` пока не содержит отличий от `main`.
- Открытые вопросы из README.md:79-83: сервер (VPS в Казахстане или школьный), вход охраны (логин/пароль или Google hta.kz), канал отчёта, вопросы раздела 10 ТЗ (в т.ч. «нужна ли отметка “вернулся”»).

---

## 3. Technology Stack

| Слой | Технология | Источник |
|---|---|---|
| Язык backend | Python ≥ 3.12 | `backend/pyproject.toml:5` |
| Web | FastAPI ≥ 0.115, Uvicorn | `backend/pyproject.toml:11-12` |
| ORM / миграции | SQLAlchemy 2.x, Alembic | `backend/pyproject.toml:7-8` |
| СУБД (prod) | PostgreSQL 16 (psycopg 3) | `deploy/docker-compose.yml:5-17`, `:25` |
| СУБД (dev/tests) | SQLite (по умолчанию `sqlite:///./kpp.db`) | `backend/app/config.py:8` |
| Сессии | itsdangerous `URLSafeTimedSerializer`, cookie `kpp_session` | `backend/app/services/auth.py:14-15` |
| Пароли | hashlib.scrypt (n=2^14, r=8, p=1), соль 16 байт | `backend/app/services/auth.py:17-31` |
| Планировщик | APScheduler 3 (BackgroundScheduler, in-process) | `backend/app/scheduler.py` |
| Telegram | aiogram 3 (бот, polling), httpx (Bot API из API-процесса) | `backend/app/bot.py`, `backend/app/notify.py:31-54` |
| Отчёт | Jinja2 HTML | `backend/app/templates/report.html`, `backend/app/services/report.py` |
| Frontend | React 18.3.1, react-router 6, Vite 5, TypeScript 5.6, Vitest 2 | `frontend/package.json` |
| PWA | Service Worker, localStorage-очередь | `frontend/public/sw.js`, `frontend/src/lib/offlineQueue.ts` |
| Деплой | Docker (multi-stage), docker compose: db, api, bot, caddy (HTTPS), backup | `Dockerfile`, `deploy/docker-compose.yml` |
| Часовой пояс | `Asia/Qyzylorda` (UTC+5) | `backend/app/config.py:6` |

---

## 4. Repository Structure

```
Dockerfile                       единый образ: сборка React + Python API (CMD: alembic upgrade head && uvicorn, 1 воркер)
README.md                        описание, установка, разработка, открытые вопросы
backend/
  alembic/versions/0001_initial_schema.py   единственная миграция (вся схема)
  app/config.py                  все настройки из env (секреты, TZ, SMTP, Telegram)
  app/db.py                      engine + SessionLocal
  app/clock.py                   «сейчас» в TZ школы (подменяется в тестах)
  app/models.py                  ORM-модели (8 таблиц)
  app/main.py                    FastAPI app, WebSocket /api/ws, раздача SPA
  app/deps.py                    get_db, current_user, роли-зависимости
  app/api/auth.py                /api/auth/login|logout, /api/me
  app/api/kpp.py                 /api/day, /api/exits, /api/exits/{id}/cancel, /api/audit
  app/api/advisor.py             /api/advisor/* (группы, разрешения)
  app/api/admin.py               /api/admin/* (импорт, ученики, пользователи, календарь, отчёты, health)
  app/services/day.py            «лист дня», статусы, сортировка
  app/services/exits.py          отметка/снятие выхода
  app/services/advisor.py        видимость групп, права, set_permission
  app/services/audit.py          запись и чтение журнала действий
  app/services/auth.py           пароли, сессии, проверка Telegram initData
  app/services/calendar.py       рабочие дни
  app/services/invites.py        одноразовые коды привязки Telegram
  app/services/report.py         отчёт за день
  app/services/search.py         эталон поиска (используется только тестами)
  app/services/normalize.py      нормализация ФИО
  app/services/time_parse.py     разбор «1505», «15.05», «15»
  app/events.py                  in-memory WebSocket hub
  app/notify.py                  Telegram/SMTP, фоновый ThreadPoolExecutor
  app/scheduler.py               ежедневный отчёт
  app/bot.py                     Telegram-бот (/start + инвайт)
  app/cli.py                     create-admin, send-report, demo
  app/importer.py                разбор xlsx, diff, применение
  tests/                         conftest + 4 файла тестов
deploy/  docker-compose.yml, Caddyfile, backup.sh, .env.example
frontend/src/  App.tsx, pages/{Kpp,Advisor,Admin,Reports,Login}.tsx, lib/{api,live,offlineQueue,search,normalize,telegram}.ts
shared/search_cases.json         общие кейсы поиска для pytest и vitest
```

Неиспользуемый/дублирующийся код:
- `backend/app/services/search.py` — используется только в `backend/tests/test_search.py:7`; в рантайме поиск выполняется в браузере (`frontend/src/lib/search.ts`). Это осознанный «эталон», дублирование алгоритма закрыто общими кейсами `shared/search_cases.json`.
- `backend/app/importer.py:291-316` — CLI-импорт, дублирует `/api/admin/import`, но без записи в audit.
- Graphify-граф (`graphify-out/`) в репозитории отсутствует.

---

## 5. Current Architecture

```
 Браузер КПП (PWA)  ──cookie──┐
 Браузер админа/руководства ──┤      ┌──────────── API (uvicorn, 1 процесс) ─────────────┐
 Telegram Mini App ─initData──┼─────►│ FastAPI routers → services → SQLAlchemy → Postgres │
                              │      │ WebSocket hub (in-memory)                         │
                              │      │ APScheduler (отчёт 16:50)                          │
                              │      │ notify ThreadPool → Telegram Bot API / SMTP        │
                              │      └───────────────────────────────────────────────────┘
 Telegram ◄── бот (отдельный контейнер, polling, только /start+инвайт) ──► Postgres
 Caddy (HTTPS) → api:8000;   backup-контейнер: pg_dump раз в сутки
```

Ключевые свойства:
- **Один процесс API** обязателен: в нём живут планировщик и WebSocket-хаб (`Dockerfile:24-25`, `backend/app/scheduler.py:1-5`, `backend/app/events.py:15-50`).
- Время выхода ставит **сервер** (`backend/app/services/exits.py:56`), с точностью до минуты (`backend/app/clock.py:16-19`); офлайн-отметки принимают время клиента, но не позже серверного (`exits.py:58-63`).
- WebSocket передаёт только «что изменилось» (дата, student_id, advisory_id), клиент сам перечитывает данные (`backend/app/events.py:1-5`, `:55-56`).
- Слои разделены корректно: `api/*` — тонкие обработчики, логика в `services/*`. Исключение — `api/admin.py` содержит бизнес-логику учеников и пользователей прямо в роутере (`backend/app/api/admin.py:94-137`, `:190-213`).

### 5.1 Зависимости по графу Graphify

Подробно: `HTA_STUDENT_RELEASE_GRAPHIFY_ANALYSIS.md`. Граф: `graphify-out/graph.json` (AST-разбор `graphify extract . --code-only`, коммит `2077ee77`).

- Слои однонаправлены: `api/* → services/* → models.py / clock.py / config.py`; **циклов импорта нет**.
- Хабы: `User` (63 связи), `Student` (28), `apply_import()` (24), `DayRow` (21), `mark_exit()` (20), `set_permission()` (18).
- `set_permission()` (`services/advisor.py:70`) — **единственный** писатель `Permission`; `load_day()` (`services/day.py:70`) — **единственный** читатель; от `load_day()` зависят 21 узел (КПП, эдвайзер, отчёт, рассылка).
- В графе **нет ребра `mark_exit()` → `Permission`**: запись выхода не проверяет разрешение (подтверждает раздел 10).
- `audit.log()` вызывают ровно 6 функций (`mark_exit`, `cancel_exit`, `set_permission`, `send_report`, `import_list`, `login`); админ-операции его не вызывают (подтверждает R4).
- `is_working_day()` не вызывается ни из `mark_exit()`, ни из `set_permission()`.
- Ограничение графа: связи frontend → backend идут через HTTP-строки и в AST-графе отсутствуют (0 рёбер); их сопоставление дано в разделе 8 и в Graphify-анализе.
- Точки подключения Hikvision по графу: новое решение `decide_exit()` рядом с `load_day()`; запись проходов — новая функция в `services/exits.py` по образцу `mark_exit()`; постановка синхронизации/отмены — в `set_permission()` после commit; адаптер — отдельный процесс, не в `main.py:lifespan()`.

---

## 6. Existing Features and Status

Методика: **[T]** — подтверждено автотестами проекта; **[P]** — подтверждено проверочными сценариями аудитора (временные тесты в изолированной копии, удалены после прогона); **[C]** — установлено только по исходному коду.

| # | Функция | Статус | Подтверждение | Где |
|---|---|---|---|---|
| 1 | Добавление ученика (вручную) | WORKING | [P] создан через API, 200 | `backend/app/api/admin.py:114-122` |
| 1a | Импорт списка xlsx (предпросмотр/применение) | WORKING | [T] `test_p13_import_preview_and_apply`, `test_importer.py` | `backend/app/api/admin.py:42-64`, `backend/app/importer.py` |
| 2 | Поиск ученика | WORKING | [T] pytest `test_search.py` + vitest 19 тестов | `frontend/src/lib/search.ts`, `backend/app/services/search.py` |
| 3 | Редактирование ученика | WORKING с дефектом | [P] правка работает; переименование в существующую пару ФИО+класс → **HTTP 500** | `backend/app/api/admin.py:125-137` |
| 4 | Создание разрешения на выход | WORKING (только на сегодня) | [T] П-6, П-8 | `backend/app/services/advisor.py:70-105` |
| 5 | Разовые разрешения | WORKING (одно на ученика в день) | [T] | `backend/app/models.py:133-152` (`UNIQUE(date, student_id)`) |
| 6 | Повторяющиеся разрешения | MISSING | [C] нет модели и API | — |
| 7 | Изменение и отмена разрешения | WORKING | [T] П-8 (пустое время = отмена, soft delete `deleted_at`) | `backend/app/services/advisor.py:84-95` |
| 8 | Проверка конкретной даты | PARTIAL | [P] API не принимает дату — разрешение всегда на `clock.today()`; лист дня по дате читается | `backend/app/api/advisor.py:32-34`, `advisor.py:72` |
| 9 | Проверка временного интервала | PARTIAL | [T] только нижняя граница «разрешено с»; верхней границы нет; проверка выполняется **после** выхода (раскраска) | `backend/app/services/day.py:41-47` |
| 10 | Подтверждение родителя / уполномоченного | MISSING | [C] нет таблиц и полей | — |
| 11 | Авторизация сотрудников | WORKING с дефектами | [T] `test_roles`, Mini App; [P] сессии не отзываются, при пустом `SECRET_KEY` cookie подделывается | `backend/app/deps.py`, `backend/app/services/auth.py` |
| 12 | Разграничение прав | WORKING | [T] `test_roles`, `test_advisor_sees_only_own_advisory` | `backend/app/deps.py:48-53`, `backend/app/services/advisor.py:22-34` |
| 13 | История изменений | PARTIAL | [T] журнал выходов/разрешений; [P] создание ученика **не** журналируется; [C] пользователи, роли, календарь, инвайты не журналируются | `backend/app/services/audit.py` |
| 14 | Журнал фактических выходов | WORKING (ручной ввод охраной) | [T] П-3, П-5, отчёт П-11 | `backend/app/services/exits.py` |
| 15 | API для внешних устройств | MISSING | [C] нет сервисной авторизации, нет endpoint для событий | — |
| 16 | Интеграция с Hikvision | MISSING | [C] поиск `hikvision|isapi|device|turnstile` — 0 совпадений | — |
| 17 | Обработка ошибок и недоступности сервера | PARTIAL | [T] двойная отметка → 409, офлайн-время; [C] офлайн-очередь и SW в браузере не тестировались; [P] ряд IntegrityError → 500 | `frontend/src/lib/offlineQueue.ts`, `frontend/public/sw.js` |
| — | Telegram Mini App вход | WORKING | [T] `test_telegram_mini_app_auth` | `backend/app/services/auth.py:46-67` |
| — | Привязка Telegram по инвайту | WORKING | [T] `test_invite_binds_telegram` | `backend/app/services/invites.py` |
| — | Уведомления эдвайзеру о выходе | WORKING (отправка замокана) | [T] | `backend/app/notify.py:111-115` |
| — | Telegram-бот (polling) | IMPLEMENTED_NOT_TESTED | [C] | `backend/app/bot.py` |
| — | Отчёт за день (сборка, HTML, рассылка) | WORKING (отправка замокана) | [T] П-11 | `backend/app/services/report.py` |
| — | Отправка отчёта по почте | IMPLEMENTED_NOT_TESTED | [C] | `backend/app/notify.py:57-75` |
| — | Расписание отчёта 16:50 | IMPLEMENTED_NOT_TESTED | [C] в тестах выключено (`conftest.py:3`) | `backend/app/scheduler.py` |
| — | WebSocket live-обновления | WORKING | [T] `test_websocket_notifies_guard` | `backend/app/main.py:37-52` |
| — | Календарь рабочих дней | WORKING | [T] `test_school_calendar` | `backend/app/services/calendar.py` |
| — | Проверка системы (health) | WORKING | [T] `test_admin_users_and_health` | `backend/app/api/admin.py:303-347` |
| — | Офлайн-очередь КПП | IMPLEMENTED_NOT_TESTED | [C] серверная часть [T] `test_offline_queue_time` | `frontend/src/lib/offlineQueue.ts` |
| — | Резервные копии | IMPLEMENTED_NOT_TESTED | [C] | `deploy/backup.sh` |
| — | Docker / compose / Caddy | IMPLEMENTED_NOT_TESTED | Docker daemon был недоступен | `Dockerfile`, `deploy/` |
| — | Работа на PostgreSQL | IMPLEMENTED_NOT_TESTED | тесты только на SQLite | `backend/app/models.py:160-168` (partial index для обеих СУБД) |

---

## 7. Database Analysis

### 7.1 СУБД и миграции
- Prod: PostgreSQL 16 (`deploy/docker-compose.yml:6`). Dev/test: SQLite.
- Миграции: Alembic, одна ревизия `0001` (`backend/alembic/versions/0001_initial_schema.py`). Именование ограничений через `naming_convention` (`backend/app/models.py:29-39`). Для SQLite включён batch-режим (`backend/alembic/env.py:28`).
- Миграция применяется автоматически при старте контейнера (`Dockerfile:25`). **Проверено:** `alembic upgrade head` + `alembic check` на временной SQLite — расхождений моделей и миграции нет. Downgrade не проверялся.
- Enum хранятся как строки (`native_enum=False`), в БД пишутся **имена** (`'ADMIN'`, `'GUARD'`…), а не значения (`0001_initial_schema.py:24`, `:38`).

### 7.2 Таблицы

| Таблица | Ключевые поля | Ограничения |
|---|---|---|
| `advisories` | id, name, kind (PRIMARY/ALPHA/CDC/GROUP), sort_order, active | UNIQUE(name) |
| `students` | id, full_name, full_name_norm, class_name, advisory_id, active, created_at | UNIQUE(full_name, class_name); FK advisory; индекс по full_name_norm |
| `users` | id, role, display_name, email, username, password_hash, telegram_id, receives_report, active | UNIQUE(email), UNIQUE(username), UNIQUE(telegram_id) |
| `invites` | code (PK), user_id, expires_at, used_at | FK users |
| `user_advisories` | (user_id, advisory_id) PK | FK обе стороны |
| `school_days` | date (PK), is_working, note | — |
| `permissions` | id, date, student_id, allowed_time (TIME, nullable), raw_time, reason, created_by, updated_at, deleted_at | UNIQUE(date, student_id); FK students, users |
| `exits` | id, date, student_id, exit_time (TIME), guard_id, offline, cancelled_at, cancelled_by | UNIQUE(date, student_id) WHERE cancelled_at IS NULL (partial) |
| `audit_log` | id, ts, user_id, action, student_id, payload (JSON) | FK users, students; индекс по ts |

Источник: `backend/app/models.py:56-194`.

### 7.3 Связи
- Ученик → эдвайзери (группа) → эдвайзеры (`user_advisories`). Права эдвайзера определяются группой ученика.
- Разрешение → ученик, → пользователь `created_by` (перезаписывается при каждом изменении — `backend/app/services/advisor.py:95`, [P] подтверждено).
- Выход → ученик, → охранник (`guard_id`), → отменивший (`cancelled_by`).
- **Связи «разрешение ↔ выход» нет** — статус вычисляется на лету по дате и student_id (`backend/app/services/day.py:70-105`).
- **Родителей/уполномоченных лиц в модели нет вообще.**

### 7.4 Идентификаторы учеников
- Внутренний `students.id` (autoincrement) — стабилен при переводе в другой класс (импорт обновляет запись, `backend/app/importer.py:248-255`).
- Бизнес-ключ — пара ФИО + класс (`models.py:71`). Внешнего ID (номер ученика, номер карты, employeeNo терминала) **нет**.

### 7.5 Дата, время, часовые пояса
- TZ школы — `Asia/Qyzylorda` (UTC+5) (`backend/app/config.py:6`), «сейчас» — `clock.now()` в этом поясе (`backend/app/clock.py:8-9`).
- `permissions.date`, `exits.date` — DATE (локальная дата школы); `allowed_time`, `exit_time` — TIME без пояса, точность до минуты.
- `updated_at`, `deleted_at`, `cancelled_at`, `audit_log.ts`, `invites.*` — `DateTime(timezone=True)`. В SQLite пояс теряется — код это компенсирует (`backend/app/services/audit.py:40`, `backend/app/services/invites.py:30`).
- Для событий турникета этого недостаточно: нужны секунды и абсолютное время (timestamptz) + время устройства отдельно от времени приёма.

### 7.6 Аудит
- `audit_log` пишется для: `login`, `exit`, `exit_cancel`, `permission_set`, `permission_clear`, `import`, `report_sent` (`backend/app/services/audit.py:16-24`).
- **Не пишется** для: создания/изменения учеников (`admin.py:114-137`, [P] подтверждено), создания/изменения пользователей и ролей (`admin.py:221-239`), выдачи инвайтов (`admin.py:242-247`), изменений календаря (`admin.py:264-279`), разрешения «только причина без времени» и снятия такого разрешения (`advisor.py:97-101`).
- Журнал изменяем на уровне БД (нет append-only защиты).

### 7.7 Достаточно ли данных для автоматического решения о выходе

| Вопрос | Можно определить сейчас? | Комментарий |
|---|---|---|
| Кто получил разрешение | Да | `permissions.student_id` |
| Кто его выдал | Частично | `created_by` перезаписывается последним редактором; первоначальный автор — только в `audit_log` |
| Кто подтвердил (родитель/уполномоченный) | **Нет** | полей нет |
| На какое время действительно | Частично | только «с ЧЧ:ММ» на одну дату; верхней границы нет |
| Было ли отменено | Да, но без автора | `deleted_at` есть, `deleted_by` нет (автор — в audit, если было время) |
| Использовано ли одноразовое | Косвенно | есть активный `exits` за дату; явной связи и флага «погашено» нет |
| Через какой турникет вышел | **Нет** | нет устройства/двери |
| Подтверждён ли физический проход | **Нет** | отметка ставится охранником по нажатию; признака прохода нет |
| Когда разрешение выдано относительно выхода | **Нет** (в данных статуса) | [P] разрешение, выданное после выхода, меняет статус на OK задним числом |

### 7.8 Минимальные изменения схемы (предложение, миграции НЕ создавались)

1. `students`: `access_id VARCHAR(32) UNIQUE NULL` — идентификатор персоны на терминалах (employeeNo); не ФИО.
2. Новая `student_credentials`: `id, student_id FK, kind ('card'|'face'|'pin'), card_no VARCHAR NULL, issued_at, revoked_at, note` + UNIQUE(kind, card_no) WHERE revoked_at IS NULL. Биометрию в БД системы **не хранить**.
3. `permissions`: добавить `valid_until TIME NULL`, `granted_by FK users` (неизменяемый), `updated_by FK users`, `deleted_by FK users`, `confirmed_by_kind` ('parent'|'guardian'|'staff'), `confirmed_by_name VARCHAR`, `confirmation_method` ('phone'|'message'|'in_person'), `confirmed_at timestamptz`, `kind` ('one_time'|'recurring'), `recurring_id FK NULL`, `version INT` (для синхронизации), `consumed_exit_id FK exits NULL`.
4. Новая `recurring_permissions`: `id, student_id, weekdays SMALLINT (битовая маска), allowed_time, valid_until, start_date, end_date, granted_by, confirmed_*, created_at, revoked_at, revoked_by`. Разовые строки `permissions` материализуются на день (или решение вычисляется по обеим таблицам).
5. Новая `devices`: `id, name, model, firmware, host, port, door_no, direction ('in'|'out'), is_test BOOL, enabled BOOL, last_seen_at, last_event_cursor`. Логин/пароль устройства — **только в env/секрет-хранилище**, не в БД и не в репозитории.
6. Новая `device_events`: `id, device_id FK, serial_no BIGINT, device_time timestamptz, received_at timestamptz, major INT, minor INT, employee_no VARCHAR NULL, card_no_hash NULL, verify_mode VARCHAR, door_no INT, direction, student_id FK NULL, decision ('granted'|'denied'|'unknown'), raw JSONB` + **UNIQUE(device_id, serial_no)** для дедупликации.
7. `exits`: `source ('manual'|'offline'|'device')`, `device_id FK NULL`, `device_event_id FK NULL UNIQUE`, `permission_id FK NULL`, `exit_at timestamptz` (точное время), `pass_confirmed BOOL`.
8. Новая `device_sync` (outbox): `id, device_id, student_id, desired_state JSON, permission_version, status ('pending'|'done'|'failed'), attempts, last_error, updated_at`.

---

## 8. API Analysis

Все пути с префиксом `/api`. Авторизация — cookie `kpp_session` или заголовок `X-Telegram-Init-Data` (`backend/app/deps.py:11`, `:19-29`).

| Метод и путь | Роли | Назначение | Код |
|---|---|---|---|
| POST `/auth/login` | — | вход по логину/паролю, ставит cookie | `api/auth.py:22-37` |
| POST `/auth/logout` | — | удаляет cookie (токен не отзывается) | `api/auth.py:40-43` |
| GET `/me` | любой вошедший | профиль, группы, рабочий ли день | `api/auth.py:46-56` |
| GET `/health` | — | `{"ok": true}` | `main.py:32-34` |
| WS `/ws?tg=` | любой вошедший | сигналы изменений | `main.py:37-52` |
| GET `/day?d=` | guard, admin, viewer | лист дня | `api/kpp.py:20-28` |
| POST `/exits` | guard, admin | отметить выход (`student_id`, `client_time?`) | `api/kpp.py:45-47` |
| POST `/exits/{student_id}/cancel` | guard, admin | снять отметку за сегодня | `api/kpp.py:50-52` |
| GET `/audit?d=` | guard, admin, viewer | журнал действий за день | `api/kpp.py:55-57` |
| GET `/advisor/advisories` | advisor, admin, viewer | видимые группы | `api/advisor.py:15-17` |
| GET `/advisor/advisories/{id}` | advisor, admin, viewer | строки группы на сегодня | `api/advisor.py:20-30` |
| PUT `/advisor/students/{id}/permission` | advisor (свои), admin | время+причина на сегодня; пусто = отмена | `api/advisor.py:37-44` |
| POST `/admin/import` | admin | xlsx, `apply` false/true | `api/admin.py:42-64` |
| GET/POST `/admin/students`, PUT `/admin/students/{id}` | admin | ученики | `api/admin.py:88-137` |
| GET `/admin/advisories` | admin | группы | `api/admin.py:140-157` |
| GET/POST `/admin/users`, PUT `/admin/users/{id}`, POST `/admin/users/{id}/invite` | admin | пользователи, инвайты | `api/admin.py:216-247` |
| GET `/admin/school-days`, PUT/DELETE `/admin/school-days/{d}` | admin | календарь | `api/admin.py:258-279` |
| GET `/reports/{d}`, `/reports/{d}/html` | admin, viewer | отчёт | `api/admin.py:285-292` |
| POST `/admin/reports/{d}/send` | admin | разослать отчёт | `api/admin.py:295-297` |
| GET `/admin/health` | admin | проверки конфигурации | `api/admin.py:303-347` |

Наблюдения:
- Нет endpoint для внешних систем (устройств): нет машинной авторизации (API-ключ/mTLS), нет «проверить разрешение», нет приёма событий.
- Нет пагинации; объёмы школы (сотни учеников) это допускают.
- Ошибки целостности в нескольких местах не перехватываются → 500: `update_student` [P], `create_student` при гонке [C], `set_permission` при одновременном первом сохранении [C] (`advisor.py:81-90`, нет обработки IntegrityError на `UNIQUE(date, student_id)`).
- Схемы запросов (Pydantic) минимальны: `PermissionIn` — две строки без ограничений длины (обрезка в сервисе, `advisor.py:79-80`); `UserIn.role` — enum; `StudentIn` проверяется через `clean_name/clean_class`.

---

## 9. Authentication and Permissions

- Пароли: scrypt + соль, сравнение константного времени (`backend/app/services/auth.py:20-31`). Минимум 8 символов (`api/admin.py:196-197`, `cli.py:26`). OK.
- Сессия: подписанный (не зашифрованный) токен `{"uid": N}`, срок `SESSION_DAYS=30` (`services/auth.py:34-43`, `config.py:12`). Cookie: `httponly`, `secure` по `COOKIE_SECURE`, `samesite=lax` (`api/auth.py:29-36`).
- Каждый запрос перечитывает пользователя и проверяет `active` (`deps.py:26-29`) — деактивация и смена роли действуют сразу.
- **Отзыва сессий нет:** logout только удаляет cookie у клиента, смена пароля старые сессии не инвалидирует [P].
- **Ключ подписи:** `SECRET_KEY` по умолчанию `"dev-secret-change-me"` (`config.py:11`); в `deploy/.env.example` переменная пустая, а compose её не требует (в отличие от `POSTGRES_PASSWORD`, `docker-compose.yml:11`). При пустом значении `os.environ.get` вернёт пустую строку, и [P] подтверждено: cookie с `uid` администратора, подписанная пустым ключом, даёт доступ к `/api/admin/users` (HTTP 200). Дефолтный ключ публично известен из репозитория — тот же эффект.
- Telegram Mini App: проверка HMAC initData по алгоритму Telegram, срок 24 ч (`services/auth.py:46-67`). Для WebSocket initData передаётся в query string (`main.py:38`, `frontend/src/lib/live.ts:26-28`) — может оседать в логах прокси.
- Нет ограничения частоты входа / блокировки [P] (30 неверных попыток подряд — все 401, без задержек).
- Роли (`deps.py:48-53`):
  - `ADMIN` — всё; `GUARD` — лист дня, отметки, журнал; `ADVISOR` — свои группы, разрешения; `VIEWER` — чтение листа дня, групп, отчётов.
  - Права эдвайзера на ученика — по группе ученика (`services/advisor.py:31-34`, `:76-77`).
- Демо-учётки: `cli demo` создаёт `admin/kpp/kotiki/primary/director` с общим паролем (`backend/app/cli.py:47-68`), а страница входа **всегда** показывает эти логины и пароль (`frontend/src/pages/Login.tsx:45-72`). Если команда `demo` будет выполнена на рабочей БД — полный административный доступ для любого посетителя страницы.
- Ролей для устройств/интеграций нет.

---

## 10. Student Release Business Logic

### 10.1 Как работает сейчас
1. Эдвайзер (только для своей группы, только на **сегодня**) вводит время и причину: `set_permission` (`services/advisor.py:70-105`). Время разбирается из «15:05 / 15.05 / 1505 / 15» (`services/time_parse.py:14-30`); нераспознанное сохраняется как `raw_time` с `allowed_time=NULL` → статус «⚠️ время не распознано» и **никакого разрешения для охраны**.
2. Пустые время и причина → soft delete (`deleted_at`). Повторное заполнение «воскрешает» ту же строку (`advisor.py:84-95`).
3. Охрана находит ученика и нажимает «Вышел» → `mark_exit` (`services/exits.py:48-79`): проверяет существование ученика и отсутствие активной отметки, ставит серверное время, ловит гонку двух охранников по partial unique index.
4. Статус строки вычисляется при каждом чтении (`services/day.py:41-47`):
   - нет выхода: `ALLOWED` (есть время) / `NONE`;
   - выход без `allowed_time`: `NO_PERMISSION`;
   - `exit_time < allowed_time`: `EARLY`, иначе `OK`.
5. Эдвайзеру уходит уведомление о любом выходе своего ученика (`notify.py:111-115`).

### 10.2 Чего нет для автоматического выпуска
- Решения «разрешить/запретить» **до** прохода. `mark_exit` не проверяет разрешение, рабочий день и даже `student.active` ([P] выход для деактивированного ученика — 200).
- Верхней границы окна, будущих дат, повторов, подтверждения родителем.
- Учёта момента выдачи: [P] выход в 14:00 без разрешения → эдвайзер в 14:05 ставит «13:00» → в листе дня и отчёте статус становится `ok`. Для журнала это неприятно, для турникета — недопустимо (решение должно опираться на состояние разрешения **на момент события**).
- Понятия «одноразовое использовано»: один активный выход на день по уникальному индексу, но разрешение с выходом не связывается; повторный выход после возвращения в школу не моделируется (вопрос «отметка “вернулся”» открыт в README.md:83).
- `Exit` хранит только минуты, нет секунд и абсолютного времени.

### 10.3 Предлагаемая доменная функция (новый код, не реализовано)
`app/services/release.py`: `decide_exit(db, student_id, at: datetime, device_id | None) -> Decision(allowed: bool, reason_code, permission_id, permission_version)`. Правила: ученик активен; рабочий день (или явное разрешение в нерабочий); есть неотменённое разрешение на дату `at` (разовое или из повторяющегося), подтверждённое; `allowed_time ≤ at.time() ≤ valid_until`; разрешение не погашено (если одноразовое). Чистая функция, без обращения к оборудованию; переиспользует запросы из `day.py`.

---

## 11. Hikvision Integration Readiness

### 11.1 Ответы на вопросы задачи

1. **Модуль взаимодействия с оборудованием:** отсутствует полностью.
2. **Подходящие API endpoints:** отсутствуют. `POST /api/exits` — ручная отметка от имени пользователя-охранника по cookie; для устройства не подходит (нет машинной авторизации, нет id события, время всегда серверное).
3. **Где разместить Hikvision Adapter:** отдельный пакет `backend/app/integrations/hikvision/` (ISAPI-клиент, маппинг, синхронизация, приём событий) и **отдельный процесс** `python -m app.hikvision_worker` — новый сервис в `deploy/docker-compose.yml` по образцу `bot` (`docker-compose.yml:32-40`). Не внутри API-процесса: он однопроцессный и держит планировщик/WebSocket (`Dockerfile:24`). Доменные сервисы не должны импортировать адаптер; адаптер вызывает `services/release.py` и пишет в `device_events`/`exits`. HTTP-клиент `httpx` уже в зависимостях и поддерживает Digest-аутентификацию, обычно используемую ISAPI (**NOT VERIFIED** на данном терминале).
4. **Сопоставление ученика и терминала:** `students.access_id` ↔ `employeeNo` на терминале (не ФИО, не внутренний `id` напрямую); карта — через `student_credentials`. Рекомендуемый способ идентификации для MVP — **карта** (без биометрии).
5. **Синхронизация разрешений:** outbox `device_sync`. Каждое изменение разрешения увеличивает `version` и создаёт задачу; воркер применяет её к терминалам направления «выход», с ретраями и отметкой результата. Периодическая полная сверка (reconcile) терминал ↔ БД.
6. **Получение событий:** два механизма ISAPI (по документации, **NOT VERIFIED** для DS-K1T341CM V3.3.40):
   - опрос журнала `POST /ISAPI/AccessControl/AcsEvent?format=json` с курсором по времени/`serialNo` — надёжен после перезапусков;
   - подписка `GET /ISAPI/Event/notification/alertStream` или настройка push на HTTP-хост (`/ISAPI/Event/notification/httpHosts`) — меньше задержка.
   Рекомендация: опрос как основной источник истины, поток — как ускоритель.
7. **Направление:** определять конфигурацией устройства (`devices.direction`: терминал установлен на выход) и/или номером двери/считывателя. Поле `attendanceStatus` терминала не считать надёжным.
8. **Повторная обработка:** UNIQUE(`device_id`, `serial_no`) в `device_events`, вставка «insert … on conflict do nothing», связь `exits.device_event_id UNIQUE`. Учесть возможный сброс `serialNo` после сброса устройства (дополнительно сверять `device_time`).
9. **Отмена разрешения:** в сценарии A — немедленная задача outbox на удаление/сужение срока пользователя на терминале + алерт охране, если терминал не подтвердил применение за N секунд; короткие окна валидности как страховка. В сценарии B — проверка в момент запроса, отмена действует сразу.
10. **Недоступность:** см. 11.2 и раздел 12. Принцип: при сомнении — **не выпускать самостоятельно** (fail-closed для выхода ученика), но **никогда** не влиять на аварийную разблокировку (fire input/эвакуация — аппаратно, вне ПО).

### 11.2 Сравнение сценариев

**A. Разрешения загружаются в терминал, решение принимает устройство.**
Запись персоны с `Valid.beginTime/endTime` (и/или шаблоном расписания) на терминал выхода через `UserInfo/Record|Modify|Delete`, карта через `CardInfo/Record` (по документации ISAPI; **NOT VERIFIED** на данном устройстве и прошивке).

**B. Терминал запрашивает систему в момент прохода (remote verification) или система открывает дверь командой.**
Варианты: (B1) режим удалённой проверки, когда терминал отправляет событие и ждёт ответ сервера — поддержка моделью **NOT VERIFIED**, требуется проверка capabilities; (B2) терминал только идентифицирует, сервер получает событие и шлёт `PUT /ISAPI/AccessControl/RemoteControl/door/1` (`<cmd>open</cmd>`) — изучена, физическое открытие турникета **не подтверждено**.

| Критерий | A (решение в терминале) | B1 (remote verification) | B2 (событие → команда open) |
|---|---|---|---|
| Работа без сети/сервера | Да, по загруженным данным | Нет (поведение по таймауту зависит от устройства — NOT VERIFIED) | Нет |
| Своевременность отмены | Задержка синхронизации; риск, если терминал офлайн в момент отмены | Мгновенно | Мгновенно |
| Задержка прохода | Минимальная | + RTT до сервера | + RTT + команда; ученик ждёт |
| Привязка решения к конкретному человеку | Да (идентификация и открытие в одном устройстве) | Да | **Слабая**: команда открывает дверь для того, кто стоит рядом; риск прохода другого человека |
| Совместимость | Базовая функция терминалов СКУД (ожидаемо, NOT VERIFIED) | Зависит от модели/прошивки | Зависит от схемы подключения турникета |
| Сложность | Средняя (синхронизация, reconcile) | Средняя | Низкая, но небезопасна |
| Аудит | События из журнала терминала | Событие + ответ сервера | Событие + команда, связь косвенная |

**Рекомендация (NOT VERIFIED до опроса устройства):** основной — **A** с короткими окнами валидности и outbox, плюс приём событий для журнала. B1 — рассмотреть, если capabilities терминала подтвердят поддержку и поведение при таймауте «deny». B2 — только для ручного «открыть» охранником с экрана КПП, не как механизм автоматического выпуска.

### 11.3 Безопасность детей, данные, проход следом, эвакуация
- **Идентификация несовершеннолетних:** для MVP — карты. Биометрия (лицо) — только после юридического решения: согласие законного представителя, локализация хранения в РК, политика удаления (Закон РК «О персональных данных и их защите»; требует проверки юристом — NOT VERIFIED). Шаблоны лиц не должны попадать в БД этой системы и в логи.
- **Минимизация данных на терминале:** на терминал выхода передавать `employeeNo`, номер карты и, при необходимости, имя; не передавать класс, причину, контакты.
- **Проход следом (tailgating) и передача карты:** ПО это не решает. Нужны: турникет с датчиками прохода и сигналом нарушения (тип барьера — NOT VERIFIED), видеонаблюдение, присутствие охраны, событие «проход не совершён/нарушение» от турникета. Сценарий B2 усиливает этот риск.
- **Подтверждение физического прохода:** только если контроллер турникета передаёт сигнал прохода (pass sensor) в терминал/событие; иначе фиксировать «доступ разрешён», а не «вышел» (`exits.pass_confirmed=false`).
- **Эвакуация:** пожарный вход турникета/терминала (fire alarm → свободный проход) должен оставаться аппаратным и не зависеть от сервера; адаптеру **запретить** команды `alwaysClose`/изменение конфигурации пожарного входа; никаких изменений схемы подключения без инженера СКУД.
- **Учётные данные устройства:** хранить вне репозитория; терминалы — в отдельном VLAN, доступ к ISAPI только с хоста адаптера.

### 11.4 Известное об оборудовании
- Подтверждено ранее (заказчиком): DS-K1T341CM, прошивка V3.3.40, тип accessControlTerminal, `GET /ISAPI/System/deviceInfo` → 200 с авторизацией. В рамках этого аудита к устройствам **не обращались**.
- Не известно: поддерживаемые методы идентификации (лицо/карта/PIN), поддержка remote verification, как подключён турникет (реле терминала / Wiegand / отдельный контроллер), есть ли датчик прохода, отдельные ли терминалы на вход и выход, синхронизация времени (NTP), модели остальных школьных турникетов.

---

## 12. Security and Reliability Risks

| ID | Серьёзность | Проблема | Где | Последствие | Минимальное исправление |
|---|---|---|---|---|---|
| R1 | CRITICAL | Подделка сессии при пустом или дефолтном `SECRET_KEY` [P] | `backend/app/config.py:11`, `deploy/.env.example`, `deploy/docker-compose.yml:23-25` | Любой получает права admin → может выдать разрешения/править учеников | Падать при старте, если ключ < 32 символов или равен дефолту; `${SECRET_KEY:?}` в compose |
| R2 | HIGH | Демо-логины и общий пароль на странице входа; `cli demo` создаёт admin с этим паролем | `frontend/src/pages/Login.tsx:45-72`, `backend/app/cli.py:47-68` | При запуске `demo` на рабочей БД — публичный admin | Показывать блок только при флаге сборки; `demo` только для SQLite/по явному флагу |
| R3 | HIGH | Разрешение после выхода задним числом меняет статус на `ok` [P] | `backend/app/services/day.py:41-47`, `services/advisor.py:70-105` | Сокрытие самовольного выхода; для турникета — неверная модель решения | Хранить статус/ссылку на разрешение в момент выхода; учитывать `granted_at ≤ exit_at` |
| R4 | HIGH | Административные изменения не журналируются (ученики [P], пользователи, роли, инвайты, календарь) | `backend/app/api/admin.py:114-279` | Нельзя расследовать, кто выдал себе роль или переименовал ученика | `audit.log` в этих обработчиках |
| R5 | HIGH (для интеграции) | Нет подтверждения родителя, верхней границы времени, внешнего ID | `backend/app/models.py:68-152` | Автоматический выпуск по неполным данным | Раздел 7.8 |
| R6 | MEDIUM | Сессии не отзываются (logout, смена пароля) [P]; срок 30 дней | `backend/app/services/auth.py:34-43`, `api/auth.py:40-43` | Украденная cookie живёт до 30 дней | `session_version` в users + в токене; короче срок для guard/admin |
| R7 | MEDIUM | Нет ограничения попыток входа [P] | `backend/app/api/auth.py:22-37` | Подбор паролей | Счётчик неудач/задержка по username+IP |
| R8 | MEDIUM | IntegrityError → 500: `update_student` [P], `set_permission` при одновременном первом сохранении [C], `create_student` при гонке [C] | `api/admin.py:125-137`, `services/advisor.py:81-96` | Ошибки у пользователей, потерянные правки | Перехват IntegrityError → 409; upsert |
| R9 | MEDIUM | `created_by` перезаписывается, нет `deleted_by` [P] | `services/advisor.py:95`, `models.py:146-150` | Неясно, кто выдал/отменил | Поля `granted_by/updated_by/deleted_by` |
| R10 | MEDIUM | Один процесс API: планировщик и WS-хаб в памяти; при >1 воркере дубли отчётов и потеря событий | `Dockerfile:24-25`, `scheduler.py`, `events.py` | Ограничение масштабирования | Вынести планировщик в отдельный процесс/лок в БД |
| R11 | MEDIUM | Отчёт теряется, если сервер был выключен в 16:50 (memory jobstore) [C] | `backend/app/scheduler.py:31-42` | Руководство не получит отчёт | Проверка при старте «отчёт за сегодня отправлен?» по audit |
| R12 | MEDIUM | Бэкапы без шифрования, на том же хосте, восстановление не проверялось [C] | `deploy/backup.sh` | Потеря данных при потере сервера; утечка ПДн из файла | Шифрование + копия вне сервера + регулярный тест восстановления |
| R13 | MEDIUM | Нет мониторинга, алертов, структурированных логов [C] | `backend/app/main.py:15` | Отказы незаметны (особенно для адаптера) | health-эндпоинты с проверкой БД/устройств + внешний мониторинг |
| R14 | LOW | Выход можно отметить для деактивированного ученика [P] | `services/exits.py:51-53` | Мусорные записи | Проверять `student.active` |
| R15 | LOW | Офлайн-очередь в localStorage не привязана к пользователю; клиент может сдвинуть время выхода на более раннее в пределах дня [C] | `frontend/src/lib/offlineQueue.ts:35-57`, `services/exits.py:58-63` | Отметка уходит от имени следующего вошедшего; неточное время | Хранить user id в очереди; ограничить сдвиг (например, ≤ 2 ч) |
| R16 | LOW | `--forwarded-allow-ips='*'` при прямом доступе к порту API | `Dockerfile:25`, `docker-compose.yml:28-30` | Подмена схемы/IP в заголовках (IP сейчас не используется) | Ограничить IP прокси |
| R17 | LOW | initData Telegram в query string WebSocket | `backend/app/main.py:38` | Попадание в логи прокси | Первое сообщение WS вместо query |
| R18 | LOW | Нет CSP-заголовка | `deploy/Caddyfile` | Меньше защиты от XSS | Добавить CSP |
| R19 | LOW | `audit_log` изменяем на уровне БД | `models.py:184-194` | Подделка истории при доступе к БД | Права БД: отдельная роль без UPDATE/DELETE |
| R20 | INFO | Время только с точностью до минуты, TIME без пояса | `clock.py:16-19`, `models.py:174` | Недостаточно для корреляции с событиями устройства | `exit_at timestamptz` |

Секреты в репозитории: не обнаружены. `.env` в `.gitignore`/`.dockerignore`; `deploy/.env.example` содержит только пустые значения и несекретные примеры. Демо-пароль `demo-pass-123` присутствует в открытом виде в `README.md`, `backend/app/cli.py` и `frontend/src/pages/Login.tsx` — это осознанный тестовый пароль, но см. R2.

---

## 13. Bugs and Technical Debt

Подтверждённые проверкой:
1. `PUT /api/admin/students/{id}` с ФИО+классом существующего ученика → HTTP 500 (`backend/app/api/admin.py:125-137`). [P]
2. Ретроактивное разрешение меняет статус выхода (R3). [P]
3. `created_by` перезаписывается последним редактором (`backend/app/services/advisor.py:95`). [P]
4. Отметка выхода деактивированного ученика разрешена (`backend/app/services/exits.py:51-53`). [P]
5. Сессия действует после logout и после смены пароля. [P]

По коду (NOT VERIFIED запуском):
6. Гонка в `set_permission`: два первых сохранения на одного ученика одновременно → второй получит IntegrityError → 500 (`backend/app/services/advisor.py:81-96`).
7. «Причина без времени» и её удаление не попадают в audit (`advisor.py:97-101`).
8. `cancel_exit` при двух одновременных отменах — двойная запись в audit (безвредно) (`exits.py:82-97`).
9. CLI-импорт не пишет audit (`backend/app/importer.py:291-316`).
10. Python в среде разработки: `requires-python >=3.12` (`backend/pyproject.toml:5`); на машине аудита установлен 3.11 по умолчанию — тесты запускались на 3.13.
11. README содержит путь Windows конкретной машины `D:\Git\kpp-journal` в командах Docker (README.md:44-50) — не совпадает с текущим расположением репозитория.
12. Предупреждение в тестах: `starlette.testclient` + `httpx` deprecated (версии зависимостей не зафиксированы — `pyproject.toml` использует `>=`), риск поломки при обновлении.
13. Нет lock-файла для Python-зависимостей (frontend зафиксирован `package-lock.json`).
14. Тесты выполняются только на SQLite; поведение partial index и timezone на PostgreSQL не проверяется.

---

## 14. Components to Reuse

Полностью пригодно, **не менять без необходимости**:
- `backend/app/services/normalize.py`, `frontend/src/lib/normalize.ts`, `search.ts`, `shared/search_cases.json` — поиск.
- `backend/app/services/time_parse.py` — разбор времени.
- `backend/app/importer.py` — импорт/diff (добавить только перенос `access_id`, если он будет в xlsx).
- `backend/app/services/auth.py` (хеширование, проверка initData), `backend/app/deps.py` (модель ролей-зависимостей — расширяется новой ролью/зависимостью для устройств).
- `backend/app/events.py` — WebSocket-хаб (адаптер может публиковать `day_changed` через API или общий канал — см. раздел 16).
- `backend/app/notify.py` — уведомления эдвайзеру (переиспользовать для «вышел через турникет», «отказ в выходе»).
- `backend/app/services/calendar.py` — рабочие дни (используется в решении о выходе).
- Тестовая инфраструктура `backend/tests/conftest.py` (подмена часов, in-memory БД, перехват Telegram) — основа для тестов адаптера с фейковым ISAPI.
- Деплой: compose-структура, Caddy, backup (с доработкой).

Переиспользовать для Hikvision:
- `day.py:load_day/get_row` — для отображения выходов через турникет на экране КПП без изменения UI-логики.
- `exits.py:mark_exit` — как образец идемпотентной записи выхода (partial unique index + обработка IntegrityError); для событий устройства нужна отдельная функция `record_device_exit`.
- `audit.log` — для всех решений адаптера.

Сохранить решения без изменений: серверное время как источник истины; soft delete/cancel вместо удаления; «лист дня как выборка»; права эдвайзера по группе; WebSocket без персональных данных.

---

## 15. Required Modifications

Доработать (минимально инвазивно):
- `config.py` / compose — обязательный `SECRET_KEY` (R1).
- `Login.tsx`, `cli.py` — демо только в демо-режиме (R2).
- `api/admin.py` — audit для всех изменений, обработка IntegrityError (R4, R8).
- `models.py` + новая миграция `0002` — поля и таблицы из 7.8.
- `services/advisor.py` — дата разрешения, `valid_until`, подтверждение, неизменяемый `granted_by`, `version`, событие в outbox.
- `services/day.py` — статус выхода с учётом момента выдачи разрешения; новые источники выхода (device).
- `api/advisor.py` + `frontend/src/pages/Advisor.tsx` — поля «до», «подтвердил (родитель/законный представитель/…)», «способ подтверждения», выбор даты/повтора.
- `frontend/src/pages/Kpp.tsx` — отображение источника (🖐 вручную / 🎫 турникет / 📴 офлайн), отказов турникета, состояния устройств.
- `frontend/src/pages/Admin.tsx` — ученики: `access_id` и карты; новый раздел «Устройства» (только чтение статуса для MVP).

Новый код:
- `backend/app/services/release.py` — `decide_exit`.
- `backend/app/integrations/hikvision/{client.py, schemas.py, sync.py, events.py}` и `backend/app/hikvision_worker.py`.
- Модели `Device`, `DeviceEvent`, `DeviceSync`, `StudentCredential`, `RecurringPermission`.
- Сервисная авторизация, если события будут приниматься через HTTP push (API-ключ на устройство + allowlist IP).
- Тестовый фейковый ISAPI-сервер (fixtures) для автотестов адаптера.

---

## 16. Recommended Target Architecture

```
                    ┌──────────────── Postgres ────────────────┐
                    │ students(+access_id), credentials,        │
                    │ permissions(+window,+confirm,+version),   │
                    │ recurring_permissions, exits(+source...), │
                    │ devices, device_events, device_sync, audit│
                    └───────▲───────────────────────▲──────────┘
                            │                       │
  UI / API (как сейчас) ────┤                       │
  services/release.py ◄─────┤                       │
  (decide_exit, чистая)     │                       │
                            │     ┌─────────────────┴─────────────────┐
                            │     │ hikvision_worker (отдельный сервис)│
                            │     │  sync: outbox → UserInfo/CardInfo  │
                            │     │  events: AcsEvent poll (+stream)   │
                            │     │  reconcile: терминал ↔ БД          │
                            │     │  health: deviceInfo, last_seen     │
                            │     └─────────────────┬─────────────────┘
                            │                       │ ISAPI (Digest, HTTPS при наличии)
                            │                VLAN СКУД│
                            │               ┌────────▼────────┐   сухой контакт / Wiegand
                            │               │ Терминал (выход) │──────────► Турникет
                            │               └─────────────────┘   Fire alarm → турникет (аппаратно)
```

Принципы:
- Решение о самостоятельном выходе принимается терминалом по данным, загруженным из системы (сценарий A); система — источник истины и журнал.
- Адаптер — единственный компонент, который говорит с устройствами; режимы `read_only` / `write_test_only` / `write` в конфиге; запись разрешена только в устройства с `is_test=true` до приёмки.
- Связь адаптера с UI: адаптер пишет в БД и вызывает внутренний endpoint API для `day_changed` (или API периодически опрашивает `device_events`). Не делать адаптер частью API-процесса.
- Время: NTP на сервере и терминалах; хранить `device_time` и `received_at`; при расхождении > N сек — алерт.
- Fail-closed для самостоятельного выхода; эвакуация — только аппаратно.

---

## 17. Step-by-Step Implementation Roadmap

### Этап 1. Исправление критических проблем
- Задачи: 1.1 обязательный `SECRET_KEY` (проверка при старте + `${SECRET_KEY:?}` в compose); 1.2 демо-блок на странице входа и `cli demo` — только в демо-режиме; 1.3 audit для admin-операций (ученики, пользователи, роли, инвайты, календарь) и для «причины без времени»; 1.4 перехват IntegrityError → 409 в `update_student`, `create_student`, `set_permission`; 1.5 запрет выхода для неактивного ученика; 1.6 `session_version` для отзыва сессий; 1.7 ограничение попыток входа.
- Файлы: `backend/app/config.py`, `backend/app/main.py`, `deploy/docker-compose.yml`, `deploy/.env.example`, `frontend/src/pages/Login.tsx`, `backend/app/cli.py`, `backend/app/api/admin.py`, `backend/app/services/advisor.py`, `backend/app/services/exits.py`, `backend/app/services/auth.py`, `backend/app/api/auth.py`, `backend/app/models.py` + миграция (для 1.6).
- Зависимости: нет.
- Готово, когда: каждый пункт закрыт автотестом (аналог проверочных сценариев раздела 6); существующие 75 тестов зелёные.
- Тест: `pytest` в изолированном окружении; ручной запуск API с пустым ключом — должен не стартовать.
- В первую очередь: 1.1 и 1.2.

### Этап 2. API и модели для интеграции
- Задачи: миграция `0002` по разделу 7.8 (без `device_*` можно разбить на две миграции); `decide_exit`; статус выхода «на момент события»; разрешения на дату и с `valid_until`; поля подтверждения; `access_id` и карты в админке и импорте (опционально).
- Файлы: `backend/app/models.py`, `backend/alembic/versions/0002_*.py`, новые `backend/app/services/release.py`, правки `services/advisor.py`, `services/day.py`, `api/advisor.py`, `api/admin.py`, `frontend/src/pages/Advisor.tsx`, `frontend/src/pages/Admin.tsx`, `frontend/src/lib/api.ts`.
- Зависимости: Этап 1.
- Готово, когда: `decide_exit` покрыта таблицей тестов (нет разрешения / рано / в окне / поздно / отменено / отменено после выдачи / неактивный / нерабочий день / погашено); `alembic check` чистый; миграция проверена на копии PostgreSQL.
- Тест: unit-тесты `release.py`; API-тесты; upgrade/downgrade на PostgreSQL в Docker с вымышленными данными.
- В первую очередь: `access_id` + `decide_exit`.

### Этап 3. Независимый Hikvision Adapter
- Задачи: ISAPI-клиент (Digest, таймауты, ретраи); read-only функции: `deviceInfo`, capabilities (`/ISAPI/AccessControl/capabilities`, `UserInfo/capabilities`, `AcsEvent/capabilities`, `RemoteControl/door/capabilities` — пути по документации, NOT VERIFIED); опрос `AcsEvent` с курсором; запись `device_events` с дедупликацией; конфиг устройств из env; режимы `read_only`/`write_test_only`.
- Файлы (новые): `backend/app/integrations/hikvision/client.py`, `events.py`, `schemas.py`, `backend/app/hikvision_worker.py`, сервис `hikvision` в `deploy/docker-compose.yml`, `backend/tests/test_hikvision_*.py` с фейковым ISAPI.
- Зависимости: Этап 2 (таблицы `devices`, `device_events`). Read-only опрос capabilities можно начать сразу отдельным скриптом без записи в БД.
- Готово, когда: воркер переживает перезапуск без дублей и пропусков (тест с фейковым сервером); на тестовом терминале получены capabilities и события.
- Тест: автотесты с фейковым ISAPI; ручной прогон в режиме `read_only` против тестового терминала.
- В первую очередь: скрипт опроса capabilities (только GET) → решение, какой сценарий поддерживается.

### Этап 4. Идентификация и управление тестовым турникетом
- Задачи: на тестовом терминале создать 1–2 **вымышленные** персоны с тестовыми картами (не реальные ученики, без биометрии); проверить события идентификации (major/minor, employeeNo, время, номер двери); проверить срабатывание реле/турникета по валидной карте; отдельно — `RemoteControl/door/1` на стенде; проверить пожарный вход (с инженером СКУД, без участия ПО); измерить поведение при отключении сети.
- Файлы: только адаптер и тесты; протокол испытаний (новый документ).
- Зависимости: Этап 3; доступ к стенду; инженер СКУД.
- Готово, когда: задокументировано, что делает терминал при валидной/невалидной/просроченной карте, при недоступном сервере, при пожарном сигнале; подтверждено или опровергнуто физическое открытие.
- Тест: протокол ручных испытаний с фото/видео и выгрузкой событий.

### Этап 5. Подключение разрешений к оборудованию
- Задачи: outbox `device_sync` из `set_permission`/отмены/повторов; применение `UserInfo/Record|Modify|Delete` и карт к терминалу выхода (`is_test=true`); короткие окна `Valid`; reconcile; алерт охране при неподтверждённой отмене.
- Файлы: `services/advisor.py` (постановка в outbox), `integrations/hikvision/sync.py`, модели.
- Зависимости: Этапы 2–4, выбор сценария A/B1.
- Готово, когда: выдача → проход разрешён ≤ N сек; отмена → проход запрещён ≤ N сек; при офлайн-терминале отмена ставится в очередь, охране показывается предупреждение; reconcile исправляет расхождения.
- Тест: автотесты с фейковым ISAPI + испытания на тестовом терминале с вымышленными персонами.

### Этап 6. Регистрация выходов и исключения
- Задачи: `device_event → exits(source='device')` идемпотентно; отказы (`decision='denied'`) — в лист дня/уведомление охране; обработка: неизвестная карта, деактивированный ученик, повторный проход, расхождение часов, события «задним числом» после восстановления связи; экран КПП: источник отметки, отказы, статус устройств; ручная отметка охраной остаётся.
- Файлы: `integrations/hikvision/events.py`, `services/exits.py` (новая функция), `services/day.py`, `frontend/src/pages/Kpp.tsx`, `notify.py`.
- Зависимости: Этап 3 (события), Этап 2.
- Готово, когда: одно событие → ровно одна запись; перезапуск воркера не создаёт дублей; эдвайзер получает «🚪 через турникет».
- Тест: автотесты повторной доставки, out-of-order, сброса serialNo.

### Этап 7. Сквозное тестирование и эксплуатация
- Задачи: E2E на стенде (выдача → проход → журнал → отчёт → отмена → отказ); нагрузочный опрос нескольких терминалов; мониторинг (last_seen устройств, очередь outbox, ошибки); резервные копии с проверкой восстановления; регламент «сервер недоступен» для охраны; согласование ПДн; поэтапное включение по одному терминалу.
- Готово, когда: пройдён чек-лист приёмки раздела 19; есть runbook; владелец подписал протокол.

---

## 18. Testing Strategy

- **Что проверено при аудите** (без изменения репозитория): копия `git archive HEAD` во временной папке, Python 3.13 venv, `DATABASE_URL=sqlite://`, `TELEGRAM_BOT_TOKEN=""`:
  - `pytest` → 75 passed;
  - 11 временных проверочных тестов аудитора (R1, R3, R6, R7, R9, R14, баг №1 и др.) → все подтвердили описанное поведение; файлы удалены;
  - `npm ci && vitest run` → 19 passed; `npm run build` (tsc + vite) → успешно;
  - `alembic upgrade head && alembic check` на временной SQLite → без расхождений.
  - Рабочая БД, Telegram, SMTP, устройства — **не затрагивались**.
- **Безопасно ли запускать тесты проекта:** да — `conftest.py` подменяет `SessionLocal` на in-memory SQLite (`backend/tests/conftest.py:61-67`) и перехватывает Telegram (`:52-58`). Но `app.db.engine` создаётся при импорте из `DATABASE_URL` (`backend/app/db.py:5`); перед запуском явно задавать `DATABASE_URL=sqlite://` и пустой `TELEGRAM_BOT_TOKEN`, чтобы исключить случайное подключение к рабочей БД.
- **Дальше нужно:**
  - CI-прогон тестов на PostgreSQL (partial index, timestamptz);
  - unit-тесты `decide_exit` (таблица истинности);
  - контрактные тесты ISAPI-клиента на записанных ответах тестового терминала (обезличенных);
  - фейковый ISAPI-сервер для тестов воркера (перезапуск, дубли, офлайн, таймауты);
  - ручные стендовые испытания по протоколу Этапа 4;
  - E2E-сценарии Этапа 7;
  - тест восстановления из бэкапа.

---

## 19. MVP Definition and Acceptance Criteria

**MVP:** один тестовый терминал (DS-K1T341CM V3.3.40 или выделенный стенд), подключённый к **тестовому** турникету/реле, изолированный от остальных проходов; 1–3 вымышленные персоны с тестовыми картами; без биометрии; сценарий A; адаптер в режиме `write_test_only` (запись только в устройства с `is_test=true`, allowlist по адресу).

Критерии приёмки:
1. Этап 1 закрыт (R1–R4, R8 исправлены, тесты есть).
2. Выдача разрешения «сегодня 15:05–15:30, подтвердил: законный представитель, по телефону» сохраняется с автором и подтверждением; на терминале появляется валидность в этом окне ≤ 30 сек.
3. Тестовая карта до 15:05 — отказ; в 15:10 — проход; после 15:30 — отказ. Все три события есть в `device_events`, ровно одно в `exits` с `source='device'`, `device_id`, точным временем.
4. Отмена разрешения в 15:12 → проход в 15:13 запрещён; если терминал офлайн — охрана видит предупреждение, после восстановления связи состояние синхронизируется.
5. Перезапуск воркера и повторная выдача тех же событий терминалом не создают дублей.
6. При недоступности сервера терминал работает по загруженным данным; ни один ученик без действующего разрешения не проходит; пожарный вход открывает турникет при выключенном сервере.
7. Остальные терминалы школы не получили ни одного запроса (проверка по логам адаптера).
8. Журнал аудита содержит: выдачу, отмену, синхронизацию, проход, отказ.

---

## 20. Open Questions and External Dependencies

К владельцу проекта / школе:
1. Какие модели и прошивки у **всех** школьных терминалов и турникетов; один терминал на направление или общий; как терминал подключён к турникету (реле, Wiegand, контроллер); есть ли датчик прохода и сигнал tailgating.
2. Способ идентификации учеников: карты (какие — Mifare/EM), лицо, PIN. Есть ли уже выданные карты и их номера.
3. Юридическое решение по биометрии несовершеннолетних, согласиям родителей, сроку хранения, месту хранения (РК).
4. Кто «подтверждает» разрешение: родитель, законный представитель, другое уполномоченное лицо; как фиксируется (звонок, сообщение, бумага); нужен ли список уполномоченных лиц в системе.
5. Нужны ли повторяющиеся разрешения (дни недели, период) и кто их утверждает.
6. Нужна ли верхняя граница времени; что делать после неё.
7. Модель «вышел и вернулся»: может ли ученик выйти дважды за день (вопрос из README.md:83).
8. Что должен делать турникет для ученика **без** разрешения: просто не открываться или вызывать охранника; может ли охрана выпустить вручную (с записью).
9. Политика при недоступности сервера/сети (fail-closed подтвердить).
10. Сетевой доступ: VLAN СКУД, откуда разрешён ISAPI, NTP, учётные записи ISAPI (передать вне репозитория).
11. Доступ к тестовому стенду и инженеру СКУД; разрешение на испытания реле/турникета.
12. Где будет сервер (README.md:80) — влияет на связь с терминалами в школьной сети.
13. Официальная документация ISAPI для DS-K1T341CM V3.3.40 (Hikvision ISAPI Access Control/Person Management) — от поставщика/дистрибьютора.
14. Где находится ТЗ (Ф-1…Ф-25, П-3…П-13) — в репозитории его нет.

Внешние зависимости: Telegram Bot API, SMTP (опционально), Let's Encrypt (Caddy), Docker Hub образы (`postgres:16-alpine`, `caddy:2-alpine`, `python:3.12-slim`, `node:20-slim`), терминалы Hikvision.

---

## 21. Final Technical Assessment

- **Core:** как журнал КПП — готов к пилоту после закрытия R1–R2 (конфигурация и демо-доступ). Код качественный, тесты содержательные, схема согласована с миграцией.
- **Можно ли начинать интеграцию Hikvision:** да, но в правильном порядке: (1) Этап 1; (2) параллельно read-only исследование тестового терминала; (3) Этап 2 до первой записи в устройство. Писать в терминал и связывать разрешения с турникетом до Этапа 2 нельзя.
- **Блокеры:** R1 (CRITICAL); отсутствие внешнего ID, окна времени, подтверждения и функции решения; отсутствие данных о возможностях терминала и схеме подключения турникета; отсутствие юридического решения по идентификации детей.
- **Обязательно до подключения реального оборудования:** Этапы 1–2; изолированный стенд; режим `write_test_only`; аппаратная проверка пожарного входа; согласованная политика fail-closed; учётные данные устройств вне репозитория.
- **Интерфейс:** форма разрешения (дата/повтор, «до», подтверждение); КПП — источник отметки, отказы турникета, статус устройств; админка — `access_id`/карты, раздел «Устройства»; удалить демо-блок со входа.
- **База данных:** раздел 7.8 (access_id, credentials, расширение permissions, recurring_permissions, devices, device_events, device_sync, расширение exits, session_version).
- **API:** параметр даты и новые поля в `PUT /advisor/students/{id}/permission`; эндпоинты повторяющихся разрешений; админ-эндпоинты устройств и карт; (опционально) приём push-событий с авторизацией устройства; внутренний сигнал `day_changed` для воркера.

Оценка по компонентам (субъективно, для приоритизации): ученики/поиск/импорт — 90%; разрешения — 40% от целевой модели; журнал выходов — 50% (ручной есть, устройства нет); авторизация — 65%; аудит — 50%; эксплуатация/надёжность — 50%; интеграция с оборудованием — 0%.

---

## HANDOFF TO NEXT DEVELOPER

**Фактическое состояние.** Работающий веб-журнал КПП (ручная отметка выходов охраной + разовые разрешения эдвайзеров на сегодня + отчёты + Telegram). Никакой интеграции с оборудованием нет. Ветка `test_connection_of_turnstiles` = `main` (`2077ee7`). Тесты зелёные (75 backend, 19 frontend). Найдены и подтверждены дефекты безопасности (раздел 12).

**Ключевые файлы и точки входа.**
- API: `backend/app/main.py` (app, WS, SPA), роутеры `backend/app/api/*.py`, роли `backend/app/deps.py:48-53`.
- Бизнес-логика: `backend/app/services/advisor.py:70-105` (разрешения), `backend/app/services/exits.py:48-97` (выходы), `backend/app/services/day.py:41-47` (статусы), `backend/app/services/audit.py`.
- Схема: `backend/app/models.py`, `backend/alembic/versions/0001_initial_schema.py`.
- Настройки: `backend/app/config.py` (все из env).
- Процессы: API (`Dockerfile:25`), бот (`python -m app.bot`), CLI (`python -m app.cli create-admin|send-report|demo`), импорт (`python -m app.importer file.xlsx [--apply]`).
- Frontend: `frontend/src/App.tsx` (маршруты по ролям), `pages/Kpp.tsx`, `pages/Advisor.tsx`, `pages/Admin.tsx`, `lib/offlineQueue.ts`.
- Деплой: `deploy/docker-compose.yml` (db, api, bot, caddy, backup).

**Граф Graphify.** Перед чтением исходников: `graphify query "<вопрос>"`, `graphify explain "set_permission()" --all`, `graphify affected "Permission"`; после изменений кода — `graphify update .`. Список проверенных запросов — `HTA_STUDENT_RELEASE_GRAPHIFY_ANALYSIS.md`, раздел 12.

**Безопасный локальный запуск тестов (проверено при аудите, без Docker).** Выполнять на копии или с гарантированно тестовыми переменными:
```bash
# backend (Python >= 3.12; на машине аудита: py -3.13)
py -3.13 -m venv .venv-audit && .venv-audit/Scripts/python -m pip install "./backend[dev]"
cd backend
DATABASE_URL=sqlite:// TELEGRAM_BOT_TOKEN= SMTP_HOST= PYTHONDONTWRITEBYTECODE=1 \
  ../.venv-audit/Scripts/python -m pytest -q -p no:cacheprovider
# frontend
cd frontend && npm ci && npx vitest run && npm run build
```
(`pip install` без `-e` ставит пакет не в editable-режиме и не создаёт `*.egg-info` в репозитории; `npm ci` создаёт `node_modules`, он в `.gitignore`.) Вариант через Docker — README.md:42-56 (путь `D:\Git\kpp-journal` нужно заменить на свой). Локальный стек с демо-данными: README.md:52-56 — **только** на отдельной БД с вымышленными данными.

**Важные зависимости и ограничения.**
- API должен работать в **одном** процессе uvicorn (планировщик и WS-хаб в памяти).
- Тесты используют SQLite; prod — PostgreSQL 16.
- Время школы — `Asia/Qyzylorda`; время выхода ставит сервер с точностью до минуты.
- HTA Student Release — отдельный проект; не объединять БД и логику с Budokan Core.
- Не отправлять команды реальным турникетам; не загружать биометрию; не использовать реальные разрешения учеников для тестов.
- Учётные данные терминалов и `SECRET_KEY` — только в `.env`/секрет-хранилище, не в репозитории.

**Первая задача.** Этап 1.1–1.2:
1. В `backend/app/config.py` / `backend/app/main.py` — отказ запуска, если `SECRET_KEY` пуст, короче 32 символов или равен `dev-secret-change-me` (с исключением для тестов через явную переменную); в `deploy/docker-compose.yml` — `SECRET_KEY: ${SECRET_KEY:?задайте SECRET_KEY в .env}`.
2. В `frontend/src/pages/Login.tsx:45-72` — показывать демо-блок только при `import.meta.env.VITE_DEMO === "1"`; в `backend/app/cli.py:47-68` — `demo` только при `DATABASE_URL` на SQLite или с явным флагом `--i-know-this-is-demo`.
3. Тесты на оба пункта. Затем — 1.3 (audit админ-операций) и 1.4 (IntegrityError → 409).

Параллельно (не блокирует): read-only скрипт вне репозитория или в `backend/app/integrations/hikvision/` с режимом `read_only`, выполняющий только `GET /ISAPI/System/deviceInfo` и `GET` capabilities на **тестовом** терминале, чтобы определить поддержку карт/лица, remote verification и событий.

**Что запросить у владельца проекта.** Пункты 1–14 раздела 20; в первую очередь: модели всех терминалов и схему подключения турникетов, способ идентификации (карты?), доступ к тестовому стенду и учётные данные ISAPI (вне репозитория), решение по биометрии несовершеннолетних, кто и как подтверждает разрешение, политику при недоступности сервера, текст ТЗ.
