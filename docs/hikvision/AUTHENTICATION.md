# Аутентификация, подключение, таймауты

Источники — см. [README.md](README.md#обозначения-источников). Статусы: **DOC** — описано в документации; **HW** — подтверждено на нашем оборудовании; **?** — не известно.

## 1. HTTP Digest Authentication

| Факт | Статус | Источник |
|---|---|---|
| Клиент обязан использовать HTTP Digest (RFC 7616) | DOC | [FRT §4.1, с.10] |
| Пример Python: `requests.auth.HTTPDigestAuth('admin', '…')` | DOC | [FRT §4.1.4, с.11] |
| Первый запрос без авторизации → `401 Unauthorized` с `WWW-Authenticate: Digest qop="auth", realm="…", nonce="…", stale="FALSE"`; повтор с `Authorization: Digest …` → `200` | DOC | [FRT §4.3.1.1, с.19] (пример для `alertStream`) |
| `GET /ISAPI/System/deviceInfo` с Digest на DS-K1T341CM V3.3.40 → 200 | HW (со слов заказчика) | `HTA_STUDENT_RELEASE_TECHNICAL_AUDIT.md` §11.4 |
| `POST /ISAPI/AccessControl/UserInfo/Search?format=json` с Digest, постранично по 30, выгружено 2216 записей | HW | `export_hikvision_users.py`, `hikvision_users.json` (не в git) |
| Сессионный вход (`/ISAPI/Security/sessionLogin`) | **не описан** в наборе | поиск по FRT — 0 совпадений |

**Практика (наш код):** `export_hikvision_users.py` создаёт новую `requests.Session` с новым `HTTPDigestAuth` и `Connection: close` на каждую страницу,
делает паузу 5 с и останавливается при первом 401, не повторяя попытку. Это сознательная защита от блокировки учётной записи (см. §3).

## 2. Формат сообщений

* XML: `Content-Type: application/xml; charset="UTF-8"`, namespace `http://www.isapi.org/ver20/XMLSchema`, version `2.0` [FRT §4.2.1.1, с.11].
* JSON: признак — query-параметр `format=json` в URL; бывают исключения — смотреть определение API [FRT §4.2.1.2, с.11].
* Время: ISO 8601, рекомендуется формат с часовым поясом `YYYY-MM-DDThh:mm:ss+hh:mm`; старые устройства могут вернуть `Z` и поле `timeDiff`; клиент должен понимать оба [FRT §4.2.4, с.16].
* Ошибка: HTTP-статус ≠ 200 + тело с ISAPI-кодом ошибки [FRT §4.2.6, с.17–18] → см. `ERROR_CODES.md`.
* Допустимые символы в строковых полях и именах — таблица [FRT §4.2.5, с.16–17].

## 3. Блокировка после неудачных входов

| Параметр | Значение по документации | Источник |
|---|---|---|
| `maxIllegalLoginTimes` | 3–20, по умолчанию 5 | [FRT §14.1.4.2 Get the system security capability, с.211] |
| `maxIllegalLoginLockTime` | 1–120 мин, по умолчанию 30 | [FRT с.212] |
| Флаг поддержки | `issupIllegalLoginLock` / `issupportIllegalLoginLock` | [FRT с.209–211] |
| Ошибка «user name is locked» | `userNameLocked`, `0x40001A19` | [EC] |
| События журнала | «Remote: Lock Login» `0x137`, «Remote: Unlock Login» `0x138`; «Local Login Lock/Unlock» `0x428`(значение восстановлено по порядку)/`0x429` | [ACET с.10; с.5–6] |

Наш скрипт выгрузки при 401 печатает из XML-ответа `lockStatus`, `unlockTime`, `retryLoginTime` — эти поля в FRT **не описаны** (известны из практики, **?**).

**Правило для адаптера:** не повторять запрос автоматически после 401 с той же парой логин/пароль более 1 раза (повтор нужен только для
digest-рукопожатия, `requests`/`httpx` делают это сами); при втором 401 — остановиться и поднять алерт. Иначе действующий терминал может заблокировать учётную запись на 30 минут.

## 4. Таймауты и соединения

| Сценарий | Что известно | Источник |
|---|---|---|
| Обычный запрос | Пример кода: `CURLOPT_TIMEOUT 5`, `CURLOPT_CONNECTTIMEOUT 5` | [FRT §4.1.1, с.10] |
| Наш скрипт | `TIMEOUT = (10, 60)` (connect, read) — для поиска пользователей | `export_hikvision_users.py:33` |
| Постоянное соединение (arming) | `GET /ISAPI/Event/notification/alertStream` с `Connection: keep-alive`; устройство шлёт события и heartbeat; клиент не может отправлять данные в это соединение; при таймауте heartbeat — разорвать и переподключиться | [FRT §4.3.1, с.18; §5.1.3, с.29] |
| Heartbeat | `eventState` для heartbeat; «uploaded every 10 seconds» | [FRT с.516] (описание `eventState`) |
| Пример заголовка | `Keep-Alive: timeout=10, max=99` в ответе 401 | [FRT с.19] |
| Listening (устройство → нам) | устройство само открывает соединение; может закрыть после передачи или держать | [FRT §10.16.3.1, с.128] |
| Таймаут удалённой проверки | `remoteCheckTimeout` 1–10 с | [FRT с.424, 428] |
| Число одновременных arming-подключений | **не описано** — **?** | — |

## 5. Аутентификация устройства перед нашим сервером (Listening)

В `httpHosts` есть `httpAuthenticationMethod`: в примере `none`; «MD5 digest authentication is recommended for higher security» [FRT §10.16.3.2.1, с.129].
Значит, наш HTTP-приёмник должен уметь принимать Digest от устройства (или работать в изолированном VLAN с allowlist IP устройства).
Детали схемы `httpHosts` — [FRT §14.2.1, с.344–360]. Параметры `security`/`iv` (шифрование чувствительных полей в query) — **не разобраны**, проверить.

## 6. Хранение учётных данных

* Логин/пароль терминала — только в переменных окружения/секретах развертывания (`.env` уже в `.gitignore`), не в коде и не в `docs/`.
* Отдельная учётная запись ISAPI для адаптера с минимальными правами (оператор/только чтение на этапе пилота) — **проверить**, поддерживает ли терминал такие роли.
