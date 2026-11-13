# Ошибки ISAPI

Полный словарь: [EC] = `ISAPI/Field Dictionary (1).xlsx` (реально — ErrorCode) → `raw/03_error_code.md` (2269 кодов).
Поиск: `grep -n "<subStatusCode или 0x…>" docs/hikvision/raw/03_error_code.md`.

## 1. Структура ответа об ошибке

JSON (API с `format=json`) [FRT с.427, 521]:
```json
{ "statusCode": 4, "statusString": "Invalid Operation", "subStatusCode": "notSupport",
  "errorCode": 1073741825, "errorMsg": "…", "MErrCode": "0x…", "MErrDevSelfEx": "0x…" }
```
XML `ResponseStatus` [FRT с.518]: `requestURL`, `statusCode`, `statusString`, `subStatusCode`, `description`, `MErrCode`, `MErrDevSelfEx`.
HTTP-статус при ошибке ≠ 200 (пример 403 — [FRT §4.2.6, с.18]).

`errorCode` в JSON — целое; в словаре [EC] — шестнадцатеричное (`0x40000001` = 1073741825).

## 2. Классы `statusCode` [FRT с.518; EC]

| statusCode | statusString | Кол-во кодов в EC | Обработка в адаптере |
|---|---|---|---|
| 0, 1 | OK | 10 | успех (`1` — также «ok» с предупреждением, напр. `riskPassword`) |
| 2 | Device Busy | 14 | повтор с backoff, не более N раз |
| 3 | Device Error | 119 | алерт, без повтора |
| 4 | Invalid Operation | 1570 (+18 с китайским `操作错误`) | ошибка логики/прав — без повтора |
| 5 | Invalid Format (XML/JSON) | 3 | баг клиента |
| 6 | Invalid Content | 530 | баг клиента / неверные данные |
| 7 | Reboot Required | 2 | **никогда** не перезагружать автоматически |
| 8 | Batch Operation | 3 | разбирать по элементам |

## 3. Коды, важные для нашей интеграции [EC]

| subStatusCode | errorCode | Описание | Когда ждать |
|---|---|---|---|
| `notSupport` | 0x40000001 | Not supported | функция/поле не поддерживается прошивкой (например, `remoteCheckUserTypeList`) |
| `lowPrivilege` | 0x40000002 | No permission | у учётной записи адаптера нет прав |
| `methodNotAllowed` | 0x40000004 | Invalid HTTP method | неверный метод |
| `invalidOperation` | 0x40000006 | Invalid input command | — |
| `invalidID` | 0x40001008 | Invalid ID | неверный doorID/hostID |
| `userNameLocked` | 0x40001A19 | The user name is locked | после серии неудачных входов (см. `AUTHENTICATION.md` §3) |
| `theSessionIdDoesNotExist` | 0x40001135 | The session ID does not exist | — |
| `deviceBusy` | 0x20000004 | Device is busy or no response | повтор |
| `noMemory` | 0x20000001 | Not enough memory | — |
| `deviceError` | 0x30000001 | Device hardware error | алерт |
| `badXmlFormat` / `badJsonFormat` | 0x50000001 / 0x50000002 | Ошибка формата | баг клиента |
| `badXmlContent` / `badJsonContent` | 0x60000003 / 0x60000017 | Неверное содержимое | баг клиента |
| `MessageParametersLack` | 0x60000019 | No message parameter | не хватает обязательного поля |
| `employeeNoNotExist` | 0x6000601f | The employee No. does not exist | поиск/изменение несуществующего пользователя |
| `employeeNoAlreadyExist` | 0x60006020 | The employee No. already exists | `UserInfo/Record` для существующего |
| `illegalEmployeeNo` | 0x60006036 | Incorrect employee No. | формат/длина `employeeNo` |
| `deviceUserAlreadyExist` | 0x60007002 | The person already exists | — |
| `cardNoAlreadyExist` | 0x60006033 | Card No. already exists | — |
| `rebootRequired` | 0x70000001 | Takes effect after rebooting | **стоп**, решение принимает человек |

Кодов, специфичных для `remoteCheck`/`AcsCfg`, в словаре **не найдено** (поиск по `remoteCheck`, `AcsCfg`). Ошибки этих API, вероятно, общие (`notSupport`, `badJsonContent`, …) — **проверить на стенде**.

## 4. HTTP-уровень

| HTTP | Значение | Действие |
|---|---|---|
| 401 | нет/неверная Digest-авторизация (первый 401 — нормальная часть рукопожатия) | второй 401 подряд → стоп, алерт (риск блокировки) |
| 403 | запрещено / ошибка ISAPI | разобрать тело |
| 404 | URL не поддерживается | считать функцию неподдерживаемой |
| 5xx / таймаут | устройство недоступно | backoff; для удалённой проверки решение = отказ (fail-closed) |

## 5. Особенности словаря
* `Status Code` в исходнике хранится то числом, то строкой; MarkItDown вывел `1.0`, `4.0` — это артефакт pandas.
* Пустые описания отображены как `NaN`.
