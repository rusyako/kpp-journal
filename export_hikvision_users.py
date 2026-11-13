
import csv
import json
import os
import time
import uuid
from pathlib import Path
from getpass import getpass
from xml.etree import ElementTree

import requests
from requests.auth import HTTPDigestAuth


# ==========================================
# НАСТРОЙКИ
# ==========================================

DEVICE_IP = "192.168.4.49"
BASE_URL = f"http://{DEVICE_IP}"

OUTPUT_DIR = Path(r"C:\Hikvision-Export")

PAGE_SIZE = 30
MAX_PAGES = 1000

# Каждая страница — новая HTTP-сессия
NEW_SESSION_EVERY_PAGE = True

# Пауза между запросами
DELAY_BETWEEN_PAGES = 5

TIMEOUT = (10, 60)

API_URL = (
    f"{BASE_URL}/ISAPI/AccessControl/"
    "UserInfo/Search?format=json"
)

PARTIAL_PATH = OUTPUT_DIR / "hikvision_users.partial.json"
JSON_PATH = OUTPUT_DIR / "hikvision_users.json"
CSV_PATH = OUTPUT_DIR / "hikvision_users.csv"


# ==========================================
# НОВАЯ АВТОРИЗАЦИЯ
# ==========================================

def create_session(username, password):
    session = requests.Session()

    # Новый объект Digest Authentication
    session.auth = HTTPDigestAuth(
        username,
        password
    )

    session.headers.update({
        "Accept": "application/json",
        "Connection": "close"
    })

    return session


# ==========================================
# СОХРАНЕНИЕ JSON
# ==========================================

def save_json(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = path.with_name(
        path.name + ".tmp"
    )

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temp_path, path)


# ==========================================
# ЗАГРУЗКА СОХРАНЁННОГО ПРОГРЕССА
# ==========================================

def load_state():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not PARTIAL_PATH.exists():
        return {
            "version": 1,
            "device_ip": DEVICE_IP,
            "search_id": str(uuid.uuid4()),
            "total": None,
            "users": []
        }

    print("\nНайдена незавершённая выгрузка.")

    with open(
        PARTIAL_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        state = json.load(f)

    if state.get("version") != 1:
        raise RuntimeError(
            "Несовместимая версия файла прогресса."
        )

    if state.get("device_ip") != DEVICE_IP:
        raise RuntimeError(
            "Файл относится к другому терминалу."
        )

    if not state.get("search_id"):
        raise RuntimeError(
            "Отсутствует search_id."
        )

    users = state.get("users")

    if not isinstance(users, list):
        raise RuntimeError(
            "Некорректный формат пользователей."
        )

    ids = []

    for user in users:
        if not isinstance(user, dict):
            raise RuntimeError(
                "Некорректная запись пользователя."
            )

        employee_id = str(
            user.get("employeeNo", "")
        ).strip()

        if not employee_id:
            raise RuntimeError(
                "Пользователь без employeeNo."
            )

        ids.append(employee_id)

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            "Обнаружены дубликаты employeeNo."
        )

    print(
        f"Уже сохранено пользователей: {len(users)}"
    )

    return state


# ==========================================
# ДИАГНОСТИКА HTTP 401
# ==========================================

def describe_401(response):

    print("\n========== HTTP 401 ==========")
    print("Терминал отклонил авторизацию.")

    challenge = response.headers.get(
        "WWW-Authenticate", ""
    )

    if challenge:
        print(
            "Authentication scheme:",
            challenge.split(" ", 1)[0]
        )
    else:
        print(
            "WWW-Authenticate: отсутствует"
        )

    print(
        "Authorization sent:",
        bool(
            response.request.headers.get(
                "Authorization"
            )
        )
    )

    try:
        root = ElementTree.fromstring(
            response.content
        )

        for key in (
            "statusValue",
            "statusString",
            "lockStatus",
            "unlockTime",
            "retryLoginTime"
        ):
            value = root.findtext(
                f".//{{*}}{key}"
            )

            if value is not None:
                print(f"{key}: {value}")

    except ElementTree.ParseError:
        pass

    print(
        "Повторная авторизация после ошибки "
        "не выполняется."
    )
    print("===============================")


