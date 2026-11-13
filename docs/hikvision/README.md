# База знаний Hikvision ISAPI для kpp-journal

Постоянная техническая база для интеграции терминалов распознавания лиц Hikvision с kpp-journal.
Создана 2026-11-11 из документации в `ISAPI/` (конвертация MarkItDown MCP). **Сначала прочитайте этот файл.**

## Правила
1. **Документация ≠ оборудование.** Каждое утверждение помечено источником; «HW» — только то, что реально получено с нашего терминала.
   В документах: **DOC** — описано, **HW** — подтверждено на оборудовании, **?** — неизвестно.
2. **Не изменять реальные устройства** без явного разрешения: никаких `PUT/POST/DELETE` конфигурации, пользователей, `httpHosts`,
   команд `RemoteControl/door`, включения удалённой проверки. Даже read-only запросы — только после разрешения.
3. Перед использованием endpoint’а — сверить с первоисточником (страница в `raw/`), а затем с `capabilities` устройства.
4. Новые решения и результаты проверок на оборудовании — записывать сюда (раздел «Журнал решений» ниже или новый файл).

## Содержание

| Файл | Что внутри |
|---|---|
| [VISITOR_REMOTE_VERIFICATION_PLAN.md](VISITOR_REMOTE_VERIFICATION_PLAN.md) | **Текущий пилот:** normal — локально, visitor — через kpp-journal; ответы на вопросы, изменяемые параметры, перечень read-only запросов |
| [VISITOR_PILOT_TESTS.md](VISITOR_PILOT_TESTS.md) | Автотесты A–K, проверки на оборудовании, физическая процедура, команда normal → visitor |
| [VISITOR_ROLLBACK.md](VISITOR_ROLLBACK.md) | Откат записи и настроек терминала |
| [MVP_IMPLEMENTATION.md](MVP_IMPLEMENTATION.md) | **Код MVP:** адаптер, Decision Engine, режимы, таблицы, запуск, проверка DENY/ALLOW в симуляции |
| [PILOT_TEST_PLAN.md](PILOT_TEST_PLAN.md) | Физический пилот на стенде: условия, параметры, сценарии DENY→ALLOW→DENY, откат, что требует разрешения |
| [STUDENT_ACCESS_STRATEGY.md](STUDENT_ACCESS_STRATEGY.md) | Будущая политика для учеников: `belongGroup`, `userType`, варианты |
| [REMOTE_VERIFICATION.md](REMOTE_VERIFICATION.md) | **Главное.** Механизмы удалённой проверки §10.16, параметры, выбор механизма, изоляция пилота, тест-план |
| [INTEGRATION_ARCHITECTURE.md](INTEGRATION_ARCHITECTURE.md) | Анализ backend kpp-journal, что есть/нет (подтверждение родителей — нет), архитектура Hikvision Adapter |
| [DEVICE_CAPABILITIES.md](DEVICE_CAPABILITIES.md) | Что известно о нашем терминале, read-only чек-лист, решающая матрица, стенд |
| [API_REFERENCE.md](API_REFERENCE.md) | Отобранные endpoint’ы с классом риска R/R\*/W/X |
| [API_ENDPOINT_INDEX.md](API_ENDPOINT_INDEX.md) | Все 263 endpoint’а гл. 14 FRT: метод, путь, раздел, страница (автоиндекс) |
| [AUTHENTICATION.md](AUTHENTICATION.md) | Digest, 401, блокировка входа, таймауты, keep-alive |
| [USER_MANAGEMENT.md](USER_MANAGEMENT.md) | employeeNo, UserInfo, лица, карты, права и расписания |
| [ACCESS_CONTROL.md](ACCESS_CONTROL.md) | Двери, турникет, реле, статус, `AcsCfg`, расписания, пожарная безопасность |
| [EVENTS.md](EVENTS.md) | Получение событий, `AccessControllerEvent`, коды событий, запрос vs факт, направление, дедупликация |
| [ERROR_CODES.md](ERROR_CODES.md) | Структура ошибок, классы statusCode, ключевые коды, обработка |
| [SOURCE_COVERAGE.md](SOURCE_COVERAGE.md) | Какие файлы/страницы обработаны, проверка полноты, пробелы |
| `raw/` | Markdown-конвертация исходников; `manifest.json` (хэши, фрагменты), `verification.json` (покрытие по страницам) |

