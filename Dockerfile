# Один образ: API + собранный React. Бот запускается из него же другой командой.

FROM node:20-slim AS web
WORKDIR /src/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY shared/ /src/shared/
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STATIC_DIR=/app/static
WORKDIR /app
COPY backend/pyproject.toml ./
COPY backend/app ./app
RUN pip install --no-cache-dir . && useradd --system --uid 1000 kpp
COPY backend/alembic.ini ./
COPY backend/alembic ./alembic
COPY --from=web /src/frontend/dist ./static
USER kpp
EXPOSE 8000
# Один воркер: в нём же работает расписание отчёта
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'"]
