# События: распознавание лиц, доступ, проход

Источники — см. [README.md](README.md#обозначения-источников). Всё — **DOC**, на оборудовании не проверено, если не указано иное.

## 1. Способы получения событий [FRT §4.3, с.18–25; §5.1, с.25–29]

| Способ | Запрос | Кто открывает соединение | Замечания |
|---|---|---|---|
| Arming без подписки | `GET /ISAPI/Event/notification/alertStream` (`Connection: keep-alive`) | мы → устройство | все события; поток `multipart/mixed`, части XML/JSON + картинки |
| Arming с подпиской | `POST /ISAPI/Event/notification/subscribeEvent` | мы → устройство | только подписанные события; проверить `isSupportSubscribeEvent` в `GET /ISAPI/System/capabilities`; первая часть — `SubscribeEventResponse` |
| Listening | `httpHosts` на устройстве → устройство делает `POST` на наш URL | устройство → мы | `multipart/form-data`; по умолчанию у СКУД **один** listening-хост [с.128] |
| Поиск в журнале | `POST /ISAPI/AccessControl/AcsEvent?format=json` | мы → устройство | для сверки/догрузки пропущенных; read-only по смыслу, но метод POST |

API: [FRT §14.1.1 с.163–175] (arming/subscribe), [§14.2.1 с.344–360] (httpHosts), [§14.6.1 с.391–411] (AcsEvent и событие доступа).

Части события разделяются boundary; `Content-Type` части говорит, XML это или JSON — разбирать по нему [FRT с.19]. В нормальном режиме устройство
не закрывает arming-соединение и не шлёт завершающий `--boundary--` [с.21, 28].

## 2. `AccessControllerEvent` — ключевые поля [FRT §14.6.1.20, с.408–411]

| Поле | Тип | Смысл |
|---|---|---|
| `dateTime` (верхний уровень) | datetime | время события |
| `eventType` | string | `AccessControllerEvent` |
| `eventState` | enum | `active`/`inactive`; для heartbeat — данные heartbeat, каждые 10 с [с.516] |
| `majorEventType`, `subEventType` | int | major/minor тип в **десятичном** виде; расшифровка — [ACET] |
| `employeeNoString` | string | ID персоны. «the node employeeNoString will be parsed in priority; if not configured, the node employeeNo will be parsed» |
| `employeeNo` | int | устаревший числовой вариант |
| `name` | string | имя |
| `serialNo` | int | порядковый номер события, `[1,100000]`, **переполняется и начинается заново** |
| `frontSerialNo` | int | номер предыдущего события — для обнаружения потерь |
| `currentEvent` | bool | событие в реальном времени (а не догрузка) |
| `remoteCheck` | bool | **требуется удалённая проверка** (это запрос на авторизацию, см. `REMOTE_VERIFICATION.md`) |
| `userType` | enum | `normal`, `visitor`, `blacklist`, `administrators` |
| `currentVerifyMode` | enum | текущий режим аутентификации считывателя (`card`, `faceOrFpOrCardOrPw`, …) |
| `doorNo`, `cardReaderNo`, `verifyNo` | int | дверь/считыватель |
| `attendanceStatus` | enum | `checkIn`, `checkOut`, `breakOut`, … — признак учёта рабочего времени, **не направление прохода** |
| `unlockType` | enum | способ открытия (только для minor «unlock record») |
| `picturesNumber`, `pictureURL` | — | фото |
| `faceRecognitionFailedReason`, `faceSimilarity` | — | детали распознавания |
| `remoteCheckResult` | — | только в §10.16 (прошивки 2024+); в схеме не описано |

## 3. Типы событий, важные для КПП [ACET]

Major `0x5` = «Other Events» (события аутентификации/двери) [ACET с.16–23].

| Hex | Dec | Описание | Тип для нас |
|---|---|---|---|
| 0x5 / 0x4b | 5 / 75 | Face Authentication Completed | лицо опознано (может быть запросом при `remoteCheck=true`) |
| 0x5 / 0x4c | 5 / 76 | Face Authentication Failed | отказ |
| 0x5 / 0x50 | 5 / 80 | Face Recognition Failed | лицо не распознано |
| 0x5 / 0x06 | 5 / 6 | No Permission | нет локального права |
| 0x5 / 0x07 | 5 / 7 | Invalid Card Swiping Time Period | вне расписания |
| 0x5 / 0x08 | 5 / 8 | Expired Card | истёк срок |
| 0x5 / 0x98 | 5 / 152 | Employee ID Not Exists | — |
| 0x5 / 0x15 | 5 / 21 | Door Unlocked | дверь/реле открыто |
| 0x5 / 0x16 | 5 / 22 | Door Locked | — |
| 0x5 / 0x19, 0x1a | 5 / 25, 26 | Door Open / Closed (Contact) | магнитный контакт |
| 0x5 / 0xda | 5 / 218 | **Passing Event** | фактический проход (турникет); в §10.16.6 — после прохода [FRT с.135] |
| 0x5 / 0x86 | 5 / 134 | Reverse Passing | проход в обратную сторону |
| 0x5 / 0x89 | 5 / 137 | Passing Timed Out | не прошёл после открытия |
| 0x5 / 0x805 | 5 / 2053 | Do Not Open Barrier When Lane Is Not Clear | — |
| 0x5 / 0x80c | 5 / 2060 | Permission Authentication Is Intercepted | — (значение не раскрыто) |
| 0x5 / 0x32 | 5 / 50 | Card Platform Authentication | — |
| 0x3 / 0x400 | 3 / 1024 | Door Remotely Open | открытие командой `RemoteControl/door` |
| 0x5 / 0x34 | 5 / 52 | Fire Relay Closed: Door Remains Open | пожарный режим |
| 0x2 / 0x426, 0x427 | 2 / 1062, 1063 | Face Recognition Terminal Online/Offline | — |

Точные страницы ACET — `raw/01_access_control_event_types.md` (маркеры `<!-- page: N -->`). Некоторые описания искажены водяным знаком.

## 4. Запрос до прохода vs. события после

```
лицо → [устройство: локальная проверка] → AccessControllerEvent{remoteCheck:true, serialNo:N}  ← ЗАПРОС (ждёт ответа)
        → наш ответ RemoteCheck{serialNo:N, checkResult}                                     ← РЕШЕНИЕ
        → (опц.) AccessControllerEvent{remoteCheckResult}  (прошивки 2024+)                    ← ФАКТ решения
        → Door Unlocked 0x15 / Passing Event 0xda / Passing Timed Out 0x89                     ← ФАКТ прохода
```

Только первое — авторизация. Остальное — для журнала: `Exit` в kpp-journal фиксировать по факту прохода (0xda), а при его отсутствии —
как «доступ разрешён, проход не подтверждён» (см. `INTEGRATION_ARCHITECTURE.md`).

## 5. Направление прохода

В событии нет явного поля «вход/выход». `attendanceStatus` — учёт рабочего времени, а не направление. Для турникета есть «Reverse Passing» (0x86),
но какое направление считается прямым — **не описано**. Направление определять **конфигурацией**: какой терминал/считыватель (`doorNo`,
`cardReaderNo`, IP устройства) стоит на выходе. Проверить на месте.

## 6. Дедупликация и потери

* `serialNo` переполняется (`[1,100000]`) и может сброситься после сброса устройства → ключ: (`device_id`, `serialNo`, `dateTime`).
* `frontSerialNo` позволяет заметить пропуск [с.410]; догружать через `POST AcsEvent` с `beginSerialNo`/`endSerialNo` или `startTime`/`endTime` [с.396–397].
* `AcsEventCond`: `searchID`, `searchResultPosition`, `maxResults`, `major`, `minor`, `startTime`, `endTime`, `employeeNoString`, `picEnable`, `timeReverseOrder` [с.396–397].
  Поставить `picEnable: false`, чтобы не тянуть фото.
