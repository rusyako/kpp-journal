# Пилот userType = visitor: план Remote Verification только для visitor

Дата: 2026-11-13. Источники — [README.md](README.md#обозначения-источников).
Статусы: **IMPLEMENTED** · **TESTED** · **DOCUMENTED** · **VERIFIED ON DEVICE** · **NOT VERIFIED**.

> **Ни один запрос к реальному терминалу не выполнялся.** Всё ниже — документация, HW-выгрузка `hikvision_users.json`
> (получена ранее, не в git) и виртуальный терминал. VERIFIED ON DEVICE — пусто.

## 1. Целевая схема

| Категория | userType | Как проходит | Кто решает |
|---|---|---|---|
| Сотрудники и все остальные | `normal` | локальные права терминала (`doorRight` + `RightPlan`) — как сейчас | терминал |
| Будущие ученики (сейчас — только `3818077855`) | `visitor` | лицо → `employeeNo` → запрос Remote Verification → проход только при `success` | kpp-journal |

Настройка терминала (план): Remote Verification, Synchronous Listening, `remoteCheckUserTypeList=["visitor"]`,
`needDeviceCheck=true`, `offlineDevCheckOpenDoorEnabled=false`, `remoteCheckVerifyMode=6`, таймаут → отказ.

## 2. Ответы на вопросы

| # | Вопрос | Ответ | Статус |
|---|---|---|---|
| 1 | Можно ли сменить `userType` без потери лица и карты? | Документировано: редактирование персоны `PUT /ISAPI/AccessControl/UserInfo/Modify?format=json`, если `supportFunction` содержит `put` [FRT §10.15.2.5, с.123]; учётные данные удаляются **вместе с персоной** [с.125], при редактировании — не сказано. **Схемы тела Modify в нашем наборе документации нет** (USER_MANAGEMENT.md §2). Поэтому отправляем минимум `{employeeNo, userType}` и сверяем запись до/после (`numOfFace`, `numOfCard`, `doorRight`, `RightPlan`, `Valid`, ФИО-хэш …) | DOCUMENTED частично; NOT VERIFIED |
| 2 | Можно ли включить Remote Verification только для visitor? | Единственный механизм — `remoteCheckUserTypeList`. Есть **только в комментариях примеров** [с.126, 129, 132], нет в API Reference (caps/PUT/GET, с.423–428). «If absent or empty, all person types require remote verification». | DOCUMENTED частично; NOT VERIFIED |
| 3 | Останутся ли normal на локальной авторизации? | Если поле поддержано и работает — да (по примерам). Если прошивка **молча игнорирует** поле — проверка включится для **всех 2216** `normal`. Из документации гарантировать нельзя | NOT VERIFIED |
| 4 | Сохранит ли visitor опознание по лицу без самостоятельного права открытия? | Права `doorRight`/`RightPlan` **не снимаем**: при `needDeviceCheck=true` удалённая проверка идёт после локальной аутентификации [с.127], без локального права запроса к нам, вероятно, не будет. «Самостоятельное право» отключает Remote Verification: дверь управляется ответом платформы [с.125–126]. Обходы — см. §4 | DOCUMENTED; NOT VERIFIED |
| 5 | Нужны ли visitor-параметры, сроки, лимиты проходов? | Документация: «visitors have **temporary** permissions» [FRT §2.3.11, с.5]. В записи нашего терминала есть `maxOpenDoorTime: 0`, `openDoorTime: 0` (HW-выгрузка); в нашем наборе они встречаются только в capabilities асинхронного импорта [с.508] **без описания**. Возможно, для visitor это лимит открытий. `Valid` тестовой записи — до 2035-08-12 (HW). Мы ничего из этого не меняем; проверка — В-5 в VISITOR_PILOT_TESTS.md | NOT VERIFIED |
| 6 | Что при отключении kpp-journal? | visitor: «if no result is received within this time, the verification fails» [с.126, 132], `offlineDevCheckOpenDoorEnabled=false` → закрыто. normal: не ходит к нам → без изменений. Аварийная разблокировка — аппаратная, от ПО не зависит (ACCESS_CONTROL.md §8) | DOCUMENTED; NOT VERIFIED |
| 7 | Можно ли проверить и восстановить исходную конфигурацию, не затрагивая других? | Да по построению: Modify — по одной записи; `AcsCfg`/`httpHosts` — откат телом из снимка «до». Инструменты сохраняют снимки и проверяют откат. Неизвестно, сбрасывает ли `PUT AcsCfg` непереданные поля — сверка GET после PUT | IMPLEMENTED, TESTED (mock); NOT VERIFIED |

**Вывод:** поддержка visitor-only Remote Verification на нашей модели (DS-K1T341CM, V3.3.40 — со слов, не подтверждено
запросом) **не доказана**. Даже если `remoteCheckUserTypeList` окажется в capabilities, это не доказывает, что фильтр работает.
Неизменность работы `normal` на общем терминале **гарантировать нельзя** до проверок И-1…И-4 на изолированном стенде.
Поэтому на общем терминале Remote Verification **не включается**. Допустимо до стенда: read-only диагностика и (по отдельному
решению) смена `userType` только тестовой записи — она одна не включает удалённую проверку.

## 3. Что меняется

### Только запись `3818077855` (по отдельному подтверждению)

```http
PUT /ISAPI/AccessControl/UserInfo/Modify?format=json
{"UserInfo": {"employeeNo": "3818077855", "userType": "visitor"}}
```
Не отправляются: ФИО, `Valid`, `doorRight`, `RightPlan`, лицо, карта, пароль, `belongGroup` и т.д. Запись не удаляется и не создаётся заново.
Клиент kpp-journal **технически не может** отправить в Modify другие поля, другой `employeeNo` или тип кроме normal/visitor
(`client.check_operation`, тесты `test_user_write_gates`).

### Глобальные настройки терминала (только стенд; инженер СКУД вручную; по согласованию)

`PUT /ISAPI/AccessControl/AcsCfg?format=json` — **весь терминал**:

| Поле | Цель | Зачем | Источник |
|---|---|---|---|
| `remoteCheckDoorEnabled` | `true` | главный выключатель | с.424–428 |
| `checkChannelType` | `ISAPIListen` | терминал сам шлёт POST на наш хост | с.424–426 |
| `remoteCheckWithISAPIListen` | `sync` | решение в теле ответа | с.425, 428, 132 |
| `needDeviceCheck` | `true` | сначала локальное опознание → есть `employeeNo` | с.126–127 |
| `remoteCheckVerifyMode` | **`6`** (лицо или карта) | при `2` карта visitor проходит **локально в обход kpp-journal**; при `6` карта тоже идёт на проверку, а kpp-journal отклоняет карту (`unsupported_event`) | таблица с.127 |
| `remoteCheckTimeout` | `5` | ≤ 10 с; наш бюджет ответа 1,5 с | с.424, 428 |
| `offlineDevCheckOpenDoorEnabled` | `false` | нет связи → не открывать | с.126 |
| `remoteCheckUserTypeList` | `["visitor"]` | изоляция normal | только примеры с.126/129/132 |

`httpHosts` — добавить хост прослушивания `http://<IP kpp-journal>:8090/hikvision/listen/<key>` (по умолчанию слот один [с.128, 131]).

Точный список «текущее → целевое» и тело отката для конкретного терминала строит инструмент
`remote_check_plan` (только чтение, §6). Если в capabilities нет `remoteCheckUserTypeList`, `remoteCheckVerifyMode=6`,
`ISAPIListen`, или удалённая проверка уже включена / слот `httpHosts` занят — вердикт **STOP**.

## 4. Может ли visitor открыть проход в обход kpp-journal

| Путь | Закрывается | Статус |
|---|---|---|
| Лицо | Remote Verification для visitor | NOT VERIFIED |
| Карта (у записи `numOfCard=1`) | `remoteCheckVerifyMode=6` + DENY карты в kpp-journal | NOT VERIFIED (С-9) |
| PIN (`password` пустой, HW), отпечаток (`numOfFP=0`, HW), QR | нет учётных данных; QR — `QRCodeEnabled` не трогаем | HW (выгрузка) |
| Кнопка выхода, ручное открытие охраной, пожарный режим | **не закрывается и не должно** — штатные и аварийные пути | — |
| Нет ответа / таймаут | `offlineDevCheckOpenDoorEnabled=false` | NOT VERIFIED |

## 5. Перечень read-only запросов к действующему терминалу (выполнять ТОЛЬКО после вашего разрешения)

Терминал `192.168.4.49` (адрес из `export_hikvision_users.py`). По одному запросу, пауза 1 с, остановка при 401.

| # | Запрос | Зачем |
|---|---|---|
| 1 | `GET /ISAPI/System/deviceInfo` | модель, прошивка, дата прошивки |
| 2 | `GET /ISAPI/System/capabilities` | общие возможности |
| 3 | `GET /ISAPI/AccessControl/capabilities` | `isSupportRemoteCheck`, `isSupportAcsCfg` |
| 4 | `GET /ISAPI/AccessControl/AcsCfg/capabilities?format=json` | `remoteCheckUserTypeList`, `ISAPIListen`, `sync`, `remoteCheckVerifyMode @opt` |
| 5 | `GET /ISAPI/AccessControl/AcsCfg?format=json` | снимок «до» |
| 6 | `GET /ISAPI/AccessControl/remoteCheck/capabilities?format=json` | формат ответа |
| 7 | `GET /ISAPI/Event/notification/httpHosts/capabilities` | число слотов |
| 8 | `GET /ISAPI/Event/notification/httpHosts` | занят ли слот |
| 9 | `GET /ISAPI/AccessControl/AcsEvent/capabilities?format=json` | поиск журнала |
| 10 | `GET /ISAPI/AccessControl/AcsWorkStatus?format=json` | состояние двери |
| 11 | `GET /ISAPI/AccessControl/Door/param/1` | параметры двери (пароли вырезаются) |
| 12 | `GET /ISAPI/AccessControl/UserInfo/capabilities?format=json` | `supportFunction` (`put`), `userType @opt` |
| 13 | `GET /ISAPI/Security/capabilities` | политика блокировки входа |
| 14 | `POST /ISAPI/AccessControl/UserInfo/Search?format=json` с `EmployeeNoList:[{"employeeNo":"3818077855"}]`, `maxResults:1` | запись «до»; если терминал игнорирует фильтр — ответ отбрасывается |
| 15 | (опц.) `POST /ISAPI/AccessControl/AcsEvent?format=json` по `3818077855` за сутки, `picEnable:false` | какие события приходят при проходе |

Команды (PowerShell, из `backend`; логин/пароль — в переменных среды текущей сессии, не в файлах):
```powershell
$env:HIKVISION_MODE = "READ_ONLY"
$env:HIK_DIAG_USER = "<логин>"; $env:HIK_DIAG_PASSWORD = "<пароль>"
.\.venv\Scripts\python -m app.integrations.hikvision.diagnostics --host 192.168.4.49 --confirm-read-only --events   # 1–13, 15
.\.venv\Scripts\python -m app.integrations.hikvision.user_type --host 192.168.4.49 --confirm-network --to visitor   # 12, 14: DRY_RUN
.\.venv\Scripts\python -m app.integrations.hikvision.remote_check_plan --host 192.168.4.49 --confirm-network        # 3–5, 8: план, ничего не меняет
```

## 6. Инструменты (IMPLEMENTED, TESTED на mock)

| Инструмент | Что делает | Запись на терминал |
|---|---|---|
| `python -m app.integrations.hikvision.user_type` | capabilities → запись «до» → резервная копия (ФИО/пароль — хэш) → точный запрос → (с `--apply --confirm`) Modify → запись «после» → сверка всех полей; откат с `--backup` сверяется с исходной записью | только `UserInfo/Modify` `{employeeNo, userType}`; по умолчанию DRY_RUN |
| `python -m app.integrations.hikvision.remote_check_plan` | проверки поддержки, «текущее → целевое», тело отката, вердикт STOP / GO_STAND_ONLY | **нет** |
| `python -m app.integrations.hikvision.diagnostics` | чек-лист read-only | нет |
| `/pilot` → «Прочитать userType и AcsCfg» | то же чтение для зарегистрированного терминала, результат на экране | нет |

Условия реальной записи `userType` (все одновременно): `HIKVISION_MODE=PILOT`, `HIKVISION_USER_WRITE_ENABLED=1`,
ключ/адрес терминала в `HIKVISION_USER_WRITE_DEVICES`, `--confirm-network`, `--apply`, фраза `--confirm "3818077855:normal->visitor"`,
фактический тип совпадает с ожидаемым, capabilities подтверждают `put` и `visitor`, у записи есть лицо.
Право управлять проходом (`HIKVISION_CONTROL_*`) права на запись персон **не даёт** (тест).

Контролируемое изменение — [VISITOR_PILOT_TESTS.md](VISITOR_PILOT_TESTS.md) §3; откат — [VISITOR_ROLLBACK.md](VISITOR_ROLLBACK.md).

## 7. Изменения kpp-journal (IMPLEMENTED, TESTED)

* Событие хранит `userType` (`hik_events.user_type`); запись пилота — прочитанный с терминала тип (`hik_persons.terminal_user_type`).
* Decision Engine: запрос удалённой проверки от типа вне `HIKVISION_REMOTE_CHECK_USER_TYPES` (по умолчанию `visitor`) →
  **DENY `not_remote_check_type`** и тревога «Нарушение изоляции» на `/pilot`. Если терминал не прислал `userType` — используется
  только проверенно прочитанный тип, иначе DENY `user_type_unknown`. Все прежние проверки `decide_exit` выполняются.
* Решение привязано к событию (терминал + `serialNo` + время); тот же `serialNo` с другого терминала — отдельное событие;
  проход другого человека не засчитывается чужому решению; повтор — DENY без открытия.
* `/pilot`: userType тестовой записи, вердикт Remote Verification по терминалу, тревога изоляции, userType/serialNo в
  решениях и событиях, смена userType на виртуальном терминале (DRY_RUN → ввод фразы → применить).
* Миграция `0003` (только новые столбцы); режим PILOT и запись персон по умолчанию выключены.
