#!/bin/sh
# Дамп раз в сутки, старше 30 дней — удаляется.
# Восстановление: gunzip -c backups/kpp_ДАТА.sql.gz | docker compose exec -T db psql -U kpp kpp
set -u
while true; do
  file="/backups/kpp_$(date +%Y-%m-%d_%H%M).sql.gz"
  # pg_dump сам сжимает (-Z), без конвейера «| gzip»: в конвейере ошибка pg_dump терялась
  # и получался пустой «успешный» архив. Проверяем и код pg_dump, и целостность архива.
  if pg_dump -h db -U kpp -Z 6 -f "$file.tmp" kpp \
     && gzip -t "$file.tmp" \
     && gunzip -c "$file.tmp" | tail -n 5 | grep -q "PostgreSQL database dump complete"; then
    mv "$file.tmp" "$file"
    echo "backup: $file"
  else
    rm -f "$file.tmp"
    echo "backup: ОШИБКА — копия не создана" >&2
  fi
  find /backups -name 'kpp_*.sql.gz' -mtime +30 -delete
  sleep 86400
done
