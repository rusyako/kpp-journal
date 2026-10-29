import os
from pathlib import Path
from zoneinfo import ZoneInfo

# Часовой пояс школы (UTC+5). Всё время выхода ставит сервер в этом поясе.
SCHOOL_TZ = ZoneInfo("Asia/Qyzylorda")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./kpp.db")

# Подпись cookie сессии. В продакшене обязательно задать своё значение.
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
SESSION_DAYS = int(os.environ.get("SESSION_DAYS", "30"))
# Cookie только по HTTPS; локально без TLS выключить: COOKIE_SECURE=0
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1") == "1"

# Адрес сайта снаружи — для кнопки Mini App и ссылок в сообщениях
PUBLIC_URL = os.environ.get("PUBLIC_URL", "http://localhost:8000").rstrip("/")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME", "")

# Отчёт за день (Ф-19)
REPORT_TIME = os.environ.get("REPORT_TIME", "16:50")
REPORT_EMAILS = [e.strip() for e in os.environ.get("REPORT_EMAILS", "").split(",") if e.strip()]
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)

SCHEDULER_ENABLED = os.environ.get("SCHEDULER_ENABLED", "1") == "1"

# Собранный React (frontend/dist); если папки нет — API работает без UI
STATIC_DIR = Path(os.environ.get("STATIC_DIR", Path(__file__).resolve().parents[2] / "frontend" / "dist"))

# Сколько совпадений показывать в поиске КПП (Ф-7)
SEARCH_LIMIT = 5