# ==========================================
# ПОЛУЧЕНИЕ СТРАНИЦЫ
# ==========================================

def get_page(username, password, search_id, position):

    payload = {
        "UserInfoSearchCond": {
            "searchID": search_id,
            "searchResultPosition": position,
            "maxResults": PAGE_SIZE
        }
    }

    # Каждый запрос получает новую сессию
    # и новый экземпляр HTTPDigestAuth.

    with create_session(
        username,
        password
    ) as session:

        response = session.post(
            API_URL,
            json=payload,
            timeout=TIMEOUT
        )

        if response.status_code == 401:
            describe_401(response)

            raise RuntimeError(
                "HTTP 401. Выгрузка остановлена."
            )

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError(
                "Терминал вернул не JSON."
            )

    result = data.get("UserInfoSearch")

    if not isinstance(result, dict):
        raise RuntimeError(
            "Отсутствует объект UserInfoSearch."
        )

    batch = result.get("UserInfo") or []

    if isinstance(batch, dict):
        batch = [batch]

    if not isinstance(batch, list):
        raise RuntimeError(
            "Некорректный формат UserInfo."
        )

    count = result.get("numOfMatches")

    if count is not None:
        if int(count) != len(batch):
            raise RuntimeError(
                "numOfMatches не совпадает "
                "с количеством записей."
            )

    return result, batch


# ==========================================
# ПРОВЕРКА ОБЩЕГО КОЛИЧЕСТВА
# ==========================================


def check_total(state, result):

    reported = result.get("totalMatches")

    if reported is None:
        raise RuntimeError(
            "Терминал не вернул totalMatches."
        )

    reported = int(reported)

    if state["total"] is None:
        state["total"] = reported
        print(f"Всего пользователей: {reported}")
        return

    previous = int(state["total"])

    if reported != previous:
        print(
            f"\n[WARNING] Количество пользователей "
            f"изменилось: {previous} -> {reported}"
        )

        print(
            "Продолжаем выгрузку, но итоговый "
            "список потребуется проверить повторно."
        )

        state["total"] = reported


# ==========================================
# ПРОВЕРКА СОХРАНЁННЫХ ДАННЫХ
# ==========================================

def verify_resume(username, password, state):

    users = state["users"]

    if not users:
        return

    start = max(
        0,
        len(users) - PAGE_SIZE
    )

    print(
        "\nПроверка сохранённой страницы "
        f"с позиции {start}..."
    )

    result, batch = get_page(
        username,
        password,
        state["search_id"],
        start
    )

    check_total(state, result)

    saved_batch = users[
        start:start + len(batch)
    ]

    if (
        len(batch) < len(users) - start
        or batch != saved_batch
    ):
        raise RuntimeError(
            "Сохранённые данные больше не совпадают "
            "с терминалом. Необходимо начать "
            "новую полную выгрузку."
        )

    print("[OK] Данные совпадают.")

    time.sleep(DELAY_BETWEEN_PAGES)


# ==========================================
# ОСНОВНАЯ ВЫГРУЗКА
# ==========================================

