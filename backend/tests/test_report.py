import io
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from openpyxl import load_workbook

from app.main import app
from app.services.report import build_report, render_xlsx
from tests.conftest import login, student_id


@pytest.mark.parametrize("username,status", [(None, 401), ("kpp", 403), ("kotiki", 403), ("director", 200), ("admin", 200)])
def test_xlsx_roles(db, username, status):
    client = login(username) if username else TestClient(app)
    assert client.get("/api/reports/2026-10-29/xlsx").status_code == status


def test_xlsx_selected_date(db, guard, advisor, admin, now):
    ids = {name: student_id(db, name) for name in (
        "Ким Илья", "Ким Ирина", "Гарамов Ислам", "Ахметов Арман", "Ахметова Дана",
    )}
    advisor.put(f"/api/advisor/students/{ids['Ким Илья']}/permission", json={"time": "15:00", "reason": "кружок"})
    advisor.put(f"/api/advisor/students/{ids['Ким Ирина']}/permission", json={"time": "13:00"})
    advisor.put(f"/api/advisor/students/{ids['Гарамов Ислам']}/permission", json={"time": "16:00"})
    for name in ("Ким Илья", "Ким Ирина", "Ахметов Арман", "Ахметова Дана"):
        assert guard.post("/api/exits", json={"student_id": ids[name]}).status_code == 200
    guard.post(f"/api/exits/{ids['Ахметова Дана']}/cancel")
    selected = now.value.date()
    expected = build_report(db, selected)
    now.value += timedelta(days=1)
    guard.post("/api/exits", json={"student_id": ids['Гарамов Ислам']})

    response = admin.get(f"/api/reports/{selected}/xlsx")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert response.headers["content-disposition"] == f'attachment; filename="otchet_{selected}.xlsx"'
    assert response.headers["cache-control"] == "no-store"
    wb = load_workbook(io.BytesIO(response.content))
    assert wb.sheetnames == ["Сводка", "Подробности"]
    summary, details = wb.worksheets
    assert summary["A1"].value == "Отчёт КПП за 29.10.2026"
    assert summary["B2"].value == selected.isoformat()
    assert [summary.cell(i, 2).value for i in range(4, 9)] == list(expected["summary"].values())
    assert [summary.cell(i, 1).value for i in range(4, 9)][-1] == "С разрешением, но не вышли"
    fields = ("full_name", "class_name", "advisory", "allowed_time", "exit_time", "reason")
    expected_rows = [
        (group["title"], *(row[field] or None for field in fields))
        for group in expected["lists"] for row in group["rows"]
    ]
    assert len(expected_rows) == 5
    assert list(details.iter_rows(min_row=4, values_only=True)) == expected_rows
    assert details.auto_filter.ref == "A3:G8"
    for sheet in wb:
        assert sheet.freeze_panes == "A4"
        assert sheet["A3"].font.bold
        assert sheet["A4"].alignment.wrap_text
        assert sheet.column_dimensions["A"].width >= 40


def test_xlsx_no_events(db, admin):
    response = admin.get("/api/reports/2026-10-28/xlsx")
    assert response.status_code == 200
    wb = load_workbook(io.BytesIO(response.content))
    summary, details = wb.worksheets
    assert summary["B2"].value == "2026-10-28"
    assert [summary.cell(i, 2).value for i in range(4, 9)] == [6, 0, 0, 0, 0]
    assert details.max_row == 3
    assert details.auto_filter.ref == "A3:G3"
    assert details["A3"].value == "Категория"
    assert details["G3"].value == "Причина"


@pytest.mark.parametrize("prefix", ["=", "+", "-", "@"])
def test_xlsx_literal_text_and_xml_characters(db, prefix):
    report = build_report(db, date(2026, 10, 29))
    unsafe = prefix + 'HYPERLINK("https://example.com","test")\x00\x08\x0b\x0c\x1f\ud800\ufffe\uffff\t\nтекст'
    clean = prefix + 'HYPERLINK("https://example.com","test")\t\nтекст'
    report["date"] = unsafe
    report["date_label"] = unsafe
    fields = ("full_name", "class_name", "advisory", "allowed_time", "exit_time", "reason")
    report["lists"] = [{"key": "early", "title": unsafe, "rows": [dict.fromkeys(fields, unsafe)]}]
    wb = load_workbook(io.BytesIO(render_xlsx(report)), data_only=False)
    for sheet in wb:
        assert sheet["A1"].value == f"Отчёт КПП за {clean}"
        assert sheet["B2"].value == clean
        assert sheet["B2"].data_type == "s"
    for cell in wb["Подробности"][4]:
        assert cell.value == clean
        assert cell.data_type == "s"
