#!/bin/sh
# Дамп раз в сутки, старше 30 дней — удаляется.
# Восстановление: gunzip -c backups/kpp_ДАТА.sql.gz | docker compose exec -T db psql -U kpp kpp
set -u
while true; do
  file="/backups/kpp_$(date +%Y-%m-%d_%H%M).sql.gz"
  if pg_dump -h db -U kpp kpp | gzip > "$file.tmp"; then
    mv "$file.tmp" "$file"
    echo "backup: $file"
  else
    rm -f "$file.tmp"
    echo "backup: ОШИБКА pg_dump" >&2
  fi
  find /backups -name 'kpp_*.sql.gz' -mtime +30 -delete
  sleep 86400
done