def export_users(username, password):

    state = load_state()

    users = state["users"]
    position = len(users)

    seen_ids = {
        str(u["employeeNo"]).strip()
        for u in users
    }

    print(
        f"\nПодключаемся к терминалу {DEVICE_IP}..."
    )

    print(
        "Режим: новая HTTP-сессия на каждую страницу."
    )

    print(
        "Операции только чтения."
    )

    # Проверка перед продолжением

    if position:
        verify_resume(
            username,
            password,
            state
        )

    if (
        state["total"] is not None
        and position == int(state["total"])
    ):
        print("Все записи уже получены.")
        return users

    for page in range(1, MAX_PAGES + 1):

        print(
            f"\nЗапрос страницы {page}, "
            f"позиция {position}..."
        )

        # get_page самостоятельно открывает
        # и закрывает HTTP-сессию.

        result, batch = get_page(
            username,
            password,
            state["search_id"],
            position
        )

        check_total(state, result)

        total = int(state["total"])

        status = str(
            result.get("responseStatusStrg", "")
        ).strip().upper().replace(" ", "_")

        if not batch:

            if total == 0 and position == 0:
                break

            if position == total:
                break

            raise RuntimeError(
                f"Получена пустая страница: "
                f"{position}/{total}"
            )

        # Проверяем страницу целиком
        # до добавления в основной список.

        batch_ids = []

        for user in batch:

            if not isinstance(user, dict):
                raise RuntimeError(
                    "Некорректная запись пользователя."
                )

            employee_id = str(
                user.get("employeeNo", "")
            ).strip()

            if not employee_id:
                raise RuntimeError(
                    "Пользователь без employeeNo."
                )

            if employee_id in seen_ids:
                raise RuntimeError(
                    f"Дубликат employeeNo: {employee_id}"
                )

            if employee_id in batch_ids:
                raise RuntimeError(
                    f"Дубликат внутри страницы: "
                    f"{employee_id}"
                )

            batch_ids.append(employee_id)

        if position + len(batch) > total:
            raise RuntimeError(
                "Количество записей превышает totalMatches."
            )

        # Проверка статуса перед сохранением.

        new_position = position + len(batch)

        if status == "OK" and new_position != total:
            raise RuntimeError(
                "Терминал завершил поиск раньше времени."
            )

        if status not in ("MORE", "OK"):
            raise RuntimeError(
                f"Неожиданный статус: {status}"
            )

        # Страница проверена.
        # Добавляем и сохраняем её.

        users.extend(batch)
        seen_ids.update(batch_ids)

        position = len(users)

        save_json(
            PARTIAL_PATH,
            state
        )

        print(
            f"[OK] +{len(batch)} пользователей"
        )

        print(
            f"Прогресс: {position}/{total}"
        )

        print(
            f"Статус: {status}"
        )

        if position == total:
            print(
                "\nПолучены все пользователи."
            )
            break

        print(
            f"Пауза {DELAY_BETWEEN_PAGES} сек."
        )

        time.sleep(
            DELAY_BETWEEN_PAGES
        )

    else:
        raise RuntimeError(
            "Превышено максимальное количество страниц."
        )

    if (
        state["total"] is None
        or position != int(state["total"])
    ):
        raise RuntimeError(
            f"Неполная выгрузка: "
            f"{position}/{state['total']}"
        )

    return users


# ==========================================
# СОХРАНЕНИЕ CSV И JSON
# ==========================================

def write_exports(users):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    save_json(
        JSON_PATH,
        users
    )

    temp_csv = CSV_PATH.with_name(
        CSV_PATH.name + ".tmp"
    )

    try:

        with open(
            temp_csv,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as f:

            writer = csv.writer(
                f,
                delimiter=";"
            )

            writer.writerow([
                "employeeNo",
                "name",
                "userType",
                "beginTime",
                "endTime"
            ])

            for user in users:

                valid = user.get("Valid") or {}

                writer.writerow([
                    user.get("employeeNo", ""),
                    user.get("name", ""),
                    user.get("userType", ""),
                    valid.get("beginTime", ""),
                    valid.get("endTime", "")
                ])

        os.replace(
            temp_csv,
            CSV_PATH
        )

    finally:
        if temp_csv.exists():
            temp_csv.unlink()

    # Удаляем checkpoint только после
    # успешного сохранения итоговых файлов.

    PARTIAL_PATH.unlink(missing_ok=True)


# ==========================================
# MAIN
# ==========================================

def main():

    username = (
        input("Логин терминала [admin]: ").strip()
        or "admin"
    )

    password = getpass(
        "Пароль терминала: "
    )

    users = export_users(
        username,
        password
    )

    write_exports(users)

    print("\n================================")
    print("ВЫГРУЗКА УСПЕШНО ЗАВЕРШЕНА")
    print("================================")

    print(
        f"Всего пользователей: {len(users)}"
    )

    print("CSV:", CSV_PATH)
    print("JSON:", JSON_PATH)


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print(
            "\nОстановлено пользователем. "
            "Уже полученные страницы сохранены."
        )

    except (
        requests.RequestException,
        RuntimeError,
        ValueError,
        OSError
    ) as error:

        print(f"\nОшибка: {error}")

        print(
            "Сохранённый прогресс:",
            PARTIAL_PATH
        )

        raise SystemExit(1)
