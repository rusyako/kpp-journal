"""Hikvision Adapter: терминал опознаёт человека, решение о выходе принимает kpp-journal.

Модули:
    settings     — режимы SIMULATION / READ_ONLY / PILOT и проверки «можно ли управлять»
    parsing      — разбор запросов терминала (multipart/form-data, JSON, XML) без фото и ФИО
    client       — ISAPI-клиент с HTTP Digest и белым списком операций
    mock_device  — виртуальный терминал для тестов и симуляции
    adapter      — приём запроса удалённой проверки → Decision Engine → ответ терминалу
    diagnostics  — read-only проверка реального терминала (python -m app.integrations.hikvision.diagnostics)

Источник всех форматов — docs/hikvision/ (FRT §10.16, §14.6.15).
"""
