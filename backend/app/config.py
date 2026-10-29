import os
from zoneinfo import ZoneInfo

# Часовой пояс школы (UTC+5). Всё время выхода ставит сервер в этом поясе.
SCHOOL_TZ = ZoneInfo("Asia/Qyzylorda")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./kpp.db")

# Сколько совпадений показывать в поиске КПП (Ф-7)
SEARCH_LIMIT = 5
