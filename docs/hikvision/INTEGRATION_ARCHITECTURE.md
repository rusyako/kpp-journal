# Hikvision Adapter для kpp-journal — анализ и предлагаемая архитектура

Статус: **предложение**, код не писался. Основано на исходниках репозитория на ветке `test_connection_of_turnstiles` (коммит `2077ee7`)
и на `REMOTE_VERIFICATION.md`. Дополняет `HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md` (§11, §16–17), не заменяет его.

## 1. Как работает система сейчас (проверено по коду)

| Что | Где | Факт |
|---|---|---|
| Разрешение на выход | `backend/app/models.py:133` `Permission` | **Эдвайзер** (не родитель) ставит разрешение на **один день**: `date`, `student_id`, `allowed_time` («разрешено с»), `raw_time`, `reason`, `created_by`, мягкое удаление `deleted_at`. UNIQUE(`date`,`student_id`) |
| Создание/отмена | `backend/app/services/advisor.py:70` `set_permission` | только сегодня; права — `can_edit` (админ или эдвайзер своей эдвайзери); пустые время и причина = отмена; аудит `permission_set/permission_clear` |
| Отметка выхода | `backend/app/services/exits.py:48` `mark_exit` | **охранник вручную**; время ставит сервер (`clock.now_minute()`), офлайн-очередь — `client_time`; выход **не блокируется** при отсутствии разрешения — только статус `no_permission` |
| Один выход в день | `models.py:160` индекс `uq_exits_active` | одна неотменённая отметка на ученика в день; повторный выход/возврат не моделируется |
| Статус | `backend/app/services/day.py:42` `DayRow.status` | `none` / `allowed` / `ok` / `early` (вышел раньше `allowed_time`) / `no_permission` |
| API | `backend/app/api/kpp.py` | `GET /api/day`, `POST /api/exits` (роль GUARD), `POST /api/exits/{id}/cancel`, `GET /api/audit` |
| Авторизация API | `backend/app/deps.py` | cookie-сессия или Telegram initData; роли ADMIN/GUARD/ADVISOR/VIEWER; **нет машинной (device) авторизации** |
| Ученик | `models.py:68` `Student` | `full_name` + `class_name`; **нет поля для `employeeNo`** |
| Миграции | `backend/alembic/versions/0001_initial_schema.py` | одна начальная миграция |
| Тесты | `backend/tests/` | 30 тест-функций: роли, выход без разрешения, отмена, ранний выход, офлайн-очередь, отчёт, Telegram, импорт, поиск, разбор времени. Тестов на устройство нет. Локально **не запускались**: pytest не установлен |
| Hikvision | — | в коде приложения **нет**; есть только внешний скрипт `export_hikvision_users.py` (read-only выгрузка) |

### Подтверждение родителей
**Не реализовано.** В моделях нет сущности родителя/законного представителя, нет связи родитель↔ученик, нет статуса подтверждения.
Единственный источник разрешения — эдвайзер. `grep -i "parent|родител"` по `backend/app` находит только `Path.parents`.

### Чего не хватает для автоматического решения у турникета
1. Связь `Student` ↔ `employeeNo` терминала.
2. Модель подтверждения родителем (кто, когда, канал, срок действия, отзыв).
3. Детерминированная функция решения «можно ли выпустить сейчас» с причиной отказа.
4. Машинный вход для устройства (не cookie охранника).
5. Хранение событий устройства с дедупликацией; связь `Exit` ↔ событие; источник отметки (охрана/турникет).
6. Решение по семантике `allowed_time` («с»), окну действия («до»), однократности.

## 2. Целевая архитектура

```
 ┌──────────────── терминал (выход) ────────────────┐
 │ лицо → локальная проверка → employeeNo            │
 │ AcsCfg: remoteCheckDoorEnabled, ISAPIListen, sync │
 └───────────────┬──────────────────────────────────┘
                 │ POST multipart (AccessControllerEvent remoteCheck=true)
                 ▼
 ┌─────────── hikvision-gateway (новый процесс) ──────────────┐
 │ FastAPI-приложение на LAN-порту, только allowlist IP        │
 │  parse → идемпотентная запись device_event                  │
 │  → release.decide(employee_no, now)  (таймаут-бюджет ~1 c)  │
 │  → ответ {"RemoteCheck":{"serialNo":N,"checkResult":…}}     │
 │  ошибка/исключение/истёк бюджет → "failed" (fail-closed)    │
 │  события прохода (0xda) → exits (source=turnstile)          │
 └───────┬────────────────────────────────────────┬───────────┘
         │ SQLAlchemy (та же БД)                  │ ISAPI read-only клиент (httpx Digest)
         ▼                                        ▼
   PostgreSQL kpp                         сверка AcsEvent, health
```

### Компоненты

