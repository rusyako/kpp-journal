# HTA Student Release — Graphify Dependency Analysis

Дата: 2026-11-03 · Репозиторий: `kpp-journal` (HTA Student Release) · Граф построен с коммита `2077ee77` (ветка `test_connection_of_turnstiles`).
Дополняет `HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md`. Обозначения связей — как в Graphify: **EXTRACTED** — найдено AST-разбором (подтверждено кодом), **INFERRED** — выведено эвристикой Graphify (требует проверки). Утверждения без подтверждения кодом помечены **NOT VERIFIED**.

---

## 1. Статус подключения Graphify

| Что | Состояние |
|---|---|
| CLI | `graphify 0.9.92`, `C:\Users\Администратор\.local\bin\graphify.exe` (установлен через `uv tool`, интерпретатор `...\AppData\Roaming\uv\tools\graphifyy\Scripts\python.exe`) |
| Skill Claude Code | `~/.claude/skills/graphify/SKILL.md` — установлен, не менялся |
| Хуки Claude Code | в `~/.claude/settings.json` уже есть глобальные `PreToolUse`-хуки `graphify hook-guard search/read` — не менялись; в этой сессии они срабатывают и требуют сначала обращаться к графу |
| MCP | бинарник `graphify-mcp.exe` установлен, но **MCP-сервер в Claude Code не зарегистрирован** (в `~/.claude.json` записей нет); облачного Graphify MCP нет. Граф используется через CLI |
| Git-хуки graphify | не установлены (`graphify hook status` → not installed); по условию задачи не устанавливались |
| Граф до начала работы | отсутствовал (`graphify-out/` не было) |
| Граф сейчас | **построен локально**: `graphify-out/graph.json`, `graph.html`, `GRAPH_REPORT.md` |

## 2. Способ индексации

1. Создан `.graphifyignore` в корне (исключает `deploy/.env*`, `deploy/backups/`, `data/`, `*.xlsx`, `*.db`, `frontend/package-lock.json`, `node_modules/`, `dist/`, `__pycache__/`, `.venv*/`, `graphify-out/`). Также соблюдается `.gitignore` проекта.
2. `graphify extract . --code-only` — только локальный AST-разбор, без LLM и без API-ключей. Документы (README, отчёты) и изображения пропущены (6 файлов).
3. `graphify cluster-only . --no-label` — кластеризация и отчёт; названия 17 сообществ заданы вручную в `graphify-out/.graphify_labels.json` и применены повторным `cluster-only`.
4. Проверка: в `graph.json`/`graph.html` нет `SECRET_KEY`, токенов и ФИО учеников (в т.ч. вымышленных). Единственное «чувствительное» совпадение — строка `demo-pass` из docstring `backend/app/cli.py:48` (публичный демо-пароль, уже лежит в репозитории, см. риск R2 аудита). Совпадения `password` — имена полей/функций (`password_hash`, `verify_password`).
5. Budokan Core не индексировался; граф содержит только файлы этого репозитория.

Файлы, давшие 0 символов (их содержимое в граф не попало): `backend/app/config.py`, `backend/app/db.py`, `backend/pyproject.toml`, `frontend/public/sw.js`, `frontend/vite.config.ts`. Не классифицированы и пропущены: `Dockerfile`, `Caddyfile`, `deploy/docker-compose.yml` и другие файлы без поддерживаемого расширения. Связи с этими файлами нужно смотреть в аудите, а не в графе.

## 3. Статистика графа

- 59 исходных файлов, **560 узлов, 1534 ребра, 17 сообществ**.
- Связи: `calls` 318, `contains` 306, `imports_from` 287, `imports` 235, `references` 163, `uses` 110, `rationale_for` 60 (docstrings), `indirect_call` 19, `inherits` 18, `method` 18.
- Достоверность: 1392 EXTRACTED (91%) / 142 INFERRED (9%) / 0 AMBIGUOUS. Токены LLM: 0.
- Циклов импорта: **не обнаружено** (`GRAPH_REPORT.md`, раздел Import Cycles).
- Хабы (god nodes): `User` 63, `Student` 28, `apply_import()` 24, `api()` (frontend) 22, `DayRow` 21, `Role` 20, `Advisory` 20, `mark_exit()` 20, `set_permission()` 18, `format_time()` 18.

