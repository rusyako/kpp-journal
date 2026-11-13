# Пилот visitor: автоматические тесты и физическая процедура

Дата: 2026-11-13. Статусы: **TESTED** — автотест на виртуальном терминале · **VERIFIED ON DEVICE** · **NOT VERIFIED**.

> Виртуальный терминал воспроизводит поведение **по документации**. Сценарии A, I, J, K на реальном оборудовании
> автотестами не подтверждаются — для них нужна физическая проверка (§3).

## 1. Автоматические тесты

Запуск: `cd backend; .\.venv\Scripts\python -m pytest -q` — итог 2026-11-13: **160 passed** (из них 26 в `tests/test_visitor.py`).

| Сценарий | Тест (`tests/test_visitor.py`) | TESTED | VERIFIED ON DEVICE |
|---|---|---|---|
| A. normal — прежняя локальная политика, kpp-journal решений не принимает | `test_a_normal_users_stay_local` | ✅ | ❌ |
| B. visitor без разрешения — DENY | `test_b_visitor_without_permission_deny` | ✅ | ❌ |
| C. visitor с разрешением — ALLOW, `serialNo` совпадает | `test_c_visitor_with_permission_allow` | ✅ | ❌ |
| D. visitor раньше окна — DENY | `test_d_visitor_too_early_deny` | ✅ | ❌ |
| E. разрешение отменено — DENY | `test_e_visitor_revoked_deny` | ✅ | ❌ |
| F. сервер недоступен — visitor закрыт, normal не затронут | `test_f_server_down_visitor_closed_normal_unaffected` | ✅ | ❌ |
| G. тот же `serialNo` — без нового открытия; привязка к терминалу; чужой проход не засчитан | `test_g_same_serial_no_reopen_and_device_binding`, `test_g_passage_of_other_person_not_linked` | ✅ | ❌ |
| H. неизвестный `employeeNo` — DENY / локальный отказ терминала | `test_h_unknown_employee` | ✅ | ❌ |
| I. смена userType сохраняет лицо, карту, права; DRY_RUN ничего не шлёт; «плохая прошивка» распознаётся | `test_i_dry_run_sends_nothing`, `test_i_change_keeps_face_card_and_rights`, `test_i_bad_firmware_resetting_fields_is_detected` | ✅ (двойник) | ❌ |
| J. откат: снова normal, запись совпадает с резервной копией, проход локальный | `test_j_rollback_restores_original` | ✅ (двойник) | ❌ |
| K. visitor-only не меняет normal; негатив: прошивка игнорирует список → тревога изоляции | `test_k_visitor_only_config_does_not_change_normal`, `test_normal_remote_request_is_isolation_violation` | ✅ | ❌ |
| Карта visitor не обходит проверку | `test_visitor_card_does_not_bypass` | ✅ | ❌ |
| Нет `userType` в событии → только проверенно прочитанный тип | `test_event_without_user_type_uses_verified_terminal_type` | ✅ | ❌ |
| Инструмент: другой `employeeNo`, нет/неверная фраза, тип вне normal/visitor, неожиданный исходный тип — отказ | `test_tool_refuses_other_employee_and_bad_confirm` | ✅ | — |
| Инструмент: capabilities без `put`; терминал игнорирует `EmployeeNoList` — стоп, чужие данные отброшены | `test_tool_stops_when_capabilities_do_not_confirm` | ✅ | ❌ |
| Права записи: только PILOT + `USER_WRITE_ENABLED` + терминал в списке; только поля `employeeNo`,`userType` | `test_user_write_gates` | ✅ | — |
| План AcsCfg: только GET; STOP без `remoteCheckUserTypeList`, при уже включённой проверке, при занятом `httpHosts` | `test_plan_go_for_stand_only`, `test_plan_stops` | ✅ | ❌ |
| API `/pilot`: чтение, DRY_RUN/применение на виртуальном терминале, запрет вне SIMULATION | `test_refresh_and_simulated_user_type_via_api` | ✅ | — |
| CLI DRY_RUN; без `--confirm-network` в сеть не идёт | `test_cli_dry_run_on_mock` | ✅ | — |

Прежние сценарии MVP (A–I в `test_release.py`, приёмник, таймауты) — без изменений, проходят.

## 2. Что проверяется только на оборудовании

| # | Проверка | Почему не автотест |
|---|---|---|
| В-1 | Модель/прошивка; есть ли в capabilities `put`, `visitor`, `remoteCheckUserTypeList`, `remoteCheckVerifyMode=6`, `sync` | нужен ответ реального терминала |
| В-2 | Modify `{employeeNo, userType}` не сбрасывает другие поля; `numOfFace`/`numOfCard` не меняются | поведение прошивки (схемы нет в документации) |
| В-3 | visitor по-прежнему опознаётся по лицу; в событии приходит `userType: visitor` | — |
| В-4 | `remoteCheckUserTypeList=["visitor"]` реально изолирует normal (И-2…И-4 из PILOT_TEST_PLAN.md §6), в т.ч. после перезагрузки | главный риск: «ignored → all types» |
| В-5 | visitor: нет ли лимита проходов (`maxOpenDoorTime`/`openDoorTime`) или ограничения срока, отличных от normal; ≥ 5 проходов подряд с ALLOW | семантика не описана |
| В-6 | Нет ответа / таймаут / сеть → закрыто для visitor, normal без изменений | — |
| В-7 | Карта visitor при `remoteCheckVerifyMode=6` идёт на проверку (и получает DENY) | — |
| В-8 | Аварийная разблокировка и пожарный вход работают независимо | — |
| В-9 | Откат возвращает запись и `AcsCfg` в точности к снимку «до» | — |

