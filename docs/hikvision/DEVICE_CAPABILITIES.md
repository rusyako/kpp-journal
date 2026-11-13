# Проверка возможностей конкретного терминала

Цель: до любой разработки на «живом» API убедиться, что **наш** терминал поддерживает нужное. Документация описывает семейство устройств;
наличие поля в документации ≠ поддержка прошивкой.

## 1. Известное об оборудовании

| Факт | Статус | Источник |
|---|---|---|
| Модель DS-K1T341CM, прошивка V3.3.40, тип `accessControlTerminal` | со слов заказчика | аудит §11.4 |
| IP терминала, с которого выгружались пользователи: `192.168.4.49` | HW | `export_hikvision_users.py:20` |
| `UserInfo/Search` работает, 2216 персон, все `userType=normal`, `doorRight="1"` | HW | `hikvision_users.json` |
| Тестовая персона `3818077855` существует, 1 лицо, 1 карта, шаблон `1` | HW | там же |
| Поддержка remote verification, sync/async, `remoteCheckUserTypeList` | **?** | — |
| Занят ли слот `httpHosts`, есть ли HikCentral/другая платформа | **?** | — |
| Как подключён турникет (реле терминала / контроллер полосы), есть ли датчик прохода | **?** | аудит §11.4 |
| Отдельные терминалы на вход и выход | **?** | — |
| Синхронизация времени (NTP) | **?** | — |

## 2. Read-only чек-лист (выполнять только после разрешения)

Все запросы — `GET`, кроме помеченных R\* (поиск через `POST`, данные не меняет). Сохранять сырые ответы в
`docs/hikvision/device-snapshots/<device>-<дата>/` (без паролей; ФИО из ответов не коммитить).

| # | Запрос | Что смотрим | Зачем |
|---|---|---|---|
| 1 | `GET /ISAPI/System/deviceInfo` | `model`, `firmwareVersion`, `firmwareReleasedDate`, `serialNumber` | год прошивки → поддержка `remoteCheckResult` (2024+) |
| 2 | `GET /ISAPI/System/capabilities` | `isSupportSubscribeEvent` | arming с подпиской |
| 3 | `GET /ISAPI/AccessControl/capabilities` | `isSupportRemoteCheck`, `isSupportAcsCfg`, `isSupportUserInfo`, `EmployeeNoInfo`, `isSupportFDLib` | ключевой флаг |
| 4 | `GET /ISAPI/AccessControl/AcsCfg/capabilities?format=json` | `remoteCheckDoorEnabled`, `checkChannelType @opt` (есть ли `ISAPIListen`), `remoteCheckWithISAPIListen @opt` (есть ли `sync`), `remoteCheckVerifyMode @opt`, `needDeviceCheck`, `offlineDevCheckOpenDoorEnabled`, **`remoteCheckUserTypeList`** | выбор механизма; возможность изоляции |
| 5 | `GET /ISAPI/AccessControl/AcsCfg?format=json` | текущие значения; включено ли уже `remoteCheckDoorEnabled` | снимок «до» |
| 6 | `GET /ISAPI/AccessControl/remoteCheck/capabilities?format=json` | `serialNo`, `checkResult`, `info` | — |
| 7 | `GET /ISAPI/Event/notification/httpHosts/capabilities` | число хостов | занят ли единственный слот |
| 8 | `GET /ISAPI/Event/notification/httpHosts` | настроенные хосты (URL, IP) | кто ещё получает события |
| 9 | `GET /ISAPI/Event/notification/subscribeEventCap` | типы событий | — |
| 10 | `GET /ISAPI/AccessControl/AcsEvent/capabilities?format=json` | `maxResults`, условия поиска | — |
| 11 | R\* `POST /ISAPI/AccessControl/AcsEvent?format=json` с `employeeNoString:"3818077855"`, `picEnable:false`, за 1 день | какие major/minor приходят при проходе тестового пользователя; есть ли `0xda` | события турникета |
| 12 | `GET /ISAPI/AccessControl/AcsWorkStatus?format=json` | `doorStatus`, `doorLockStatus` | — |
| 13 | `GET /ISAPI/AccessControl/Door/param/1` | `openDuration` и т.п. | — |
| 14 | `GET /ISAPI/AccessControl/UserInfo/capabilities?format=json` | `supportFunction`, способ поиска по `employeeNo` | поиск одного пользователя |
| 15 | `GET /ISAPI/Security/capabilities` | `maxIllegalLoginTimes`, `maxIllegalLoginLockTime` | риск блокировки |

Правила выполнения: одна учётная запись, без параллельных запросов, пауза между запросами, остановка при втором 401 подряд,
таймаут (10, 30) с; **никаких** PUT/DELETE и `RemoteControl`.

## 3. Решающая матрица по результатам

| Результат | Решение |
|---|---|
| `isSupportRemoteCheck=false` или нет `AcsCfg` | Remote verification невозможна → запасной сценарий A (окна доступа на терминале, аудит §11.2) — тоже только на стенде |
| Есть `ISAPIListen` + `sync` | Sync Listening (рекомендовано) |
| Есть `ISAPIListen`, нет `sync` | Async Listening |
| Нет `ISAPIListen`, есть `ISAPI` | Arming Method |
| `remoteCheckUserTypeList` **есть** в capabilities | изоляция по `userType` возможна теоретически — подтвердить на стенде |
| `remoteCheckUserTypeList` **нет** | изоляция на действующем терминале невозможна → только отдельный терминал/проход |
| `httpHosts` уже занят | Listening не использовать без согласования с владельцем той интеграции |

## 4. Тестовый стенд (обязателен перед любым W)

* Терминал **той же модели и прошивки** (DS-K1T341CM / V3.3.40), не подключённый к школьному турникету; выход реле — на индикатор/лампу или тестовый замок.
* На стенде только одна персона — копия `3818077855` (лицо тестового участника, с его согласия).
* Отдельная сеть/VLAN: стенд + ноутбук с адаптером kpp-journal.
* Сценарии — `REMOTE_VERIFICATION.md` §6.
