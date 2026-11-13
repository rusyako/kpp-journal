"""Разбор запросов терминала.

Формат запроса удалённой проверки — FRT §10.16.3.2.3 / §10.16.4.2.3, с.130 и 133:
POST multipart/form-data, часть «AccessControllerEvent» (JSON) + часть «Picture» (JPEG).
Поля события — FRT §14.6.1.20, с.408–411. Фото и ФИО не сохраняем и не логируем.
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from xml.etree import ElementTree

from app.config import SCHOOL_TZ

# Event types, которые могут быть запросом удалённой проверки [FRT с.126, 131–132]
REMOTE_CHECK_EVENT_TYPES = {"AccessControllerEvent", "IDCardInfoEvent", "QRCodeEvent", "FaceTemperatureMeasurementEvent"}

# major 5 = «Other Events» (ACET с.16–23); minor в десятичном виде
MAJOR_OTHER = 5
MINOR_FACE_AUTH_OK = 75  # 0x4b Face Authentication Completed
MINOR_CATEGORIES = {
    218: "passage",  # 0xda Passing Event
    137: "passage_timeout",  # 0x89 Passing Timed Out
    134: "reverse_passage",  # 0x86 Reverse Passing
    21: "door",  # 0x15 Door Unlocked
    22: "door",  # 0x16 Door Locked
    25: "door",  # 0x19 Door Open (Contact)
    26: "door",  # 0x1a Door Closed (Contact)
    75: "auth_ok",
    76: "auth_failed",  # 0x4c Face Authentication Failed
    80: "auth_failed",  # 0x50 Face Recognition Failed
    6: "auth_failed",  # 0x06 No Permission
    7: "auth_failed",  # 0x07 Invalid Card Swiping Time Period
    8: "auth_failed",  # 0x08 Expired Card
    152: "auth_failed",  # 0x98 Employee ID Not Exists
}

# Персональные данные и биометрия: не сохраняем
_DROP_KEYS = re.compile(r"^(name|cardNo|pictureURL|visibleLightURL|thermalURL|filePath|FaceRect|faceRect|picData|.*[Pp]icture.*)$")

MAX_BODY = 5 * 1024 * 1024


class ParseError(ValueError):
    pass


@dataclass
class ParsedEvent:
    event_type: str
    category: str
    date_time_raw: str
    date_time: datetime | None
    major: int | None
    minor: int | None
    employee_no: str | None
    serial_no: int | None
    front_serial_no: int | None
    current_event: bool | None
    remote_check: bool
    sanitized: dict
    # userType из события (normal / visitor / blackList / administrators) [FRT с.410]; None — терминал не прислал
    user_type: str | None = None
    pictures_dropped: int = 0
    raw_digest: str = ""
    extra: dict = field(default_factory=dict)

    def dedup_key(self, device_key: str) -> str:
        """Ключ (терминал, serialNo, время): serialNo переполняется на 100000 (EVENTS.md §6)."""
        if self.serial_no is not None and self.date_time_raw:
            return f"{device_key}:{self.serial_no}:{self.date_time_raw}"[:200]
        return f"{device_key}:sha:{self.raw_digest}"[:200]


# ---------- Части multipart ----------


def _boundary(content_type: str) -> bytes:
    m = re.search(r'boundary="?([^";]+)"?', content_type, re.I)
    if not m:
        raise ParseError("multipart без boundary")
    return m.group(1).strip().encode()


def split_multipart(content_type: str, body: bytes) -> list[tuple[dict, bytes]]:
    """[(заголовки части в нижнем регистре, тело части)]. Понимает и CRLF, и LF."""
    delim = b"--" + _boundary(content_type)
    parts = []
    for chunk in body.split(delim)[1:]:
        if chunk.startswith(b"--"):
            break  # завершающий --boundary--
        chunk = chunk.lstrip(b"\r\n")
        sep = re.search(rb"\r?\n\r?\n", chunk)
        if not sep:
            continue
        head, data = chunk[: sep.start()], chunk[sep.end():]
        if data.endswith(b"\r\n"):
            data = data[:-2]
        elif data.endswith(b"\n"):
            data = data[:-1]
        headers = {}
        for line in re.split(rb"\r?\n", head):
            if b":" in line:
                k, v = line.split(b":", 1)
                headers[k.strip().decode("latin-1").lower()] = v.strip().decode("utf-8", "replace")
        parts.append((headers, data))
    return parts


def _part_name(headers: dict) -> str:
    m = re.search(r'name="?([^";]+)"?', headers.get("content-disposition", ""))
    return m.group(1) if m else ""


def _is_image(headers: dict) -> bool:
    ct = headers.get("content-type", "").lower()
    return ct.startswith("image/") or "filename=" in headers.get("content-disposition", "")


# ---------- XML → dict ----------


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1]


def xml_to_dict(elem: ElementTree.Element) -> dict | str:
    children = list(elem)
    if not children:
        return (elem.text or "").strip()
    result: dict = {}
    for child in children:
        key = _strip_ns(child.tag)
        value = xml_to_dict(child)
        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result


def parse_xml(data: bytes) -> dict:
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as e:
        raise ParseError(f"битый XML: {e}") from None
    return {_strip_ns(root.tag): xml_to_dict(root)}


# ---------- Нормализация ----------


def sanitize(value):
    if isinstance(value, dict):
        return {k: sanitize(v) for k, v in value.items() if not _DROP_KEYS.match(k)}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    return value


def _to_int(v) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _to_bool(v) -> bool | None:
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.lower() in ("true", "false"):
        return v.lower() == "true"
    return None


def parse_time(raw: str) -> datetime | None:
    """ISO 8601; без пояса считаем временем школы (FRT §4.2.4, с.16)."""
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SCHOOL_TZ)
    return dt.astimezone(SCHOOL_TZ)


def classify(event_type: str, major: int | None, minor: int | None, remote_check: bool, ace: dict) -> str:
    if remote_check:
        return "remote_check"
    if "remoteCheckResult" in ace:
        return "remote_check_result"
    if event_type.lower() == "heartbeat" or str(ace.get("eventState", "")).lower() == "heartbeat":
        return "heartbeat"
    if major == MAJOR_OTHER and minor in MINOR_CATEGORIES:
        return MINOR_CATEGORIES[minor]
    return "other"


def normalize(doc: dict, pictures_dropped: int = 0, raw_digest: str = "") -> ParsedEvent:
    """doc — корневой объект события (верхний уровень с eventType и вложенным AccessControllerEvent)."""
    if "EventNotificationAlert" in doc and isinstance(doc["EventNotificationAlert"], dict):
        doc = doc["EventNotificationAlert"]
    event_type = str(doc.get("eventType") or "")
    ace = doc.get(event_type) if event_type in doc else doc.get("AccessControllerEvent")
    if not isinstance(ace, dict):
        raise ParseError("в событии нет объекта AccessControllerEvent")
    if not event_type:
        event_type = "AccessControllerEvent"

    # employeeNoString приоритетнее employeeNo [FRT с.409]
    emp = ace.get("employeeNoString")
    if emp in (None, ""):
        emp = ace.get("employeeNo")
    employee_no = str(emp).strip() if emp not in (None, "") else None
    if employee_no is not None and len(employee_no) > 32:
        raise ParseError("employeeNo длиннее 32 символов")

    raw_time = str(doc.get("dateTime") or ace.get("time") or "")[:40]
    major, minor = _to_int(ace.get("majorEventType")), _to_int(ace.get("subEventType"))
    remote_check = _to_bool(ace.get("remoteCheck")) is True and event_type in REMOTE_CHECK_EVENT_TYPES
    user_type = ace.get("userType")
    user_type = str(user_type).strip()[:20] if user_type not in (None, "") else None
    return ParsedEvent(
        user_type=user_type,
        event_type=event_type,
        category=classify(event_type, major, minor, remote_check, ace),
        date_time_raw=raw_time,
        date_time=parse_time(raw_time),
        major=major,
        minor=minor,
        employee_no=employee_no,
        serial_no=_to_int(ace.get("serialNo")),
        front_serial_no=_to_int(ace.get("frontSerialNo")),
        current_event=_to_bool(ace.get("currentEvent")),
        remote_check=remote_check,
        sanitized=sanitize(doc),
        pictures_dropped=pictures_dropped,
        raw_digest=raw_digest,
    )


def parse_request(content_type: str, body: bytes) -> ParsedEvent:
    """Запрос терминала → событие. Картинки отбрасываются, не читаясь."""
    if len(body) > MAX_BODY:
        raise ParseError("слишком большой запрос")
    ct = (content_type or "").lower()
    pictures = 0
    data: bytes | None = None
    data_ct = ""
    if ct.startswith("multipart/"):
        for headers, part in split_multipart(content_type, body):
            if _is_image(headers):
                pictures += 1
                continue
            if data is None:
                data, data_ct = part, headers.get("content-type", "").lower()
        if data is None:
            raise ParseError("в multipart нет части с событием")
    else:
        data, data_ct = body, ct

    digest = hashlib.sha256(data).hexdigest()[:32]
    stripped = data.lstrip()
    if "xml" in data_ct or stripped.startswith(b"<"):
        doc = parse_xml(stripped)
    else:
        try:
            doc = json.loads(stripped.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ParseError(f"битый JSON: {e}") from None
    if not isinstance(doc, dict):
        raise ParseError("событие — не объект")
    return normalize(doc, pictures, digest)


def peek_serial(content_type: str, body: bytes) -> int | None:
    """Быстро достать serialNo для ответа «failed», если основной разбор не успел или упал."""
    try:
        return parse_request(content_type, body).serial_no
    except Exception:
        m = re.search(rb'"serialNo"\s*:\s*(\d+)', body[:20000])
        return int(m.group(1)) if m else None
