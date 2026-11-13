# Graph Report - kpp-journal  (2026-11-13)

## Corpus Check
- 126 files · ~337,726 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 6, .ini 1, .mako 1)

## Summary
- 1180 nodes · 3248 edges · 93 communities (54 shown, 39 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 549 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2077ee77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- admin.py
- Students, Import & Admin API
- App.tsx
- Backend Test Fixtures & Auth
- 9. Анализ влияния предлагаемых изменений
- main.py
- create_exit
- Frontend Package Config
- services/pilot.py
- Backend Search Reference
- TypeScript Config
- conftest.py
- api/auth.py
- Backup Script
- Repository Root
- test_pilot_api.py
- User
- test_release.py
- HTA Student Release — Technical Audit
- parsing.py
- adapter.py
- set_permission
- Pilot.tsx
- api/pilot.py
- test_hik_adapter.py
- Kpp.tsx
- api/advisor.py
- 5. Цепочки вызовов ключевых функций (по графу)
- load
- Admin.tsx
- diagnostics.py
- export_hikvision_users.py
- HikDevice
- 2. Что говорит документация (§10.16, FRT с.125–136)
- client.py
- IsapiClient
- MVP: внешняя авторизация выхода через Hikvision — реализация
- ISAPI Endpoint Index (auto-generated)
- Role
- sqlalchemy
- Exit
- scheduler.py
- План безопасного физического пилота (employeeNo `3818077855`)
- Покрытие исходных документов
- Стратегия доступа учеников: «опознаёт Hikvision, выпускает kpp-journal»
- Hub
- Двери, турникеты, реле, расписания
- now
- parse_time
- ISAPI API Reference — что нужно kpp-journal
- Аутентификация, подключение, таймауты
- События: распознавание лиц, доступ, проход
- Пользователи, employeeNo, лица, карты, права
- Reports.tsx
- HTA Student Release — Graphify Dependency Analysis
- notify.py
- Ошибки ISAPI
- База знаний Hikvision ISAPI для kpp-journal
- Проверка возможностей конкретного терминала
- p001-025.md
- kpp-journal — инструкции для Claude Code
- TelegramWebApp
- 03_error_code.md
- 04_field_dictionary.md

## God Nodes (most connected - your core abstractions)
1. `User` - 87 edges
2. `5. Цепочки вызовов ключевых функций (по графу)` - 60 edges
3. `set_permission()` - 33 edges
4. `MockHikvisionDevice` - 32 edges
5. `mark_exit()` - 31 edges
6. `api()` - 31 edges
7. `now()` - 30 edges
8. `IsapiClient` - 30 edges
9. `Student` - 30 edges
10. `apply_import()` - 29 edges

## Surprising Connections (you probably didn't know these)
- `7.7 Достаточно ли данных для автоматического решения о выходе` --references--> `audit_log()`  [INFERRED]
  HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md → backend/app/api/kpp.py
- `7.5 Дата, время, часовые пояса` --references--> `now()`  [INFERRED]
  HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md → backend/app/clock.py
- `21. Final Technical Assessment` --references--> `day_changed()`  [INFERRED]
  HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md → backend/app/events.py
- `2. Персоны (UserInfo) [FRT §10.15, с.117–125]` --references--> `get()`  [INFERRED]
  docs/hikvision/USER_MANAGEMENT.md → backend/app/integrations/hikvision/diagnostics.py
- `4. Карта основных модулей` --references--> `load()`  [INFERRED]
  HTA_STUDENT_RELEASE_GRAPHIFY_ANALYSIS.md → backend/app/integrations/hikvision/settings.py

## Import Cycles
- None detected.

## Communities (93 total, 39 thin omitted)

### Community 0 - "admin.py"
Cohesion: 0.17
Nodes (3): AuditLog, Student, render_html()

### Community 1 - "Students, Import & Admin API"
Cohesion: 0.08
Nodes (34): _diff_dict(), import_list(), demo(), advisory_kind(), advisory_sort_key(), apply_import(), update(), build_diff() (+26 more)

### Community 2 - "App.tsx"
Cohesion: 0.16
Nodes (21): App(), HOME, NAV, readCachedMe(), Session, SessionContext, TopBar(), useReloadMe() (+13 more)

### Community 3 - "Backend Test Fixtures & Auth"
Cohesion: 0.05
Nodes (46): Invite, create_invite(), redeem_invite(), admin(), advisor(), Clock, guard(), login() (+38 more)

### Community 4 - "9. Анализ влияния предлагаемых изменений"
Cohesion: 0.24
Nodes (11): exit_text(), advisor_row(), status_text(), DayRow, _name_key(), sort_rows(), key(), exit_message() (+3 more)

### Community 5 - "main.py"
Cohesion: 0.16
Nodes (5): run(), lifespan(), spa(), websocket(), stop()

### Community 6 - "create_exit"
Cohesion: 0.24
Nodes (5): create_exit(), ExitIn, remove_exit(), _result(), ExitError

### Community 7 - "Frontend Package Config"
Cohesion: 0.06
Nodes (40): dependencies, react, react-dom, react-router-dom, devDependencies, @types/react, @types/react-dom, typescript (+32 more)

### Community 8 - "services/pilot.py"
Cohesion: 0.11
Nodes (24): HikSettings, Base, HikConfigSnapshot, HikEvent, HikPerson, HikPilotState, ReleaseDecision, ReleasePermission (+16 more)

### Community 9 - "Backend Search Reference"
Cohesion: 0.22
Nodes (12): normalize(), words(), Candidate, _prefix_match(), search(), SearchResult, _sort_key(), _substring_match() (+4 more)

### Community 10 - "TypeScript Config"
Cohesion: 0.13
Nodes (14): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noUnusedLocals, noUnusedParameters (+6 more)

### Community 12 - "api/auth.py"
Cohesion: 0.16
Nodes (10): login(), LoginIn, logout(), current_user(), get_db(), resolve_user(), make_session(), read_session() (+2 more)

### Community 17 - "test_pilot_api.py"
Cohesion: 0.09
Nodes (20): MockHikvisionDevice, TerminalOutcome, test_parse_crlf_and_employee_no_variants(), test_parse_plain_json_and_xml(), _gateway_device(), iso(), ready(), simulation() (+12 more)

### Community 18 - "User"
Cohesion: 0.13
Nodes (32): _apply_user(), _commit_user(), create_student(), create_user(), delete_school_day(), health(), invite_user(), list_advisories() (+24 more)

### Community 19 - "test_release.py"
Cohesion: 0.13
Nodes (28): HikPassage, face(), permit(), test_a_no_permission_deny(), test_b_permission_not_started_deny(), test_c_valid_permission_allow(), test_card_and_other_events_not_in_pilot(), test_d_expired_permission_deny() (+20 more)

### Community 20 - "HTA Student Release — Technical Audit"
Cohesion: 0.06
Nodes (33): Device, 0. Краткая сводка, 11.1 Ответы на вопросы задачи, 11.2 Сравнение сценариев, 11.3 Безопасность детей, данные, проход следом, эвакуация, 11.4 Известное об оборудовании, 11. Hikvision Integration Readiness, 15. Required Modifications (+25 more)

### Community 21 - "parsing.py"
Cohesion: 0.11
Nodes (20): _boundary(), classify(), _is_image(), normalize(), parse_request(), parse_time(), parse_xml(), ParsedEvent (+12 more)

### Community 22 - "adapter.py"
Cohesion: 0.12
Nodes (14): health(), listen(), _process(), GatewayResult, handle_device_request(), is_trusted(), _process(), _put_async() (+6 more)

### Community 23 - "set_permission"
Cohesion: 0.18
Nodes (18): put_permission(), day_changed(), set_permission(), log(), get_row(), load_day(), _active_exit(), cancel_exit() (+10 more)

### Community 24 - "Pilot.tsx"
Cohesion: 0.13
Nodes (24): CATEGORY, COMMAND_STATUS, CommandRow, Commands(), dateTime(), DecisionRow, Decisions(), Devices() (+16 more)

### Community 25 - "api/pilot.py"
Cohesion: 0.20
Nodes (16): _call(), check_device(), confirm(), ConfirmIn, create_permission(), enabled(), EnabledIn, PermissionIn (+8 more)

### Community 26 - "test_hik_adapter.py"
Cohesion: 0.22
Nodes (14): check_operation(), ForbiddenOperation, device(), settings(), test_credentials_come_from_env_only(), test_diagnostics_on_mock_is_read_only(), test_digest_and_read_only_requests(), test_forbidden_operations_in_every_mode() (+6 more)

### Community 27 - "Kpp.tsx"
Cohesion: 0.18
Nodes (19): AdvisorRow, AdvisoryView, ApiError, Day, DayRow, ExitResult, OfflineError, RowStatus (+11 more)

### Community 28 - "api/advisor.py"
Cohesion: 0.13
Nodes (12): advisories(), advisory(), PermissionIn, me(), audit_log(), today(), advisory_rows(), can_edit() (+4 more)

### Community 29 - "5. Цепочки вызовов ключевых функций (по графу)"
Cohesion: 0.13
Nodes (14): require(), dependency(), exit_changed(), report_chat_ids(), send_email(), send_telegram(), _submit(), daily_report() (+6 more)

### Community 30 - "load"
Cohesion: 0.15
Nodes (12): _csv(), _int(), load(), Mode, check_device(), _last_serial(), PilotError, revoke_permission() (+4 more)

### Community 31 - "Admin.tsx"
Cohesion: 0.19
Nodes (18): api(), Role, AdvisoriesTab(), Advisory, CalendarTab(), DIFF_TITLES, HealthTab(), ImportCard() (+10 more)

### Community 32 - "diagnostics.py"
Cohesion: 0.18
Nodes (7): AuthLockout, _find(), main(), redact(), run(), verdict(), test_redact_hides_passwords_and_names()

### Community 33 - "export_hikvision_users.py"
Cohesion: 0.24
Nodes (10): check_total(), create_session(), describe_401(), export_users(), get_page(), load_state(), main(), save_json() (+2 more)

### Community 34 - "HikDevice"
Cohesion: 0.18
Nodes (13): main(), pilot_device(), pilot_setup(), _timeout(), HikDevice, HikDirection, ensure_setup(), db() (+5 more)

### Community 35 - "2. Что говорит документация (§10.16, FRT с.125–136)"
Cohesion: 0.12
Nodes (15): 1. Целевая логика kpp-journal, 2.1 Назначение, 2.2 Четыре механизма, 2.3 Параметры `AcsCfg` (настройка — `PUT /ISAPI/AccessControl/AcsCfg?format=json`), 2.4 Значения `remoteCheckVerifyMode` [FRT с.127], 2.5 Запрос от устройства (пример, FRT с.130 и 132–133), 2.6 Ответ платформы, 2.7 Событие с результатом (+7 more)

### Community 36 - "client.py"
Cohesion: 0.17
Nodes (3): credentials_for(), IsapiError, NetworkDisabled

### Community 37 - "IsapiClient"
Cohesion: 0.26
Nodes (3): IsapiClient, IsapiResponse, 4. Удалённое управление дверью [FRT §14.6.14, с.517–519]

### Community 38 - "MVP: внешняя авторизация выхода через Hikvision — реализация"
Cohesion: 0.13
Nodes (12): sent(), 10. Соответствие документации и открытые вопросы, 11. Ограничения MVP, 1. Принцип, 2. Что сделано, 4. Decision Engine — правила (`release.decide_exit`), 5. Разделение «решение / команда / проход», 6. Данные (+4 more)

### Community 39 - "ISAPI Endpoint Index (auto-generated)"
Cohesion: 0.15
Nodes (13): 14.10 Video Intercom (General), 14.11 Security Control Device (General), 14.12 Zone Alarm, 14.1 Device (General), 14.2 Network Settings, 14.3 Face Capture, 14.4 VCA, 14.5 Two-Way Audio (+5 more)

### Community 40 - "Role"
Cohesion: 0.23
Nodes (4): greeting(), open_button(), start(), Role

### Community 41 - "sqlalchemy"
Cohesion: 0.23
Nodes (3): downgrade(), upgrade(), upgrade()

### Community 42 - "Exit"
Cohesion: 0.18
Nodes (8): now_minute(), Exit, 1. Как работает система сейчас (проверено по коду), Подтверждение родителей, Чего не хватает для автоматического решения у турникета, 10.2 Чего нет для автоматического выпуска, 10.3 Предлагаемая доменная функция (новый код, не реализовано), 10. Student Release Business Logic

### Community 44 - "План безопасного физического пилота (employeeNo `3818077855`)"
Cohesion: 0.18
Nodes (11): 0. Главный вывод для пилота, 1. Ответы на вопросы пилота, 2. Этапы, 3. Этап 1 — read-only диагностика 🔒, 4. Этап 2 — подготовка стенда 🔒, 5. Этап 3 — изменение настроек стенда 🔒 (выполняет инженер СКУД вручную), 6. Сценарии на стенде (последовательность DENY → ALLOW → DENY), 7. Критерии немедленной остановки (+3 more)

### Community 45 - "Покрытие исходных документов"
Cohesion: 0.18
Nodes (10): 1. Важно: имена файлов не совпадают с содержимым, 2. Метод конвертации, 3. Соответствие FRT → фрагменты, 4. Проверка полноты (не просто «конвертер отработал»), 5. Что не извлечено / требует проверки по PDF, 6. Данные, требующие осторожности, Excel: каждая непустая ячейка ищется в Markdown дословно, PDF: доля уникальных слов (≥4 символа) исходной страницы, найденных в Markdown той же страницы (+2 more)

### Community 46 - "Стратегия доступа учеников: «опознаёт Hikvision, выпускает kpp-journal»"
Cohesion: 0.18
Nodes (11): 1. Цель, 2. Что дают механизмы Hikvision, 3. Варианты, 4. Вход и выход, 5. Что уже готово в коде для учеников, 6. Порядок перехода, Вариант 1 (рекомендован): отдельные терминалы на выход + политика по категориям в kpp-journal, Вариант 2: ученики как `visitor` + `remoteCheckUserTypeList=["visitor"]` (+3 more)

### Community 48 - "Двери, турникеты, реле, расписания"
Cohesion: 0.22
Nodes (8): 1. Модель, 2. Параметры двери [FRT §14.6.4, с.434–437], 3. Статус [FRT §14.6.3.4–14.6.3.5, с.428–431], 5. Расписания, 6. Глобальные параметры контроллера `AcsCfg` [FRT §14.6.3.1–14.6.3.3, с.423–428], 7. Anti-passback, мультиаутентификация, 8. Пожарная безопасность, Двери, турникеты, реле, расписания

### Community 49 - "now"
Cohesion: 0.25
Nodes (6): now(), set_enabled(), admin_user(), mock(), setup(), test_permission_only_for_pilot_employee()

### Community 50 - "parse_time"
Cohesion: 0.36
Nodes (4): parse_time(), test_format(), test_not_recognized(), test_recognized()

### Community 51 - "ISAPI API Reference — что нужно kpp-journal"
Cohesion: 0.25
Nodes (8): 1. Общие правила, 2. Система и возможности, 3. Удалённая проверка и настройки контроллера, 4. События, 5. Персоны и учётные данные, 6. Двери, 7. Чего в наборе нет, ISAPI API Reference — что нужно kpp-journal

### Community 52 - "Аутентификация, подключение, таймауты"
Cohesion: 0.25
Nodes (7): 1. HTTP Digest Authentication, 2. Формат сообщений, 3. Блокировка после неудачных входов, 4. Таймауты и соединения, 5. Аутентификация устройства перед нашим сервером (Listening), 6. Хранение учётных данных, Аутентификация, подключение, таймауты

### Community 53 - "События: распознавание лиц, доступ, проход"
Cohesion: 0.25
Nodes (7): 1. Способы получения событий [FRT §4.3, с.18–25; §5.1, с.25–29], 2. `AccessControllerEvent` — ключевые поля [FRT §14.6.1.20, с.408–411], 3. Типы событий, важные для КПП [ACET], 4. Запрос до прохода vs. события после, 5. Направление прохода, 6. Дедупликация и потери, События: распознавание лиц, доступ, проход

### Community 54 - "Пользователи, employeeNo, лица, карты, права"
Cohesion: 0.25
Nodes (7): 1. employeeNo, 2. Персоны (UserInfo) [FRT §10.15, с.117–125], 3. Лица [FRT §10.10, с.89–97; API §14.4, с.361–379], 4. Карты [FRT §10.6, с.73–82], 5. Права доступа и расписания [FRT §10.18, с.137–142], Пользователи, employeeNo, лица, карты, права, Почему не управлять разрешениями на выход через права терминала

### Community 55 - "Reports.tsx"
Cohesion: 0.50
Nodes (7): useMe(), formatDate(), ReportsTab(), AuditEntry, AuditView(), Reports(), ReportView()

### Community 56 - "HTA Student Release — Graphify Dependency Analysis"
Cohesion: 0.25
Nodes (7): 11. Циклические зависимости, 12. Команды и запросы Graphify, 13. Готовность к следующей сессии, 1. Статус подключения Graphify, 2. Способ индексации, 4. Карта основных модулей, HTA Student Release — Graphify Dependency Analysis

### Community 58 - "Ошибки ISAPI"
Cohesion: 0.29
Nodes (6): 1. Структура ответа об ошибке, 2. Классы `statusCode` [FRT с.518; EC], 3. Коды, важные для нашей интеграции [EC], 4. HTTP-уровень, 5. Особенности словаря, Ошибки ISAPI

### Community 59 - "База знаний Hikvision ISAPI для kpp-journal"
Cohesion: 0.29
Nodes (7): База знаний Hikvision ISAPI для kpp-journal, Журнал решений, Краткие выводы, Обозначения источников, План безопасного пилота (одна учётная запись `3818077855`), Правила, Содержание

### Community 61 - "Проверка возможностей конкретного терминала"
Cohesion: 0.33
Nodes (5): 1. Известное об оборудовании, 2. Read-only чек-лист (выполнять только после разрешения), 3. Решающая матрица по результатам, 4. Тестовый стенд (обязателен перед любым W), Проверка возможностей конкретного терминала

### Community 62 - "p001-025.md"
Cohesion: 0.40
Nodes (4): - *- coding: utf-8 -*-, Output response content, Send the request and receive response, Set the authentication information

## Knowledge Gaps
- **4 isolated node(s):** `kpp-journal`, `@types/react`, `@types/react-dom`, `typescript`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 442 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `api()` connect `Admin.tsx` to `App.tsx`, `Backend Test Fixtures & Auth`, `MVP: внешняя авторизация выхода через Hikvision — реализация`, `План безопасного физического пилота (employeeNo `3818077855`)`, `set_permission`, `Reports.tsx`, `Pilot.tsx`, `Kpp.tsx`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Are the 65 inferred relationships involving `User` (e.g. with `_apply_user()` and `create_student()`) actually correct?**
  _`User` has 65 INFERRED edges - model-reasoned connections that need verification._
- **What connects `kpp-journal`, `@types/react`, `@types/react-dom` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Students, Import & Admin API` be split into smaller, more focused modules?**
  _Cohesion score 0.07826694619147449 - nodes in this community are weakly interconnected._
- **Why does `3. Статистика графа` connect `set_permission` to `HTA Student Release — Graphify Dependency Analysis`, `Students, Import & Admin API`, `9. Анализ влияния предлагаемых изменений`, `Admin.tsx`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `5. Цепочки вызовов ключевых функций (по графу)` (e.g. with `create_student()` and `create_user()`) actually correct?**
  _`5. Цепочки вызовов ключевых функций (по графу)` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Should `Backend Test Fixtures & Auth` be split into smaller, more focused modules?**
  _Cohesion score 0.052464947987336044 - nodes in this community are weakly interconnected._