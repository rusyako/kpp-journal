# MVP: внешняя авторизация выхода через Hikvision — реализация

Дата: 2026-11-13. Ветка `test_connection_of_turnstiles`. Источники — см. [README.md](README.md#обозначения-источников).

> **Обновление 2026-11-13 (пилот visitor):** normal — локально, visitor — через kpp-journal. Добавлены инструменты
> `user_type` (смена userType одной записи, DRY_RUN по умолчанию) и `remote_check_plan` (только чтение), проверка
> `userType` в Decision Engine, миграция `0003`, 26 тестов. Подробно — [VISITOR_REMOTE_VERIFICATION_PLAN.md](VISITOR_REMOTE_VERIFICATION_PLAN.md).
> Итог тестов теперь 160 passed. Белый список клиента дополнен двумя узкими операциями (§3 ниже устарел в этой части):
> `POST UserInfo/Search` одной записи пилота и `PUT UserInfo/Modify {employeeNo, userType}` при `HIKVISION_USER_WRITE_*`.
>
> **Статус: программный MVP готов и проверен автотестами на виртуальном терминале.
> К управлению реальным турникетом НЕ готов:** предварительная внешняя авторизация и изоляция пилота на нашем
> оборудовании не подтверждены (VERIFIED ON DEVICE — пусто). Порядок проверки — [PILOT_TEST_PLAN.md](PILOT_TEST_PLAN.md).

Обозначения статуса: **IMPLEMENTED** — есть в коде · **TESTED** — проверено автотестами · **DOCUMENTED** — описано
документацией Hikvision · **VERIFIED ON DEVICE** — подтверждено на оборудовании · **NOT VERIFIED** — требует проверки.

## 1. Принцип

Hikvision — **идентификация** (лицо → `employeeNo`). kpp-journal — **авторизация** (можно ли выйти сейчас).

```
лицо → терминал: локальная проверка → POST AccessControllerEvent{remoteCheck:true, serialNo:N}   (дверь закрыта, ждёт)
     → hikvision-gateway → hik_events (идемпотентно, без фото и ФИО)
     → Decision Engine decide_exit() → release_decisions (ALLOW/DENY + причина)
     → ответ {"RemoteCheck":{"serialNo":N,"checkResult":"success|failed"}} → hik_commands
     → терминал открывает ТОЛЬКО при success с тем же serialNo
     → событие прохода 0xda/0x89 (или ручное подтверждение) → hik_passages (→ exits для учеников)
```

Механизм — Remote Verification, Synchronous Listening [FRT §10.16.4, с.130–133] (DOCUMENTED). Запасной — Async Listening
(PUT `/ISAPI/AccessControl/remoteCheck` [FRT §14.6.15.2, с.520–521]) — тоже реализован. «Открыть дверь командой после
обычного события доступа» (`RemoteControl/door`) **не используется и заблокировано в клиенте**.

## 2. Что сделано

| Компонент | Файл | IMPLEMENTED | TESTED |
|---|---|---|---|
| Режимы SIMULATION / READ_ONLY / PILOT, проверка «можно ли управлять» | `backend/app/integrations/hikvision/settings.py` | ✅ | ✅ |
| Разбор запросов терминала: multipart (CRLF/LF), JSON, XML; `employeeNoString` > `employeeNo`; фото и ФИО отбрасываются | `…/hikvision/parsing.py` | ✅ | ✅ (в т.ч. дословный пример FRT с.133) |
| ISAPI-клиент: HTTP Digest, белый список операций, остановка после 401, таймауты | `…/hikvision/client.py` | ✅ | ✅ (на mock) |
| Mock-терминал: Digest, события, интерпретация ответа (fail-closed), GET-ответы, PUT remoteCheck | `…/hikvision/mock_device.py` | ✅ | ✅ |
| Адаптер: событие → решение → ответ; повторы; таймаут-бюджет; async PUT | `…/hikvision/adapter.py` | ✅ | ✅ |
| Отдельный процесс-приёмник `POST /hikvision/listen/{device_key}` | `backend/app/hikvision_gateway.py` | ✅ | ✅ |
| Decision Engine `decide_exit()`, проход, ручное подтверждение | `backend/app/services/release.py` | ✅ | ✅ |
| Тестовые разрешения PILOT, симуляция, данные экрана | `backend/app/services/pilot.py` | ✅ | ✅ |
| API администратора `/api/pilot/*` | `backend/app/api/pilot.py` | ✅ | ✅ |
| Экран «Пилот Hikvision» (`/pilot`, только admin) | `frontend/src/pages/Pilot.tsx` | ✅ | сборка + типы ✅; в браузере не проверялся (см. §9) |
| Read-only диагностика терминала (CLI) | `…/hikvision/diagnostics.py` | ✅ | ✅ (на mock) |
| Таблицы + миграция `0002` | `backend/app/models.py`, `backend/alembic/versions/0002_hikvision_pilot.py` | ✅ | upgrade/downgrade/upgrade + `alembic check` на SQLite ✅; PostgreSQL — NOT VERIFIED |
| CLI: `pilot-setup`, `pilot-device` | `backend/app/cli.py` | ✅ | вручную ✅ |
| Docker: сервис `hikvision-gateway` (profile `hikvision`, не стартует по умолчанию) | `deploy/docker-compose.yml` | ✅ | NOT VERIFIED |

## 3. Режимы и защита от управления

| Режим | Реальные терминалы по сети | Ответ `success` реальному терминалу | Виртуальные терминалы |
|---|---|---|---|
| `SIMULATION` (по умолчанию; опечатка в значении → тоже SIMULATION) | нет | никогда | да, `success` при ALLOW |
| `READ_ONLY` | только GET и поиск `AcsEvent` | никогда (решение «теневое», `status=blocked`) | нет |
| `PILOT` | GET, поиск, `PUT remoteCheck` | только если `HIKVISION_CONTROL_ENABLED=1` **и** ключ терминала в `HIKVISION_CONTROL_DEVICES` | нет |

Режим задаётся **только переменными окружения** — из браузера его не переключить.
Наличие этих настроек — не разрешение школы на изменение оборудования.

Белый список клиента (`client.check_operation`): GET; POST только `/ISAPI/AccessControl/AcsEvent`; PUT только
`/ISAPI/AccessControl/remoteCheck` при `control_allowed`. Явно запрещены для любых изменяющих методов: `RemoteControl`,
`AcsCfg`, `httpHosts`, `UserInfo/*`, `UserInfoDetail`, `FDLib` (запись), `CardInfo`, `UserRight*`, `Door/param`,
`DoorStatusWeekPlanCfg`, reboot/factoryReset/firmware, `Security/users`. **Адаптер не умеет менять конфигурацию терминала и
пользователей** — эти шаги пилота выполняет инженер вручную по [PILOT_TEST_PLAN.md](PILOT_TEST_PLAN.md).

Дополнительно: выключатель пилота в БД (`hik_pilot_state.enabled`, по умолчанию **выключен** → все запросы DENY);
доверие к источнику — реальный терминал принимается только с IP из `allowed_ips` (пусто = никому),
виртуальный — только изнутри приложения. Маршрутов «открыть дверь» нет ни в API, ни в приёмнике (есть тест).

## 4. Decision Engine — правила (`release.decide_exit`)

Первая неудачная проверка — причина отказа. Любое исключение — `DENY internal_error`.

| # | Проверка | Причина DENY |
|---|---|---|
| 1 | Повтор уже записанного события (тот же терминал + `serialNo` + `dateTime`) | `duplicate_event` |
| 2 | Терминал зарегистрирован / активен / источник доверенный | `unknown_device` / `device_inactive` / `untrusted_source` |
| 3 | Терминал на **выход** (направление — конфигурация, в событии его нет, EVENTS.md §5) | `wrong_direction` |
| 4 | Пилот включён | `pilot_disabled` |
| 5 | `majorEventType=5`, `subEventType` ∈ `HIKVISION_ALLOWED_MINORS` (по умолчанию 75 — Face Authentication Completed, ACET с.18) | `unsupported_event` |
| 6 | `currentEvent` ≠ false; время события читается и отличается от сервера ≤ `HIKVISION_MAX_EVENT_AGE_S` | `not_realtime` / `bad_event_time` / `stale_event` |
| 7 | Есть `employeeNo`; есть связь `hik_persons`; связь и профиль (ученик/пользователь) активны | `no_employee_no` / `unknown_person` / `person_inactive` / `profile_inactive` |
| 8 | Человек отмечен `pilot` **и** входит в `HIKVISION_PILOT_EMPLOYEE_NOS` | `not_in_pilot` |
| 9 | Есть действующее разрешение `source=pilot`: не отменено, не использовано (если одноразовое), `valid_from ≤ now < valid_until` | `no_permission` / `permission_revoked` / `permission_used` / `permission_not_started` / `permission_expired` |
| 10 | Решение готово до дедлайна | `decision_timeout` |

ALLOW расходует одноразовое разрешение **атомарно** (`UPDATE … WHERE used_at IS NULL AND revoked_at IS NULL`).
Повтор события всегда получает `failed`, даже при многоразовом разрешении.

## 5. Разделение «решение / команда / проход»

| Сущность | Таблица | Когда создаётся |
|---|---|---|
| Событие терминала | `hik_events` | каждый POST; уникальный `dedup_key`; у повтора `dedup_key=NULL`, `duplicate_of_id` |
| Решение | `release_decisions` | одно на событие-запрос (`event_id` UNIQUE) |
| Ответ/команда терминалу | `hik_commands` | `sent` / `simulated` / `blocked` / `error` / `timeout` |
| Факт прохода | `hik_passages` | по событию 0xda/0x89/0x86 **только** для ALLOW, по которому `success` реально ушёл; или вручную |
| Выход ученика | `exits` (существующая) | только при `passed` и если `hik_persons.student_id` задан; тестовая учётная запись в журнал КПП не попадает |

## 6. Данные

Новые таблицы (миграция `0002`, существующие таблицы не меняются): `hik_devices`, `hik_persons`
(`employee_no` — строка, UNIQUE), `release_permissions`, `hik_events`, `release_decisions`, `hik_commands`,
`hik_passages`, `hik_pilot_state`, `hik_config_snapshots`. Пароли терминалов в БД не хранятся
(`credentials_env` → переменные `HIK_<X>_USER/_PASSWORD`). Фото, шаблоны лиц, ФИО и номера карт из событий не сохраняются.

**Миграции на production.** `0002` проверена на SQLite (upgrade → `alembic check` без расхождений → downgrade → upgrade).
⚠ Текущий `Dockerfile` при старте `api` выполняет `alembic upgrade head` — развёртывание этой ветки **применит `0002`
автоматически**. Перед развёртыванием: резервная копия БД (`deploy/backup.sh`), прогон на копии PostgreSQL. Я ничего не развёртывал.

## 7. Запуск (Windows PowerShell)

```powershell
# Бэкенд: Python 3.12+ (проверено на 3.13)
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"

# Тесты (оборудование не нужно)
.\.venv\Scripts\python -m pytest -q

# Локальная БД и демо-данные
$env:DATABASE_URL = "sqlite:///./kpp.db"
$env:COOKIE_SECURE = "0"; $env:SCHEDULER_ENABLED = "0"
$env:HIKVISION_MODE = "SIMULATION"          # по умолчанию и так SIMULATION
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\python -m app.cli demo         # admin / demo-pass-123
.\.venv\Scripts\python -m app.cli pilot-setup  # sim-exit, sim-entry, запись 3818077855

# Фронтенд
cd ..\frontend; npm ci; npm run build; cd ..\backend
$env:STATIC_DIR = (Resolve-Path ..\frontend\dist).Path
.\.venv\Scripts\uvicorn app.main:app --port 8000
# → http://localhost:8000/pilot  (вход admin)

# Приёмник терминалов (нужен только для стенда; в симуляции не требуется)
.\.venv\Scripts\uvicorn app.hikvision_gateway:app --host 127.0.0.1 --port 8090

# Read-only диагностика на виртуальном терминале
.\.venv\Scripts\python -m app.integrations.hikvision.diagnostics --mock
```

## 8. Как проверить DENY и ALLOW в симуляции

На `/pilot`:
1. «Подготовить пилот» → «Включить пилот».
2. «Лицо опознано» → 🔴 **DENY** «Нет разрешения» (сценарий A).
3. Создать разрешение «с» в будущем → «Лицо опознано» → DENY «ещё не начало действовать» (B).
4. Создать разрешение «с сейчас до +30 мин» → «Лицо опознано» → 🟢 **ALLOW**, «Турникет открылся (симуляция)» (C).
5. «Прошёл (Passing Event 0xda)» → в таблице решений «Проход: прошёл (событие)» (I).
6. «Повтор последнего события» → DENY «Повтор…» (F). Снова «Лицо опознано» → DENY «уже использовано».
7. Создать разрешение и «Отменить» → DENY «отменено» (D).
8. «kpp-journal недоступен» → 🔴 проход закрыт (E). employeeNo `0000000001` → DENY «не связан» (G).
   Терминал `unknown-terminal` → DENY «неизвестный терминал» (H). `sim-entry` → DENY «не на выход».

То же автоматически: `tests/test_pilot_api.py::test_full_simulation_deny_allow_deny`.

## 9. Тесты

`backend/tests/`: `test_hik_adapter.py` (разбор, клиент, белый список, Digest/401, таймаут сети, диагностика),
`test_release.py` (сценарии A–I, защитные случаи, режимы, async), `test_pilot_api.py` (API, приёмник, таймаут-бюджет,
отсутствие маршрутов открытия). Итог прогона 2026-11-13: **134 passed** (75 прежних + 59 новых), 3 прогона подряд без сбоев.
Фронтенд: `npm run build` (tsc + vite) ✅, `npm test` 19 passed.

Ручная проверка: запущен сервер на временной SQLite-БД, `alembic upgrade head`, `cli demo`, `cli pilot-setup`, HTTP-прогон
сценария DENY → ALLOW → проход → повтор → DENY. Найдена и исправлена ошибка симулятора (счётчик `serialNo` откатывался после
«повтора», новое лицо принималось за дубликат) — добавлен регрессионный тест. Экран в браузере не открывался
(расширение браузера было недоступно) — проверить визуально.

## 10. Соответствие документации и открытые вопросы

| Вопрос | DOCUMENTED | NOT VERIFIED на нашем терминале |
|---|---|---|
| Поддержка удалённой проверки | `isSupportRemoteCheck` в `GET /ISAPI/AccessControl/capabilities` [FRT с.125] | DS-K1T341CM V3.3.40 |
| Sync-ответ в теле HTTP | [FRT §10.16.4.1 шаг 4b, с.132] | формат, принятый прошивкой |
| `serialNo` ответа | «should be the same as that in the uploaded event message» [с.520–521] | ⚠ в примере с.133 ответ `serialNo: 1` на событие 1866 — расхождение документации; мы отвечаем serialNo события |
| Нет ответа → отказ | «if no result is received within this time, the verification fails» [с.126, 132]; `offlineDevCheckOpenDoorEnabled` по умолчанию `false` | поведение при обрыве сети, HTTP 500, битом JSON |
| Таймаут | `remoteCheckTimeout` 1–10 с [с.424, 428]; наш бюджет 1,5 с | фактическая задержка |
| `security`/`iv` в URL `remoteCheck` | есть в §10.16, нет в API Reference [с.520] | нужен ли на прошивке |
| Аутентификация терминала перед нами | `httpAuthenticationMethod` (Digest рекомендован) [с.129] | **не реализовано**: защищаемся allowlist IP + отдельной сетью |
| Событие с `remoteCheckResult` | прошивки 2024+ [с.126] | приходит ли; адаптер только журналирует |
| Passing Event 0xda от турникета | ACET с.22 | приходит ли от нашего турникета; иначе — ручное подтверждение |

## 11. Ограничения MVP

* Подтверждение родителей не реализовано; тестовое разрешение PILOT им **не является** (поле `source`).
* Для тестовой учётной записи календарь учебных дней не проверяется — окно задаётся явно (≤ 12 ч).
* Между фиксацией ALLOW и отправкой ответа есть узкое окно: если ответ опоздал за бюджет, терминал получит `failed`,
  а одноразовое разрешение может быть уже израсходовано (fail-closed, видно в журнале команд как `timeout`).
* `IDCardInfoEvent`/`QRCodeEvent` разбираются, но в пилоте отклоняются (`unsupported_event`).
