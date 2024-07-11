#!/bin/bash

# Переменные для настройки контейнера
DOCKER_IMAGE="apostol-finance"
DOCKER_CONTAINER="finance-container"
GIT_REPO="git@github.com:Apostol-007/finance.git"
GIT_BRANCH="master"
#PROJECT_DIR="finance_project"

# Проверяем, что Docker установлен и доступен
docker -v >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Ошибка: Docker не установлен или не доступен."
  exit 1
fi

# Удаляем старый контейнер, если он существует
docker stop $DOCKER_CONTAINER >/dev/null 2>&1
docker rm $DOCKER_CONTAINER >/dev/null 2>&1

# Подгружаем код из репозитория Git
git clone -b $GIT_BRANCH $GIT_REPO

# Строим Docker образ из Dockerfile внутри репозитория
docker build -t $DOCKER_IMAGE .

# Запускаем Docker контейнер
docker run -d -p 8000:8000 --name $DOCKER_CONTAINER $DOCKER_IMAGE

echo "Контейнер запущен. Доступен по адресу http://localhost:8085/"
