# Remote Verification (удалённая проверка) — исследование

> Статус: **только по документации**. Ни одно утверждение ниже не проверено на нашем терминале
> (DS-K1T341CM, прошивка V3.3.40 — данные из `HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md` §11.4).
> Обозначения источников — см. [README.md](README.md#обозначения-источников). Номера страниц — физические страницы PDF (1-based).

## 1. Целевая логика kpp-journal

1. Терминал распознаёт лицо → 2. определяет `employeeNo` → 3. **до открытия** отправляет запрос в нашу систему →
4. kpp-journal проверяет действительное разрешение (в т.ч. подтверждение родителей) → 5. только при `success` терминал открывает турникет →
6. при отказе/таймауте проход закрыт → 7. фактический проход фиксируется отдельно.

**Ключевое требование:** терминал не должен выпускать ученика только потому, что его лицо зарегистрировано.

## 2. Что говорит документация (§10.16, FRT с.125–136)

### 2.1 Назначение
«In high-security scenarios, local device authentication alone is inadequate. Devices need to upload authentication information
to the platform, which then determines whether to unlock the door.» — [FRT §10.16.1, с.125]

Это именно **предварительная авторизация**: устройство отправляет событие с `remoteCheck: true` и ждёт решения платформы;
дверь управляется по результату (`PUT /ISAPI/AccessControl/remoteCheck`). — [FRT §10.16.2.1 шаги 4–5, с.125–126]

### 2.2 Четыре механизма

| Механизм | `checkChannelType` | Кто инициирует соединение | Как платформа отдаёт решение | Источник |
|---|---|---|---|---|
| **Arming Method** | `ISAPI` | Платформа держит постоянное соединение `GET /ISAPI/Event/notification/alertStream?deployID=` или `POST .../subscribeEvent?deployID=` | Отдельным запросом `PUT /ISAPI/AccessControl/remoteCheck?format=json&security=&iv=` на устройство | [FRT §10.16.2.1, с.125–126] |
| **Asynchronous Listening** | `ISAPIListen` + `remoteCheckWithISAPIListen: "async"` | Устройство делает `POST` на наш HTTP-хост (`httpHosts`) | Отвечаем `200 OK`, затем отдельно `PUT .../remoteCheck` на устройство | [FRT §10.16.3, с.127–130] |
| **Synchronous Listening** | `ISAPIListen` + `remoteCheckWithISAPIListen: "sync"` | Устройство делает `POST` на наш HTTP-хост | **В теле HTTP-ответа** на тот же POST: JSON `{"RemoteCheck":{"serialNo":…,"checkResult":"success"}}` | [FRT §10.16.4, с.130–133] |
| **Verification by Platform Only** | любой из выше + `needDeviceCheck: false` | — | Как выше, плюс `userInfo` для отображения на экране | [FRT §10.16.5, с.133–134] |

Ещё два варианта в §10.16 (Group Ticket, Text QR Code — [FRT §10.16.6–10.16.7, с.134–136]) к нашей задаче не относятся.

### 2.3 Параметры `AcsCfg` (настройка — `PUT /ISAPI/AccessControl/AcsCfg?format=json`)

Пример из §10.16.2.2.1 / §10.16.3.2.2 / §10.16.4.2.2 [FRT с.126, 129, 132]:

```json
{
  "AcsCfg": {
    "remoteCheckDoorEnabled": true,
    "checkChannelType": "ISAPIListen",
    "needDeviceCheck": true,
    "remoteCheckTimeout": 5,
    "remoteCheckVerifyMode": 7,
    "offlineDevCheckOpenDoorEnabled": false,
    "remoteCheckUserTypeList": ["normal", "visitor", "unregistered"],
    "remoteCheckWithISAPIListen": "sync"
  }
}
```

| Поле | Смысл по документации | Где описано | Примечание |
|---|---|---|---|
| `remoteCheckDoorEnabled` | Главный выключатель удалённой проверки | §10.16 примеры; API Ref: caps [с.424], PUT [с.426], GET [с.428] | По умолчанию `false` [с.424] |
| `checkChannelType` | `Ezviz`, `ISUP`, `ISAPI`, `PrivateSDK`, `ISAPIListen` | caps [с.424], PUT [с.426] | Действует при `remoteCheckDoorEnabled=true` [с.426] |
| `needDeviceCheck` | Требуется ли локальная аутентификация на устройстве до удалённой проверки; по умолчанию `true` | примеры [с.126]; caps [с.424]; GET [с.428] | **Отсутствует в схеме PUT** [с.426] |
| `remoteCheckTimeout` | Таймаут ожидания решения, 1–10 с; «if no result is received within this time, the verification fails» | примеры [с.126]; caps [с.424]; GET [с.428] | **Отсутствует в схеме PUT** |
| `remoteCheckVerifyMode` | Тип учётных данных, требующих удалённой проверки (1–15, таблица на с.127) | таблица [с.127]; caps `@opt [1..7]` [с.424]; GET [с.428] | Противоречие: таблица 1–15, caps — 1–7. **Отсутствует в схеме PUT** |
| `offlineDevCheckOpenDoorEnabled` | Разрешать ли открытие по локальной аутентификации, когда устройство **offline**; по умолчанию `false` | примеры [с.126]; caps [с.424]; GET [с.428] | Не определено, что такое «offline» (нет связи с платформой? таймаут?) — **проверить** |
| `remoteCheckUserTypeList` | Список типов персон, для которых нужна удалённая проверка; «if absent or empty, all person types require remote verification» | **только** комментарии в примерах [с.126, 129, 132] | **Нет в API Reference** (ни caps, ни PUT, ни GET). Значение `unregistered` не входит в перечисление `userType` (normal, visitor, blackList, administrators — [с.393, 410]) |
| `remoteCheckWithISAPIListen` | `async` / `sync` | примеры [с.129, 132]; caps [с.425]; GET [с.428] | **Отсутствует в схеме PUT** |

> ⚠ Схема `PUT AcsCfg` в API Reference [FRT §14.6.3.2, с.425–426] перечисляет только `remoteCheckDoorEnabled`, `checkChannelType`, `channelIp`
> из группы удалённой проверки. Остальные поля известны из примеров §10.16 и из `GET`. Перед любым изменением нужно
> получить `GET /ISAPI/AccessControl/AcsCfg/capabilities?format=json` на конкретном устройстве.

### 2.4 Значения `remoteCheckVerifyMode` [FRT с.127]

| № | Тип | № | Тип |
|---|---|---|---|
| 1 | Face and ID card comparison | 9 | Face and ID card comparison or QR code |
| 2 | **Face recognition** | 10 | Face recognition or QR code |
| 3 | Face and ID card comparison or face recognition | 11 | Face and ID card comparison, face recognition, or QR code |
| 4 | Card swiping | 12 | Card swipe or QR code |
| 5 | Face and ID card comparison or card swiping | 13 | Face and ID card comparison, card swipe, or QR code |
| 6 | Face recognition or card swipe | 14 | Face recognition, card swipe, or QR code |
| 7 | Face and ID card comparison, card swipe, or face recognition | 15 | Face and ID card comparison, card swipe, face recognition, or QR code |
| 8 | QR code | | |

MarkItDown разорвал эту таблицу на отдельные столбцы и перемешал строки 11–15 (`raw/05_isapi_frt_value_series/p126-150.md`, страница 127).
Таблица выше **сверена с изображением страницы 127 PDF** (рендер, 2026-11-11).

Примечания [FRT с.127]:
* при `needDeviceCheck=true` и режиме `2`: распознавание лица запускает удалённую проверку **после** локальной аутентификации; остальные способы — только локальная;
* при `needDeviceCheck=false` и режиме `2`: распознавание лица запускает удалённую проверку **без** локальной аутентификации; остальные способы удалённую проверку не запускают.
  (В PDF пункт 3 содержит опечатку «requires … (i.e., needDeviceCheck is false)».)

### 2.5 Запрос от устройства (пример, FRT с.130 и 132–133)

`POST <url из httpHosts>`, `Content-Type: multipart/form-data; boundary=…`, часть `AccessControllerEvent` (JSON) + часть `Picture` (JPEG):

```json
{
  "ipAddress": "10.6.123.199", "portNo": 80, "channelID": 6,
  "dateTime": "2022-11-14T13:41:56+08:00", "activePostCount": 1,
  "eventType": "AccessControllerEvent", "eventState": "active",
  "AccessControllerEvent": {
    "majorEventType": 5, "subEventType": 75,
    "name": "test123", "employeeNoString": "test",
    "serialNo": 1866, "currentEvent": true,
    "remoteCheck": true, "frontSerialNo": 1865, "picturesNumber": 1
  }
}
```

* `majorEventType 5` / `subEventType 75` = `0x5`/`0x4b` «Face Authentication Completed» [ACET с.18].
* Запрос на проверку — это событие с `remoteCheck: true` [FRT §10.16.2.1 шаг 4, с.126; API Ref с.410].
* Типы событий-запросов: `AccessControllerEvent`, `IDCardInfoEvent`, `QRCodeEvent`, `FaceTemperatureMeasurementEvent` [с.126, 128, 131].

### 2.6 Ответ платформы

`PUT /ISAPI/AccessControl/remoteCheck?format=json` [API Ref §14.6.15.2, с.520–521]:

| Поле | Тип | Обяз. | Смысл |
|---|---|---|---|
| `RemoteCheck.serialNo` | int | req | Должен совпадать с `serialNo` события |
| `RemoteCheck.checkResult` | enum | req | `success` / `failed` |
| `RemoteCheck.info` | string 1–1024 | opt | Доп. информация (capabilities: 1–32 [с.520] — расхождение) |
| `RemoteCheck.userInfo` | object | opt | `name`, `employeeNo`, `cardNo`, `filePathType`, `filePath` — для режима Platform Only |
| `customFileID`, `successCustomInfo` | — | opt | Авиа/метро-сценарии, нам не нужны |

Ответ устройства: `statusCode`, `statusString`, `subStatusCode`, `errorCode`, `errorMsg` [с.521].
В синхронном режиме тот же JSON возвращается **в теле HTTP-ответа** на POST устройства [FRT §10.16.4.1 шаг 4b, с.131; пример с.133].

В §10.16 URL указан с `&security=<security>&iv=<iv>` (шифрование чувствительных полей), а в API Reference [с.520] query-параметров нет — **уточнить на устройстве**.

### 2.7 Событие с результатом

«(Dependent) If the device initially uploaded an access control event (AccessControllerEvent), it can upload a verification event after
remote verification is complete. This event must be of type AccessControllerEvent and include the remoteCheckResult field. …
Generally, only devices with firmware from 2024 or later support this feature.» — [FRT с.126, 129, 132]

Поле `remoteCheckResult` в схеме события API Reference [с.408–411] **не описано**. Наша прошивка V3.3.40 — год выпуска неизвестен.

## 3. Ответы на обязательные вопросы

| Термин | Что это | Где |
|---|---|---|
| `isSupportRemoteCheck` | Флаг в `GET /ISAPI/AccessControl/capabilities`; `true` = устройство поддерживает удалённую проверку | [FRT с.125, 127, 128, 131]. Схемы `AccessControl/capabilities` в API Reference этого документа **нет** |
| `remoteCheck` | (1) bool в событиях `AccessControllerEvent`/`QRCodeEvent`/…: «whether remote verification is required» [с.410, 516]; (2) путь `/ISAPI/AccessControl/remoteCheck` | §10.16; API Ref §14.6.15 |
| `RemoteCheck` | Корневой объект JSON ответа платформы (`serialNo`, `checkResult`, …) | [с.127, 133–134, 520–521] |
| `remoteCheckUserTypeList` | Фильтр по типу персоны; пусто/нет = все типы | Только примеры [с.126, 129, 132] |
| `offlineDevCheckOpenDoorEnabled` | Открывать ли по локальной проверке в офлайне; по умолчанию `false` | [с.126, 424, 428] |

### Не путать

* **Предварительный запрос:** `AccessControllerEvent` с `remoteCheck: true` (до открытия, устройство ждёт решения).
* **События после решения/прохода:** `AccessControllerEvent` с `remoteCheckResult` (2024+), «Door Unlocked» `0x5/0x15`, «Passing Event» `0x5/0xda` (218), «Door Open (Contact)» `0x5/0x19` [ACET с.16–22].
  Это уже свершившиеся факты, их нельзя использовать как авторизацию — только для журнала.
* `PUT /ISAPI/AccessControl/RemoteControl/door/<doorID>` с `cmd=open` [с.517–518] — **не** удалённая проверка, а безусловная команда
  открытия; не привязана к человеку перед турникетом. Для автоматического выпуска не использовать (и запрещено без разрешения).

## 4. Какой механизм подходит

**Рекомендация: Synchronous Listening (`checkChannelType=ISAPIListen`, `remoteCheckWithISAPIListen=sync`) + `needDeviceCheck=true` + `remoteCheckVerifyMode=2` + `offlineDevCheckOpenDoorEnabled=false`.**

| Критерий | Arming | Async Listening | **Sync Listening** | Platform Only |
|---|---|---|---|---|
| Устройство знает `employeeNo` до запроса | да (`needDeviceCheck=true`) | да | **да** | неясно: устройство не аутентифицирует локально; для лица `employeeNo` может не быть |
| Сетевое направление | платформа → устройство (постоянное) + PUT | устройство → платформа + платформа → устройство | **только устройство → платформа** | — |
| Связь решения с запросом | по `serialNo` | по `serialNo` | **тот же HTTP-обмен** | — |
| Риски | обрыв постоянного соединения; лимит числа подключений неизвестен | 2 канала, гонки | один HTTP-хост на устройстве («By default, access control devices support only one HTTP(S) listening server» [с.128, 131]) — может быть занят | надо самим распознавать лицо — не наш случай |

Почему так:
* `needDeviceCheck=true`: незарегистрированное лицо / лицо без локального права отсекается устройством; до нас доходят только опознанные с `employeeNo`.
* Режим `2` (только лицо): карты и прочие способы остаются на локальной проверке — **но** это настройка всего устройства, см. §5.
* `offlineDevCheckOpenDoorEnabled=false` + истечение `remoteCheckTimeout` = «verification fails» → поведение fail-closed по документации. **Проверить на стенде.**

Asynchronous Listening — запасной вариант, если sync не поддерживается прошивкой (`remoteCheckWithISAPIListen` отсутствует в capabilities).

## 5. Изоляция пилота на одном `employeeNo`

**Вывод: штатного фильтра по конкретному `employeeNo` в документации нет.** Все параметры (`remoteCheckDoorEnabled`, `remoteCheckVerifyMode`, `needDeviceCheck`,
`offlineDevCheckOpenDoorEnabled`, `httpHosts`) — глобальные для устройства (`AcsCfg` — «parameters of the access controller» [с.425]).

Единственный рычаг — `remoteCheckUserTypeList` (по **типу** персоны). Теоретическая схема:
* у всех 2216 пользователей текущего терминала `userType = "normal"` (выгрузка `hikvision_users.json`, проверено скриптом);
* перевести только тестового `3818077855` в `userType = "visitor"` и выставить `remoteCheckUserTypeList = ["visitor"]` —
  тогда удалённая проверка затронет только его.

Почему это **нельзя делать на действующем терминале** без стенда:
1. `remoteCheckUserTypeList` не описан в API Reference — поддержка DS-K1T341CM V3.3.40 неизвестна. Если устройство **молча проигнорирует** поле,
   «absent or empty → all person types require remote verification» → все 2216 человек пойдут в удалённую проверку; при сбое сервера — массовый отказ прохода.
2. Требуется изменить запись пользователя (`userType`) и глобальный `AcsCfg` и `httpHosts` — всё это запрещено без отдельного разрешения.
3. Тип `visitor` может иметь иную семантику на устройстве (ограничения визитёров) — не описано.
4. Единственный слот `httpHosts` может быть занят существующей интеграцией (например, HikCentral) — перезапись сломает её.

**Решение:** отдельный тестовый стенд — терминал той же модели и прошивки (DS-K1T341CM, V3.3.40), не подключённый к школьному турникету
(или подключённый к индикатору/реле-лампе), с единственным пользователем `3818077855`. Подробно — `DEVICE_CAPABILITIES.md` и план пилота в `README.md`.

## 6. Что проверить на оборудовании (стенд)

| # | Проверка | Ожидание по документации |
|---|---|---|
| 1 | `GET /ISAPI/AccessControl/capabilities` → `isSupportRemoteCheck`, `isSupportAcsCfg` | `true` |
| 2 | `GET /ISAPI/AccessControl/AcsCfg/capabilities?format=json` → наличие `remoteCheckWithISAPIListen`, `remoteCheckUserTypeList`, `@opt` для `remoteCheckVerifyMode` | sync/async; список типов |
| 3 | `GET /ISAPI/AccessControl/remoteCheck/capabilities?format=json` | `serialNo`, `checkResult` |
| 4 | `GET /ISAPI/Event/notification/httpHosts` и `/capabilities` | сколько слотов, заняты ли |
| 5 | Sync: ответ `success` → турникет открывается; `failed` → нет | — |
| 6 | Нет ответа > `remoteCheckTimeout` → отказ | «verification fails» |
| 7 | Сервер недоступен (порт закрыт) при `offlineDevCheckOpenDoorEnabled=false` → отказ | — |
| 8 | Сетевой кабель устройства отключён → поведение | не описано |
| 9 | Ответ с неверным `serialNo` / битый JSON / HTTP 500 → отказ | не описано |
| 10 | `remoteCheckUserTypeList=["visitor"]`: `normal`-пользователь проходит локально, `visitor` — через нас | по примерам |
| 11 | Режим `2`: карта не вызывает удалённую проверку | по примечанию с.127 |
| 12 | Приходит ли событие с `remoteCheckResult`; приходит ли `0xda` Passing Event от турникета | 2024+ / зависит от турникета |
| 13 | Задержка «лицо → открытие» при sync | — |
| 14 | Пожарный вход / аварийная разблокировка не зависят от удалённой проверки | — |