## Обозначения источников

⚠ Имена файлов в `ISAPI/` **не совпадают** с содержимым (см. `SOURCE_COVERAGE.md` §1).

| Код | Реальное содержимое | Файл в `ISAPI/` | Markdown |
|---|---|---|---|
| **FRT** | ISAPI Developer Guide — Face Recognition Terminals (Value Series), 565 стр. | `Log (1).pdf` | `raw/05_isapi_frt_value_series/pNNN-MMM.md` |
| **ACET** | Access Control Event Types + Event Linkage Types, 31 стр. | `Country and Region Code (1).pdf` | `raw/01_access_control_event_types.md` |
| **EC** | ErrorCode (словарь ошибок), xlsx | `Field Dictionary (1).xlsx` | `raw/03_error_code.md` |
| **FD** | Field Dictionary, xlsx | `ISAPI_Face Recognition Terminals_Value Series (1).pdf` | `raw/04_field_dictionary.md` |
| **LOG** | B.1 Log Types for ISAPI, 27 стр. | `Region Code (1).pdf` | `raw/06_log_types.md` |
| **CRC** | Country/Region Code (номера авто), 10 стр. | `ErrorCode (1).xlsx` | `raw/02_country_region_code.md` |

Ссылка `[FRT §10.16.2.1, с.125]` = раздел и **физическая страница PDF** (1-based). В `raw/` страница помечена `<!-- page: 125 -->`.
Быстрый поиск: `grep -n "remoteCheck" docs/hikvision/raw/05_isapi_frt_value_series/*.md`.

## Краткие выводы

1. **Механизм:** удалённая проверка (Remote Verification, FRT §10.16) реализует нужную схему «решение до открытия».
   Рекомендовано **Synchronous Listening** (`checkChannelType=ISAPIListen`, `remoteCheckWithISAPIListen=sync`) с `needDeviceCheck=true`,
   `remoteCheckVerifyMode=2` (лицо), `offlineDevCheckOpenDoorEnabled=false`. Запасные — Async Listening, Arming. Platform Only не подходит.
2. **Изоляция пилота:** настройки удалённой проверки **глобальны для терминала**. Фильтр по одному `employeeNo` не описан.
   `remoteCheckUserTypeList` (по типу персоны) есть только в примерах, не в API Reference → на действующем терминале не полагаться.
   Нужен **отдельный тестовый стенд** той же модели и прошивки.
3. **kpp-journal:** подтверждение родителей **не реализовано**; разрешение даёт эдвайзер на день; выход отмечает охранник; связи с `employeeNo` нет.
4. **Пробелы документации:** нет схем `AccessControl/capabilities`, `UserInfo/*`, `CardInfo/*`, `deviceInfo`; схемы потоков — картинки.

## План безопасного пилота (одна учётная запись `3818077855`)

| Этап | Что | Сеть к школьным терминалам | Разрешение |
|---|---|---|---|
| 0 | База знаний (готово) | нет | — |
| 1 | Read-only опрос действующего терминала по `DEVICE_CAPABILITIES.md` §2; только GET + поиск `AcsEvent`/`UserInfo` по `3818077855` | GET/R\* | **требуется** |
| 2 | Доменная логика в kpp-journal: `employee_no`, подтверждение родителей, `release.decide()`, тесты — без устройства | нет | — |
| 3 | Gateway и парсер на синтетических запросах (образцы FRT с.130, 133) | нет | — |
| 4 | Стенд DS-K1T341CM V3.3.40, только тестовый пользователь; сценарии `REMOTE_VERIFICATION.md` §6, включая проверку `remoteCheckUserTypeList` | стенд | требуется (устройство) |
| 5 | Пилот на действующем проходе — **только** если стенд подтвердил изоляцию по `userType` (или выделен отдельный терминал/полоса); снимок `AcsCfg`/`httpHosts` «до», план отката, вне учебного времени, охранник рядом | W | **требуется письменно** |