Сообщества:

| # | Название | Узлов | Основные файлы |
|---|---|---|---|
| 0 | Permissions API, Models & Migrations | 94 | `models.py`, `api/advisor.py`, `services/advisor.py`, `alembic/*` |
| 1 | Students, Import & Admin API | 89 | `api/admin.py`, `importer.py` |
| 2 | Frontend Pages & API Types | 82 | `frontend/src/App.tsx`, `pages/*`, `lib/api.ts` |
| 3 | Backend Test Fixtures & Auth | 59 | `tests/conftest.py`, `tests/test_api.py`, `services/auth.py` |
| 4 | Day Sheet Statuses & Notifications | 58 | `services/day.py`, `notify.py`, `services/report.py` |
| 5 | App Entry, WebSocket & Bot | 42 | `main.py`, `events.py`, `deps.py`, `bot.py`, `scheduler.py` |
| 6 | KPP Exits, Clock & Audit | 35 | `api/kpp.py`, `services/exits.py`, `clock.py`, `services/audit.py` |
| 7 | Frontend Package Config | 26 | `frontend/package.json` |
| 8 | Frontend Search & Normalize | 19 | `frontend/src/lib/search.ts`, `normalize.ts` |
| 9 | Backend Search Reference | 17 | `services/search.py`, `services/normalize.py`, `tests/test_search.py` |
| 10 | TypeScript Config | 15 | `frontend/tsconfig.json` |
| 11 | Admin CLI & Demo Seed | 11 | `cli.py` |
| 12 | Login & Sessions | 8 | `api/auth.py` |
| 13–16 | Backup Script, Tests Package Init, Service Worker, Repository Root | 1–2 | — |

Низкая связность сообществ 0 и 1 (cohesion 0.06) объясняется тем, что модели (`models.py`) — общий хаб для всех слоёв, а не плохой декомпозицией.

## 4. Карта основных модулей

```
frontend/src/pages/*.tsx ──api()──► (HTTP, в графе НЕ связано) ──► backend/app/api/*.py
                                                                      │ calls / indirect_call
backend/app/api/kpp.py      ──► services/exits.py, services/day.py, services/audit.py, services/calendar.py
backend/app/api/advisor.py  ──► services/advisor.py ──► services/day.py, time_parse.py, audit.py, events.py
backend/app/api/admin.py    ──► importer.py, services/report.py, services/invites.py, services/auth.py, scheduler.py
backend/app/api/auth.py     ──► services/auth.py, services/audit.py, services/calendar.py, services/advisor.py
backend/app/main.py         ──► api/*, deps.resolve_user, events.Hub, scheduler
services/* ──► models.py (Student, Permission, Exit, AuditLog, User ...) ──► db.py
notify.py ◄── services/exits.py ; services/report.py ──► notify.py
```

**Важно:** в графе **0 рёбер** между frontend и backend. AST не связывает строки URL (`api("/api/exits")`) с обработчиками FastAPI. Соответствие установлено вручную по коду (аудит, раздел 8):

| Frontend | URL | Backend-обработчик |
|---|---|---|
| `frontend/src/pages/Kpp.tsx:43,107,129` | `GET /api/day`, `POST /api/exits`, `POST /api/exits/{id}/cancel` | `backend/app/api/kpp.py:20,45,50` |
| `frontend/src/lib/offlineQueue.ts:46` | `POST /api/exits` (`client_time`) | `backend/app/api/kpp.py:45` |
| `frontend/src/pages/Advisor.tsx:30,118` | `PUT /api/advisor/students/{id}/permission`, `GET /api/advisor/advisories/{id}` | `backend/app/api/advisor.py:37,20` |
| `frontend/src/pages/Admin.tsx` (11 вызовов) | `/api/admin/*` | `backend/app/api/admin.py` |
| `frontend/src/pages/Reports.tsx:21,36,55` | `/api/admin/reports/{d}/send`, `/api/reports/{d}/html`, `/api/audit` | `backend/app/api/admin.py:295,290`, `api/kpp.py:55` |
| `frontend/src/App.tsx` (`load`) | `GET /api/me` | `backend/app/api/auth.py:46` |
| `frontend/src/lib/live.ts` | `WS /api/ws` | `backend/app/main.py:37` |

