# LMS System – платформа онлайн-обучения

## Запуск с помощью Docker

### Предварительные требования
- Установленный Docker и Docker Compose
- Созданный файл `.env` (см. `.env.example`)

### Инструкция

Клонировать репозиторий:
   git clone <repo-url>
   cd LMS_system

## CI/CD

При каждом push в ветку `main` запускаются:
- линтер `flake8`
- тесты Django
- сборка Docker-образа
- deploy на сервер через Docker Compose

## Deploy на production

Для ручного deploy используйте:

cd ~/lms_system
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d