Критерии остановки: любой отказ прохода не-тестовому человеку; задержка > 2 с; сбой heartbeat/доступности gateway → немедленный откат к снимку.

## Журнал решений

| Дата | Решение | Основание |
|---|---|---|
| 2026-11-11 | Основной кандидат — Remote Verification, Sync Listening, `needDeviceCheck=true` | FRT §10.16; `REMOTE_VERIFICATION.md` §4 |
| 2026-11-11 | Пилот на действующем терминале без стенда **не проводить** — изоляция по `employeeNo` не поддержана документацией | `REMOTE_VERIFICATION.md` §5 |
| 2026-11-11 | `RemoteControl/door` не использовать для выпуска | `ACCESS_CONTROL.md` §4 |
| 2026-11-11 | Адаптер — отдельный процесс, доменная функция `release.decide()` без зависимостей от Hikvision | `INTEGRATION_ARCHITECTURE.md` §2 |
| 2026-11-13 | MVP реализован: приёмник `app.hikvision_gateway`, `services/release.decide_exit`, режимы SIMULATION/READ_ONLY/PILOT (по умолчанию SIMULATION), выключатель пилота по умолчанию выключен | `MVP_IMPLEMENTATION.md` |
| 2026-11-13 | Адаптер не умеет менять конфигурацию терминала и пользователей (белый список: GET, поиск AcsEvent, PUT remoteCheck только в PILOT); настройку стенда делает инженер вручную | `MVP_IMPLEMENTATION.md` §3 |
| 2026-11-13 | В ответе отдаём `serialNo` события (API Ref с.520–521), а не значение из примера с.133 | `MVP_IMPLEMENTATION.md` §10 |
| 2026-11-13 | Повтор события — всегда `failed`; одноразовое разрешение расходуется атомарно при ALLOW; проход фиксируется отдельно и только для ALLOW, по которому `success` реально ушёл | `MVP_IMPLEMENTATION.md` §4–5 |
| 2026-11-13 | **Утверждена архитектура пилота: normal — локально, visitor — Remote Verification через kpp-journal** (заказчик) | `VISITOR_REMOTE_VERIFICATION_PLAN.md` |
| 2026-11-13 | Смена userType — только `PUT UserInfo/Modify {employeeNo, userType}` одной записи пилота, отдельный флаг `HIKVISION_USER_WRITE_*`, DRY_RUN по умолчанию, сверка до/после; схемы тела Modify в нашем наборе нет | `VISITOR_REMOTE_VERIFICATION_PLAN.md` §3, §6 |
| 2026-11-13 | `remoteCheckVerifyMode=6` вместо 2: при 2 карта visitor проходит локально в обход kpp-journal | FRT с.127; `VISITOR_REMOTE_VERIFICATION_PLAN.md` §4 |
| 2026-11-13 | Запрос удалённой проверки от не-visitor → DENY `not_remote_check_type` и тревога изоляции (kpp-journal не авторизует normal) | `release._evaluate` |
| 2026-11-13 | На общем терминале Remote Verification не включать, пока стенд не подтвердил И-1…И-4: `remoteCheckUserTypeList` есть только в примерах | `VISITOR_REMOTE_VERIFICATION_PLAN.md` §2 |
| 2026-11-13 | `belongGroup` относится к Multi-Factor Authentication (§10.13, с.116), не к удалённой проверке; для учеников рекомендованы отдельные терминалы выхода + политика категорий в kpp-journal | `STUDENT_ACCESS_STRATEGY.md` |