## 5. Цепочки вызовов ключевых функций (по графу)

Все рёбра ниже — EXTRACTED, если не указано иное. Номера строк — из `source_location` графа.

**Разрешение:** `put_permission()` `api/advisor.py:L38` → (calls L42) `set_permission()` `services/advisor.py:L70` →
`today()` L72 · `can_edit()` L76 · `AdvisorError` L75 · `now()` L86 · `Permission(...)` L89 · `parse_time()` L91 · `audit.log()` L99 · `format_time()` L99 · `events.day_changed()` L104 · `get_row()` L105 → `load_day()` `services/day.py:L129` · `advisor_row()` L105.

**Отметка выхода:** `create_exit()` `api/kpp.py:L47` → (indirect_call, INFERRED — вызов через `_result(mark_exit, ...)`) `mark_exit()` `services/exits.py:L48` →
`today()` L50 · `ExitError` L53 · `_active_exit()` L54 · `now_minute()` L57 · `Exit(...)` L65 · `get_row()` L73 · `audit.log()` L74 · `events.day_changed()` L77 · `notify.exit_changed()` L78 · `exit_message()` L79.
**В графе нет ни одного ребра `mark_exit()` → `Permission`** — подтверждение того, что выход не проверяет разрешение.

**Отмена выхода:** `remove_exit()` `api/kpp.py:L52` → (INFERRED) `cancel_exit()` `services/exits.py:L82` → `_active_exit()` L85, `get_row()` L88, `now()` L89, `audit.log()` L91, `day_changed()` L95, `exit_changed()` L96.

**Лист дня / статус:** `day()` `api/kpp.py:L27` → `load_day()` `services/day.py:L70` → uses `Permission` L73, `Exit` L75, `Student` L79 (INFERRED) → `DayRow` L91 → `sort_rows()` L105. `DayRow.status()` `services/day.py:L42` читают: `.to_dict()` L65, `.color()` L51, `advisor_row()` `services/advisor.py:L58`, `exit_message()` `services/exits.py:L37`, `exit_text()` `notify.py:L106` (последние три — INFERRED).

**Авторизация:** `current_user()` `deps.py:L33` → `resolve_user()` `deps.py:L19` → `validate_init_data()` L23, `read_session()` L27; `websocket()` `main.py:L41` → `resolve_user()`. `require()` `deps.py:L39` → `dependency()` (INFERRED). `login()` `api/auth.py` → `make_session()`, `verify_password()`, `audit.log()` L27.

**Журналирование:** вызывающие `audit.log()` `services/audit.py:L12` по графу — ровно 6: `mark_exit()`, `cancel_exit()`, `set_permission()`, `send_report()`, `import_list()`, `login()`. **Не вызывают** `create_student()`, `update_student()`, `create_user()`, `update_user()`, `invite_user()`, `put_school_day()`, `delete_school_day()` — подтверждает риск R4 аудита.

**Расписание/время:** `is_working_day()` `services/calendar.py:L10` вызывают `day()` `api/kpp.py:L26`, `me()` `api/auth.py:L55`, `daily_report()` `scheduler.py:L24`. **Не вызывают** `mark_exit()` и `set_permission()`. `parse_time()` вызывает только `set_permission()` (+ тесты).

**События:** `day_changed()` `events.py:L55` вызывают только `mark_exit()`, `cancel_exit()`, `set_permission()`; `Hub.publish()` → `_send_all()`.

**Внешние интеграции:** Telegram/SMTP — `send_telegram()`, `send_email()` в `notify.py` (вызываются из `exit_changed()`, `send_report()`); бот `bot.py` → `redeem_invite()`. Модулей оборудования (Hikvision/ISAPI) в графе нет.

**Тесты:** fixtures `tests/conftest.py` (`db()`, `now()`, `sent()`, `login()`, `guard()`, `advisor()`, `admin()`) связаны с `apply_import()`, `hash_password()`, `Base`; API-тесты вызывают эндпоинты через HTTP-клиент — **в графе это не видно**, связь тест → обработчик установлена по коду (`backend/tests/test_api.py`). Прямо связанные в графе тесты: `test_time_parse.py` → `parse_time()`, `test_search.py` → `search()`/`normalize()`, `test_importer.py` → `apply_import()`, `Permission`, `Student`.

