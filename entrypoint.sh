#!/bin/bash
set -e

# Ожидание PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "PostgreSQL started"

# Ожидание Redis
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 1
done
echo "Redis started"

# Применяем миграции
python manage.py migrate --noinput

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем команду, переданную в CMD
exec "$@"