## 3. Физическая процедура

**Условия:** пост охраны и специалист СКУД на месте; штатные пути эвакуации открыты; вне учебного времени;
отдельное подтверждение владельца оборудования перед **каждым** шагом с 🔒. Шаги 6–11 — **только на изолированном стенде**,
пока В-4 не подтверждён на стенде (см. VISITOR_REMOTE_VERIFICATION_PLAN.md §2).

| Шаг | Действие | Команда / как | Ожидание |
|---|---|---|---|
| 1 🔒 | Подтвердить модель и прошивку | `diagnostics --host <IP> --confirm-read-only` | отчёт в `device-snapshots/`; В-1 |
| 2 🔒 | Сохранить исходную конфигурацию | отчёт шага 1 (`AcsCfg`, `httpHosts`, `Door/param`) + `remote_check_plan --host <IP> --confirm-network` | снимок «до», тело отката |
| 3 🔒 | Лицо и карта у тестовой записи | `user_type --host <IP> --confirm-network --to visitor` (DRY_RUN) | `numOfFace=1`, `numOfCard=1`, резервная копия записи |
| 4 | Остальные normal не затронуты | сотрудник-доброволец (normal) проходит по лицу до любых изменений; записать время и результат | проход открыт |
| 5 🔒 | normal → visitor (только запись `3818077855`) | см. §4 ниже | инструмент: «OK — изменился только userType»; В-2 |
| 5a | Поведение visitor **без** Remote Verification | тестовый участник проходит по лицу | зафиксировать (В-5: проходит ли visitor локально так же) |
| 6 🔒 | Visitor-only Remote Verification (только если `remote_check_plan` = GO_STAND_ONLY) | инженер СКУД: `httpHosts` + `PUT AcsCfg` по телу из плана; затем `GET AcsCfg` = цель; kpp-journal: `pilot-device`, приёмник, `HIKVISION_MODE=PILOT`, `HIKVISION_CONTROL_ENABLED=1`, `HIKVISION_CONTROL_DEVICES=<key>`, «Включить пилот» | сотрудник normal снова проходит **сразу и без запроса** к kpp-journal (на `/pilot` нет решений, нет тревоги изоляции) — В-4 |
| 7 | Распознавание без разрешения | тестовый участник у терминала | `/pilot`: запрос с `userType=visitor`, DENY `no_permission`; **турникет закрыт** |
| 8 | Создать тестовое разрешение | `/pilot` → окно 15 мин, одноразовое | статус «действует» |
| 9 | Повторное распознавание | тестовый участник | ALLOW, ответ `success`, турникет открыт; проход подтверждён (событие 0xda или вручную) |
| 10 | Отменить разрешение (или повторить после использования) | `/pilot` → «Отменить» | DENY `permission_revoked` / `permission_used`; закрыто |
| 11 | Потеря связи | остановить приёмник; затем отключить сеть сервера | visitor закрыт; сотрудник normal проходит; В-6 |
| 11a | Карта тестовой записи | приложить карту | на проверку → DENY; закрыто (В-7) |
| 11b | Аварийная разблокировка | по регламенту охраны | открыто независимо от ПО (В-8) |
| 12 🔒 | Вернуть исходное (если пилот завершается) | [VISITOR_ROLLBACK.md](VISITOR_ROLLBACK.md) | запись и `AcsCfg` = снимок «до» (В-9) |

**Немедленная остановка и откат:** тревога «Нарушение изоляции» на `/pilot`; любой отказ прохода normal-пользователю;
открытие турникета при DENY; систематическая задержка > 2 с; неожиданные изменения в `GET AcsCfg` или записи пользователя.

## 4. Контролируемое изменение normal → visitor (после вашего подтверждения)

```powershell
cd backend
# 1) зарегистрировать терминал в kpp-journal (на терминал ничего не отправляется)
.\.venv\Scripts\python -m app.cli pilot-device school-exit --host <IP> --allowed-ips <IP> --credentials-env SCHOOL
$env:HIK_SCHOOL_USER = "<логин>"; $env:HIK_SCHOOL_PASSWORD = "<пароль>"

# 2) DRY_RUN — читает capabilities и запись, сохраняет резервную копию, показывает запрос
$env:HIKVISION_MODE = "READ_ONLY"
.\.venv\Scripts\python -m app.integrations.hikvision.user_type --device school-exit --confirm-network --to visitor --expect-from normal

# 3) запись — только после вашего «да» на конкретный запрос из шага 2
$env:HIKVISION_MODE = "PILOT"
$env:HIKVISION_USER_WRITE_ENABLED = "1"; $env:HIKVISION_USER_WRITE_DEVICES = "school-exit"
.\.venv\Scripts\python -m app.integrations.hikvision.user_type --device school-exit --confirm-network --to visitor --expect-from normal --apply --confirm "3818077855:normal->visitor"

# 4) сразу выключить запись
$env:HIKVISION_USER_WRITE_ENABLED = "0"; $env:HIKVISION_MODE = "READ_ONLY"
```
Инструмент сам перечитает запись и сверит все поля. При любой проблеме он печатает готовую команду отката.
`HIKVISION_CONTROL_*` для смены userType не нужны и включаться не должны.