| Модуль | Ответственность |
|---|---|
| `backend/app/integrations/hikvision/client.py` | ISAPI-клиент на `httpx` с `DigestAuth`; **allowlist методов/путей** (по умолчанию только R/R\*), запрет `RemoteControl`, `AcsCfg PUT`, `UserInfo*` записи, пока не включён явный флаг; стоп после второго 401 |
| `…/hikvision/parsing.py` | разбор `multipart/form-data` и `multipart/mixed`, JSON/XML по `Content-Type`; выбрасывать картинки (не сохранять фото детей) |
| `…/hikvision/gateway.py` | HTTP-приёмник (отдельный FastAPI app): `POST /hikvision/<device_key>/events` |
| `backend/app/services/release.py` | **чистая доменная функция** `decide(db, student, now) -> Decision(allow, reason, permission_id)` — без зависимостей от Hikvision; тестируется юнит-тестами |
| `backend/app/hikvision_worker.py` | отдельный процесс (как `bot` в `deploy/docker-compose.yml`): gateway + периодическая сверка журнала `AcsEvent` |

Процесс отдельный, потому что API-процесс один и держит планировщик/WebSocket (аудит §11.1 п.3); сбой адаптера не должен ронять журнал.

### Решение `decide()` — черновик правил (требует утверждения школой)
Разрешить, только если **все** условия истинны:
1. `employeeNo` сопоставлен активному ученику;
2. сегодня рабочий день (`services/calendar.is_working_day`);
3. есть неудалённое `Permission` на сегодня с распознанным `allowed_time`, и `now >= allowed_time`;
4. есть действующее подтверждение родителя для этого разрешения (новая сущность);
5. у ученика нет неотменённого `Exit` за сегодня (существующее ограничение — один выход в день);
6. (опц.) `now <= valid_until`, если введём окно.

Иначе — `failed` с кодом причины (`unknown_person`, `no_permission`, `too_early`, `no_parent_approval`, `already_exited`, `internal_error`).
Учителя/сотрудники в пилоте не затрагиваются (изоляция — `REMOTE_VERIFICATION.md` §5).

## 3. Изменения схемы (миграция `0002`, не создавалась)

| Таблица / поле | Назначение |
|---|---|
| `devices` (`id`, `name`, `ip`, `direction`='exit', `serial`, `active`) | терминалы; направление задаётся конфигурацией |
| `student_device_ids` (`student_id`, `employee_no` UNIQUE) | сопоставление с терминалом (не ФИО) |
| `parent_approvals` (`permission_id`, `approved_at`, `channel`, `approved_by` ref, `revoked_at`) | подтверждение родителя — модель родителя/канала (Telegram?) решить отдельно |
| `device_events` (`device_id`, `serial_no`, `event_time`, `major`, `minor`, `employee_no`, `remote_check`, `payload` JSON без фото; UNIQUE(`device_id`,`serial_no`,`event_time`)) | идемпотентный журнал событий |
| `release_decisions` (`device_event_id`, `student_id`, `permission_id`, `allow`, `reason`, `latency_ms`, `responded_at`) | аудит каждого решения |
| `exits.source` (`guard`/`turnstile`), `exits.device_event_id` UNIQUE, `exits.pass_confirmed` | связь факта прохода с событием; `guard_id` уже nullable |

## 4. Надёжность и безопасность

* **Fail-closed:** любое исключение, отсутствие сопоставления, недоступная БД, превышение бюджета времени → `failed`. Бюджет ответа < `remoteCheckTimeout` устройства.
* **Идемпотентность:** повторный POST того же события (тот же `serialNo`+время) возвращает **то же** решение из `release_decisions`.
* **Не путать запрос и факт:** `remoteCheck=true` → решение; `0xda`/`remoteCheckResult` → журнал (`EVENTS.md` §4).
* **Без фото:** картинки из multipart не сохраняются и не логируются.
* **Секреты:** логин/пароль терминала — в `deploy/.env`; в логах маскировать заголовок `Authorization`.
* **Сеть:** gateway слушает только LAN/VLAN терминалов, allowlist IP; наружу через Caddy не публикуется.
* **Эвакуация:** адаптер никогда не шлёт `RemoteControl/door` и не меняет `fireAlarmInputType`.
* **Наблюдаемость:** метрики задержки решения, доля отказов по причинам, алерт при отсутствии heartbeat/событий.

## 5. Тесты (план)
* Юнит: `decide()` — таблица случаев (нет разрешения, рано, нет подтверждения родителя, уже вышел, неизвестный employeeNo, выходной).
* Контракт: парсер на образцах из FRT с.130/133 (multipart с JSON + бинарная часть).
* Интеграционные: gateway отвечает `failed` при исключении/таймауте; идемпотентность повторного POST.
* Стенд: сценарии `REMOTE_VERIFICATION.md` §6.

## 6. Порядок работ
1. (готово) база знаний `docs/hikvision/`.
2. Read-only проверка терминала по `DEVICE_CAPABILITIES.md` §2 — **после разрешения**.
3. Доменная часть без оборудования: `student_device_ids`, `parent_approvals`, `release.decide()` + тесты.
4. Gateway + парсер + журнал событий; прогон на записанных/синтетических запросах.
5. Стенд: включение удалённой проверки на тестовом терминале.
6. Пилот на действующем проходе — только если стенд подтвердил изоляцию и есть письменное разрешение.