## 6. Зависимости базы данных и API

Обратное влияние (`graphify affected`, глубина 2):

| Модель | Кто зависит (прямые рёбра) |
|---|---|
| `Permission` `models.py:L133` | `set_permission()` (создание), `load_day()` (чтение), `test_reimport_keeps_permissions_and_history()`; через `load_day()` — `day()`, `advisory_rows()`, `get_row()`, `build_report()`, `put_permission()` |
| `Exit` `models.py:L155` | `mark_exit()` (создание), `_active_exit()`, `load_day()`, `build_report()`; далее `create_exit()`, `cancel_exit()`, `day()`, `report_json()`, `report_html()`, `send_report()` |
| `Student` `models.py:L68` | 26 узлов: `apply_import()`, `load_existing()`, `create_student()`, `update_student()`, `list_students()`, `list_advisories()`, `health()`, `_student_dict()`, `set_permission()`, `mark_exit()`, `load_day()`, `get_row()`, `build_report()`, `entries_for_day()`, тесты |
| `User` `models.py:L85` | главный хаб (63 ребра), из них 45 INFERRED — в основном аннотации типов `user: User` в обработчиках |
| `load_day()` | 21 зависимый узел — любой сдвиг в этой функции затрагивает КПП, эдвайзеров, отчёт и рассылку |

Рёбра `uses` между функциями и моделями в основном **INFERRED** (Graphify выводит их по использованию имени класса в теле функции); прямые конструкторы (`Permission(...)`, `Exit(...)`) — EXTRACTED. Рёбра `imports_from` на глубине 2 — транзитивные модульные импорты, а не реальные вызовы (например, `api/auth.py` попадает в «влияние» `Permission` только через импорт `services/advisor.py`).

## 7. Цепочка создания и проверки разрешения

Запрошенная цепочка: **Создание → Сохранение → Проверка условий → Принятие решения → Регистрация результата.**

| Шаг | Есть в коде/графе? | Где |
|---|---|---|
| 1. Создание | ✅ EXTRACTED | `Advisor.tsx:30` → HTTP (не в графе) → `put_permission()` `api/advisor.py:L38` → `set_permission()` `services/advisor.py:L70`; права — `can_edit()` L76; разбор времени — `parse_time()` L91 |
| 2. Сохранение в БД | ✅ EXTRACTED | `Permission(...)` L89, soft delete через `deleted_at` (L86), `db.commit()`; аудит `audit.log()` L99; сигнал `day_changed()` L104 |
| 3. Проверка условий | ⚠️ частично | только при чтении: `load_day()` выбирает неудалённое разрешение на дату (`services/day.py:L73`); `DayRow.status()` L42 сравнивает `exit_time` с `allowed_time`. Проверок окна «до», рабочего дня, подтверждения, момента выдачи — **нет** |
| 4. Принятие решения | ❌ **отсутствует** | нет функции «разрешить/запретить». `mark_exit()` записывает выход без обращения к `Permission` (в графе нет ребра) |
| 5. Регистрация результата | ✅ (ручная) | `mark_exit()` → `Exit(...)` L65 → `audit.log()` L74 → `notify.exit_changed()` L78; статус выхода вычисляется **задним числом** `DayRow.status()` и меняется, если разрешение изменили позже (подтверждено проверкой, аудит R3) |

## 8. Потенциальные точки интеграции Hikvision

Подтверждённые (по графу и коду) точки и предлагаемые новые компоненты (новые — **не существуют**, предложение):

