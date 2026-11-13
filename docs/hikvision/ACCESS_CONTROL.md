# Двери, турникеты, реле, расписания

Источники — см. [README.md](README.md#обозначения-источников).
⚠ Любые `PUT`/`POST`/`DELETE` ниже меняют поведение действующего прохода — **запрещены без отдельного разрешения**.

## 1. Модель

Терминал распознавания лиц — это контроллер доступа с одной или несколькими «дверями» (`doorNo`). Турникет подключён к реле/выходу терминала
или к отдельному контроллеру — **как подключён школьный турникет, не известно** (аудит §11.4). События турникета (`Passing Event 0xda`,
`Reverse Passing 0x86`, `Passing Timed Out 0x89`, «Lane Controller …») приходят, только если контроллер полосы передаёт их терминалу.

## 2. Параметры двери [FRT §14.6.4, с.434–437]

`GET|PUT /ISAPI/AccessControl/Door/param/<doorID>`, `GET …/capabilities`:

| Поле | Смысл |
|---|---|
| `doorName` | имя |
| `openDuration` | время удержания открытым, 1–255 с |
| `magneticType`, `openButtonType`, `lockInputType` | `alwaysClose` / `alwaysOpen` (NC/NO) |
| `magneticAlarmTimeout` | тревога «дверь не закрыта», 0 = выкл |
| `enableDoorLock` | запирать при закрытии |
| `enableLeaderCard`, `leaderCardMode` | «первая карта» |
| `stressPassword`, `superPassword`, `unlockPassword` | пароли (Base64) |
| `useLocalController`, `localController*` | распределённый контроллер |
| `openButton` | кнопка выхода |
| `relayReverseEnabled`, `verificationPassOpenDoor` | без описания |

## 3. Статус [FRT §14.6.3.4–14.6.3.5, с.428–431]

`GET /ISAPI/AccessControl/AcsWorkStatus?format=json` (read-only):
`doorLockStatus` (реле: 0 normally close, 1 normally open, 2 short-circuit alarm, 3 broken-circuit alarm, 4 exception),
`doorStatus` (1 sleep, 2 remain unlocked, 3 remain locked, 4 normal/controlled), `magneticStatus`, `antiSneakStatus` (anti-passback),
`cardReaderOnlineStatus`, `cardReaderVerifyMode`, `netStatus`, `InterfaceStatusList`.

## 4. Удалённое управление дверью [FRT §14.6.14, с.517–519]

`PUT /ISAPI/AccessControl/RemoteControl/door/<doorID>` (`65535` = все двери), XML `RemoteControlDoor`:
`cmd` ∈ `open`, `close`, `alwaysOpen` (свободный проход), `alwaysClose` (заблокировано), `visitorCallLadder`, `householdCallLadder`, `resume`.
Доп. поля: `employeeNo`, `channelNo`, `controlType`, `personnelChannelGroupInfoList`.

**Для kpp-journal:** НЕ использовать как механизм выпуска (команда открывает проход тому, кто стоит рядом). `alwaysOpen`/`alwaysClose` —
опасны (эвакуация, блокировка). Отправка любых команд запрещена без разрешения. Событие «Door Remotely Open» `0x3/0x400` [ACET с.10].

## 5. Расписания

* Расписание статуса двери: `DoorStatusWeekPlanCfg` — `remainOpen`, `remainClosed`, `normal`, `sleep`, `invalid`, `induction`, `barrierFree` [с.422–423].
* Расписания прав персон: `UserRightPlanTemplate`, `UserRightWeekPlanCfg`, `UserRightHolidayGroupCfg`, `UserRightHolidayPlanCfg` [§10.18, с.137–142; API §14.6.9, с.492–501].
  На терминале используются шаблоны `planTemplateNo` 1, 21, 23, 24 и др. (HW, выгрузка) — их содержимое не выгружалось.
* Расписание режима аутентификации: §10.4 [с.66–71].

## 6. Глобальные параметры контроллера `AcsCfg` [FRT §14.6.3.1–14.6.3.3, с.423–428]

Помимо удалённой проверки (см. `REMOTE_VERIFICATION.md`), содержит: `voicePrompt`, `showPicture`, `showEmployeeNo`, `showName`,
`uploadCapPic`, `saveCapPic`, `uploadVerificationPic`, `QRCodeEnabled`, `thermal*`, `externalCardReaderEnabled`,
`combinationAuthenticationTimeout`, `fireAlarmInputType` (пример `alwaysOpen`) [с.428], `faceDuplicateCheckEnabled` и др.

⚠ `PUT AcsCfg` применяется к **устройству целиком**. Перед изменением обязательно: `GET AcsCfg` → сохранить снимок в репозитории/журнале →
изменить только нужные поля → `PUT` → `GET` и сравнить. Документация не говорит, сбрасываются ли поля, не переданные в `PUT` — **проверить на стенде**.

## 7. Anti-passback, мультиаутентификация

* Anti-passback: §10.1 [с.61–63], сброс правил §10.17 [с.136–137]. Состояние — `antiSneakStatus`.
* Multi-Factor Authentication: §10.13 [с.115–117].
Для пилота не трогать.

## 8. Пожарная безопасность

`fireAlarmInputType` в `AcsCfg`, события «Fire Relay Closed: Door Remains Open» `0x5/0x34`, «Lane Controller Fire Input Alarm» `0x424` [ACET].
Аварийная разблокировка должна оставаться аппаратной и не зависеть от kpp-journal (аудит §11.3). Удалённая проверка не должна влиять на неё —
**проверить на стенде** (пункт 14 в `REMOTE_VERIFICATION.md` §6).
