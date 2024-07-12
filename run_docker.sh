#!/bin/bash

# Переменные для настройки контейнера
DOCKER_IMAGE="apostol-finance"
DOCKER_CONTAINER="finance-apostol"
GIT_REPO="https://github.com/Apostol-007/finance.git"
GIT_BRANCH="master"

# Проверяем, что Docker установлен и доступен
docker -v >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Ошибка: Docker не установлен или не доступен."
  exit 1
fi

# Удаляем старые контейнеры, если они существуют
docker-compose down >/dev/null 2>&1

# Подгружаем код из репозитория Git
git clone -b $GIT_BRANCH $GIT_REPO

cd finance

chmod +x start.sh

# Запускаем контейнеры с помощью docker-compose
docker-compose up -d

echo "Контейнеры запущены. Web доступен по адресу http://localhost:8000/"
