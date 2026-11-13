# Пилот visitor: откат

Дата: 2026-11-13. Откат затрагивает только то, что менял пилот: запись `3818077855`, `AcsCfg` (поля удалённой проверки)
и добавленный `httpHosts`. Остальные пользователи не изменяются ни при пилоте, ни при откате.

> Выполняется инженером СКУД при посте охраны. Каждое изменение терминала — по отдельному подтверждению владельца оборудования.

## 0. Быстрая остановка (секунды, без доступа к терминалу)

`/pilot` → «Выключить пилот» или `HIKVISION_CONTROL_ENABLED=0` + перезапуск. Это **закрывает** проход для visitor (fail-closed),
но **не возвращает** терминал к локальной работе: если фильтр visitor не работает, normal тоже останутся закрыты. Поэтому
при тревоге изоляции или отказах normal — сразу §2 (отключить `remoteCheckDoorEnabled`).

## 1. Что должно быть сохранено ДО пилота

| Что | Откуда | Где |
|---|---|---|
| Запись `3818077855` (ФИО и пароль — только хэш) | `user_type` DRY_RUN | `device-snapshots/<key>/user-3818077855-<время>-before.json` (+ `hik_config_snapshots`, kind `user_before`) |
| `AcsCfg` целиком, `httpHosts` | `diagnostics` | `device-snapshots/<ip>-<время>/report.json` |
| Тело отката `AcsCfg` | `remote_check_plan` | вывод команды → `rollback_body` |

Без этих трёх снимков пилот не начинается.

## 2. Откат настроек терминала (если включалась удалённая проверка)

Порядок важен: сначала отключить удалённую проверку, чтобы normal гарантированно вернулись к локальной работе.

1. `PUT /ISAPI/AccessControl/AcsCfg?format=json` с телом `rollback_body` из `remote_check_plan` (минимум
   `{"AcsCfg": {"remoteCheckDoorEnabled": false}}`).
2. `GET /ISAPI/AccessControl/AcsCfg?format=json` → сравнить с `AcsCfg` из `report.json` «до». Расхождения — исправить.
   (Сбрасывает ли `PUT AcsCfg` непереданные поля — не описано; поэтому сверка обязательна.)
3. `httpHosts`: удалить/вернуть хост прослушивания к снимку «до»; `GET /ISAPI/Event/notification/httpHosts` = снимок.
4. Сотрудник normal проходит по лицу — открывается локально.

## 3. Откат записи visitor → normal

```powershell
cd backend
$env:HIKVISION_MODE = "PILOT"
$env:HIKVISION_USER_WRITE_ENABLED = "1"; $env:HIKVISION_USER_WRITE_DEVICES = "school-exit"
.\.venv\Scripts\python -m app.integrations.hikvision.user_type --device school-exit --confirm-network `
    --to normal --expect-from visitor `
    --backup device-snapshots\school-exit\user-3818077855-<время>-before.json `
    --apply --confirm "3818077855:visitor->normal"
$env:HIKVISION_USER_WRITE_ENABLED = "0"; $env:HIKVISION_MODE = "READ_ONLY"
```
Инструмент перечитывает запись и сравнивает **все** поля с резервной копией (`restore_mismatch` должен быть пуст):
`userType=normal`, `numOfFace`, `numOfCard`, `doorRight`, `RightPlan`, `Valid`, хэш ФИО и т.д.
Тестовый участник проходит по лицу — открывается локально, на `/pilot` новых решений нет.

## 4. Если что-то пошло не так

| Ситуация | Действие |
|---|---|
| После Modify изменились другие поля (`unexpected_changes`) | не продолжать пилот; вернуть значения вручную по резервной копии (через веб-интерфейс терминала/iVMS инженером СКУД); зафиксировать прошивку как «Modify заменяет запись» |
| Пропало лицо/карта (`numOfFace`/`numOfCard` уменьшились) | перерегистрация лица/карты тестового участника инженером СКУД (только его запись); пилот на этой прошивке — только через полный набор полей, отдельный план |
| `UserInfo/Search` не находит запись или возвращает чужие | остановиться; проверить запись в веб-интерфейсе терминала |
| Тревога изоляции / отказ normal | §2 немедленно (сначала `remoteCheckDoorEnabled=false`) |
| 401 при любом запросе | остановиться, не повторять (блокировка учётной записи после 5 ошибок на 30 мин) |

## 5. После отката

* `/pilot` → «Прочитать userType и AcsCfg» (в READ_ONLY): userType = `normal`, вердикт без включённой удалённой проверки.
* `HIKVISION_MODE=SIMULATION` (или READ_ONLY), `HIKVISION_CONTROL_ENABLED=0`, `HIKVISION_USER_WRITE_ENABLED=0`; приёмник остановлен.
* Итог — в «Журнал решений» `docs/hikvision/README.md`, результаты с пометкой **HW** — в `DEVICE_CAPABILITIES.md`.
