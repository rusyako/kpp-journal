# ISAPI API Reference — что нужно kpp-journal

Полный автоматический список (263 endpoint’а гл. 14 FRT, метод/путь/раздел/страница): **[API_ENDPOINT_INDEX.md](API_ENDPOINT_INDEX.md)**.
Здесь — отобранные endpoint’ы с классом риска. Схемы полей — по ссылкам на страницы; сырой текст — `raw/05_isapi_frt_value_series/p<диапазон>.md`, искать `<!-- page: N -->`.

Класс риска: **R** — только чтение; **R\*** — метод `POST`, но по смыслу поиск (без изменений); **W** — изменяет конфигурацию/данные;
**X** — физическое действие (дверь). На действующих терминалах разрешено только **R/R\*** и только после явного разрешения на сетевые запросы.

## 1. Общие правила
* Аутентификация — HTTP Digest (`AUTHENTICATION.md`).
* JSON-API — с `?format=json`; без него обычно XML [FRT §4.2.1, с.11].
* Ответ об ошибке — `statusCode/subStatusCode/errorCode` (`ERROR_CODES.md`).
* «Capabilities first»: каждый поток в гл. 10 начинается с `GET …/capabilities` и проверки флага `isSupport…`.

## 2. Система и возможности

| Метод | Путь | Риск | Назначение | Источник |
|---|---|---|---|---|
| GET | `/ISAPI/System/deviceInfo` | R | модель, прошивка, серийный № | упоминается [FRT с.10–11, 257–258]; схемы в гл.14 нет. **HW: 200** |
| GET | `/ISAPI/System/capabilities` | R | в т.ч. `isSupportSubscribeEvent` | [FRT с.20, 27; API §14.1.4.3, с.213] |
| GET | `/ISAPI/Security/capabilities?username=` | R | политика блокировки входа | [§14.1.4.2, с.209–212] |
| GET | `/ISAPI/AccessControl/capabilities` | R | `isSupportRemoteCheck`, `isSupportAcsCfg`, `isSupportUserInfo`, `isSupportFDLib`, `EmployeeNoInfo` … | только в потоках гл.10 (с.62–143); **схемы нет** |

## 3. Удалённая проверка и настройки контроллера

| Метод | Путь | Риск | Источник |
|---|---|---|---|
| GET | `/ISAPI/AccessControl/AcsCfg/capabilities?format=json` | R | [§14.6.3.1, с.423–425] |
| GET | `/ISAPI/AccessControl/AcsCfg?format=json` | R | [§14.6.3.3, с.427–428] |
| PUT | `/ISAPI/AccessControl/AcsCfg?format=json` | **W (глобально!)** | [§14.6.3.2, с.425–427] |
| GET | `/ISAPI/AccessControl/remoteCheck/capabilities?format=json` | R | [§14.6.15.1, с.519–520] |
| PUT | `/ISAPI/AccessControl/remoteCheck?format=json` | **X** (решение по ожидающему запросу) | [§14.6.15.2, с.520–521] |
| GET | `/ISAPI/AccessControl/AcsWorkStatus?format=json` | R | [§14.6.3.5, с.430–431] |

## 4. События

| Метод | Путь | Риск | Источник |
|---|---|---|---|
| GET | `/ISAPI/Event/notification/alertStream` | R (постоянное соединение) | [§4.3.1.1, с.18–19; §14.1.1.1, с.163] |
| GET | `/ISAPI/Event/notification/subscribeEventCap` | R | [§14.1.1.5, с.173] |
| POST | `/ISAPI/Event/notification/subscribeEvent` | R\* (создаёт подписку на время соединения) | [§14.1.1.4, с.170–173] |
| GET | `/ISAPI/Event/notification/httpHosts` | R | [§14.2.1.8, с.358] |
| GET | `/ISAPI/Event/notification/httpHosts/capabilities` | R | [§14.2.1.5, с.351] |
| POST/PUT/DELETE | `/ISAPI/Event/notification/httpHosts[/<hostID>]` | **W** (может сломать существующую интеграцию) | [§14.2.1, с.344–358] |
| GET | `/ISAPI/AccessControl/AcsEvent/capabilities?format=json` | R | [§14.6.1.1, с.391] |
| POST | `/ISAPI/AccessControl/AcsEvent?format=json` | R\* | [§14.6.1.5, с.396–399] |
| PUT | `/ISAPI/AccessControl/AcsEvent/StorageCfg?format=json` | **W** (режим хранения журнала) | [§14.6.1.4, с.396] |
| — | `AccessControllerEvent` (схема события) | — | [§14.6.1.20, с.408–411] |

## 5. Персоны и учётные данные

| Метод | Путь | Риск | Источник |
|---|---|---|---|
| GET | `/ISAPI/AccessControl/UserInfo/capabilities?format=json` | R | поток [§10.15.2.2, с.119] |
| GET | `/ISAPI/AccessControl/UserInfo/Count?format=json` | R | [с.120] |
| POST | `/ISAPI/AccessControl/UserInfo/Search?format=json` | R\* | [с.120]; **HW: работает** (`export_hikvision_users.py`) |
| PUT | `/ISAPI/AccessControl/UserInfo/SetUp`, `…/Modify` / POST `…/Record` | **W** | [с.121–123] |
| PUT | `/ISAPI/AccessControl/UserInfoDetail/Delete?format=json` | **W (удаление!)** | [§14.6.10–11, с.502–505] |
| GET/POST/PUT | `/ISAPI/Intelligent/FDLib/*` | R / **W** | [§10.10, с.89–97; §14.4, с.361–379] |
| GET/PUT | `/ISAPI/AccessControl/UserRight*` (расписания прав) | R / **W** | [§14.6.9, с.492–501] |

## 6. Двери

| Метод | Путь | Риск | Источник |
|---|---|---|---|
| GET | `/ISAPI/AccessControl/Door/param/<doorID>[/capabilities]` | R | [§14.6.4.4, 14.6.4.6, с.434–437] |
| PUT | `/ISAPI/AccessControl/Door/param/<doorID>` | **W** | [§14.6.4.5, с.436] |
| GET | `/ISAPI/AccessControl/RemoteControl/door/capabilities` | R | [§14.6.14.2, с.519] |
| PUT | `/ISAPI/AccessControl/RemoteControl/door/<doorID>` | **X — запрещено** | [§14.6.14.1, с.517–518] |
| PUT | `/ISAPI/AccessControl/DoorStatusWeekPlanCfg/<id>` | **W** | [§14.6.2.15, с.420] |

## 7. Чего в наборе нет
Схемы: `GET /ISAPI/AccessControl/capabilities`, `UserInfo/*` (кроме asyncImport/Delete), `CardInfo/*`, `System/deviceInfo`.
URL известны из потоков гл. 10 и из практики. Для точных схем нужен общий *ISAPI Access Control* guide (запросить у Hikvision/дистрибьютора).