| Вопрос | Ответ | Основание |
|---|---|---|
| 1. Где брать действующее разрешение | Сейчас — `load_day()`/`get_row()` `services/day.py:L70,L125` (единственное место чтения `Permission`). Для решения — новая функция в новом `services/release.py`, переиспользующая запрос из `load_day()` | EXTRACTED: `load_day()` uses `Permission` L73 — единственный читатель |
| 2. Какой сервис принимает решение | Новый `services/release.py: decide_exit()`. Существующего кандидата нет: `DayRow.status()` — классификация после выхода, `mark_exit()` разрешения не читает | отсутствие ребра `mark_exit → Permission` |
| 3. Где сопоставлять Student ID ↔ Hikvision Person ID | Новое поле `Student.access_id` + таблица учётных данных в `models.py`; редактирование — рядом с `create_student()/update_student()` `api/admin.py`; опционально в `apply_import()` `importer.py` | `Student` хаб (26 зависимых) — добавлять только nullable-поля |
| 4. Обработка событий терминала | Новый пакет `backend/app/integrations/hikvision/` + отдельный процесс `hikvision_worker` (по образцу `bot.py` — `run()` в сообществе 5). Не в `main.py`: там `lifespan()` с планировщиком и `Hub` в одном процессе | `lifespan()` → `scheduler.start()`, `Hub.bind_loop()` |
| 5. Где сохранять подтверждённые проходы | Новая таблица событий устройства + новая функция рядом с `mark_exit()` в `services/exits.py`, повторяющая её схему (уникальный индекс + перехват IntegrityError), с `audit.log()`, `day_changed()`, `notify.exit_changed()` | цепочка `mark_exit()` раздела 5 |
| 6. Обработка отмены разрешения | Точка — `set_permission()` (ветка пустого времени, `deleted_at`, L84-86): постановка задачи синхронизации в outbox после `db.commit()`, рядом с `day_changed()` L104 | `set_permission()` — единственный писатель `Permission` |
| 7. Что придётся изменить | `models.py` (+миграция), `services/advisor.py:set_permission`, `services/day.py:load_day/DayRow.status`, `services/exits.py` (новая функция), `api/advisor.py:PermissionIn/put_permission`, `api/admin.py` (ученики/устройства), `frontend/src/pages/{Advisor,Kpp,Admin}.tsx`, `frontend/src/lib/api.ts`, `deploy/docker-compose.yml` | см. раздел 9 |
| 8. Что не трогать | `services/normalize.py`, `services/search.py`, `frontend/src/lib/{search,normalize}.ts` (сообщества 8–9, изолированы), `services/time_parse.py`, `services/auth.py`, `services/invites.py`, `bot.py`, `events.Hub`, `services/calendar.py` (только вызывать), `importer.build_diff()` | нет рёбер к Permission/Exit |

## 9. Анализ влияния предлагаемых изменений

| Изменение | Затронутые узлы (по `graphify affected`) | Риск |
|---|---|---|
| Новые nullable-поля в `Student` | 26 зависимых, но поля не меняют существующие запросы; `_student_dict()`, `StudentIn` — только если поля выводить в UI | Низкий |
| Новые поля в `Permission` (`valid_until`, `granted_by`, подтверждение, `version`) | `set_permission()`, `load_day()`, `DayRow`, `advisor_row()`, тест `test_reimport_keeps_permissions_and_history()` | Средний — `load_day()` питает 21 узел (КПП, эдвайзер, отчёт, рассылка) |
| Изменение логики `DayRow.status()` (статус «на момент выхода») | `.to_dict()`, `.color()`, `advisor_row()`, `exit_message()`, `exit_text()`, `build_report()` → отчёт; тесты П-3, П-6/П-7, П-11 | Средний — меняются цвета/тексты и цифры отчёта |
| Новая функция записи выхода от устройства в `services/exits.py` | только новые вызовы; общие зависимости `get_row()`, `audit.log()`, `day_changed()`, `exit_changed()` | Низкий |
| Новые поля в `Exit` (`source`, `device_id`, `exit_at`...) | `mark_exit()`, `_active_exit()`, `load_day()`, `build_report()`, `cancel_exit()` | Средний — частичный уникальный индекс `uq_exits_active` должен остаться |
| Outbox-вызов в `set_permission()` | `put_permission()` (единственный вызывающий) | Низкий |
| `decide_exit()` в новом модуле | новые рёбра к `Permission`, `Student`, `is_working_day()`, `clock` | Нет влияния на существующее |
| Новый сервис `hikvision_worker` | не входит в граф API; общие только `models.py`, `db.py` | Низкий при отдельном процессе |

## 10. Критически важные файлы

