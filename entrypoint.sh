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

# Миграции
python manage.py migrate --noinput

# Сбор статики
python manage.py collectstatic --noinput

exec "$@"