| Файл | Почему |
|---|---|
| `backend/app/models.py` | все сущности; хабы `User`, `Student`, `Permission`, `Exit` |
| `backend/app/services/advisor.py` | `set_permission()` — единственный писатель разрешений |
| `backend/app/services/day.py` | `load_day()` — единственный читатель разрешений; `DayRow.status()` — логика статусов |
| `backend/app/services/exits.py` | `mark_exit()`/`cancel_exit()` — запись выходов |
| `backend/app/services/audit.py` | `log()` — журнал (6 вызывающих) |
| `backend/app/deps.py`, `backend/app/services/auth.py` | авторизация и роли |
| `backend/app/api/advisor.py`, `backend/app/api/kpp.py`, `backend/app/api/admin.py` | HTTP-контракты |
| `backend/app/main.py`, `backend/app/events.py`, `backend/app/scheduler.py` | процесс, WebSocket, планировщик |
| `backend/alembic/versions/0001_initial_schema.py` | схема БД |
| `backend/app/config.py` (в графе пуст — нет символов) | `SECRET_KEY`, TZ, БД |
| `frontend/src/pages/Kpp.tsx`, `Advisor.tsx`, `frontend/src/lib/api.ts`, `offlineQueue.ts` | UI охраны/эдвайзера, контракты типов |
| `deploy/docker-compose.yml`, `Dockerfile` (в графе отсутствуют) | процессы и деплой |

## 11. Циклические зависимости

`GRAPH_REPORT.md`: **Import Cycles — None detected.** Слои однонаправлены: `api → services → models/clock/config`. `notify.py` импортирует `services/day.py`, а `services/exits.py` и `services/report.py` импортируют `notify.py` — это не цикл (day не импортирует notify).

## 12. Команды и запросы Graphify

Выполнять из корня репозитория. Идентификаторы в коде — английские, поэтому запросы лучше писать по-английски или именами функций.

```bash
# обзор
graphify god-nodes --top 15
cat graphify-out/GRAPH_REPORT.md          # открыть graphify-out/graph.html в браузере

# проверено в этой сессии — работает
graphify query "put permission endpoint"            # находит put_permission(), set_permission(), Permission
graphify query "set permission advisor student"
graphify query "student model"
graphify query "mark exit guard audit"
graphify explain "set_permission()" --all           # создание разрешения
graphify explain "mark_exit()" --all                # запись выхода (без проверки разрешения)
graphify explain "load_day()" --all                 # чтение разрешений
graphify explain backend_app_services_day_dayrow_status   # проверка статуса (DayRow.status)
graphify explain backend_app_models_student --all   # модель ученика (имя Student неоднозначно: есть тип во frontend)
graphify path "put_permission()" "set_permission()"
graphify affected "Permission" --depth 2
graphify affected "Exit" --depth 2
graphify affected "load_day()" --depth 2
graphify affected backend_app_models_student --depth 1

# после изменения кода (AST, без затрат)
graphify update .
```

Неоднозначные имена (`Student`, `DayRow`, `User`, `Role`, `search()`, `words()`) существуют и в backend, и во frontend — используйте id узла (`backend_app_models_student`, `backend_app_services_day_dayrow`, `frontend_src_lib_api_dayrow`).
Запрос «permission check / decide exit» не находит функции решения — её нет в коде (это ожидаемо, а не ошибка графа).

## 13. Готовность к следующей сессии

- Граф лежит в `graphify-out/` (2.7 МБ, вместе с кэшем AST). Глобальные хуки и skill уже заставляют Claude Code сначала обращаться к графу — дополнительная настройка не нужна.
- `graphify-out/` **не в `.gitignore`** и пока не закоммичен. Решение за владельцем: закоммитить `graph.json`/`GRAPH_REPORT.md`/`graph.html` для команды или добавить `graphify-out/` в `.gitignore`. `.gitignore` не менялся. Файлы `graphify-out/.graphify_python` и `.graphify_root` содержат локальные пути этой машины.
- `.graphifyignore` создан в корне — его стоит закоммитить вместе с графом.
- Для автоматического обновления после коммитов можно установить `graphify hook install` (не выполнялось по условию).
- Если нужен доступ через MCP: `graphify-mcp.exe` установлен; регистрация в Claude Code (`claude mcp add ...`) **не выполнялась**, чтобы не менять пользовательскую конфигурацию. Точный синтаксис запуска MCP-сервера — NOT VERIFIED.
- Ограничения графа: нет HTTP-связей frontend↔backend, нет связей тест→эндпоинт через TestClient, нет содержимого `config.py`, `Dockerfile`, compose. Эти связи описаны в аудите.
