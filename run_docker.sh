#!/bin/bash

# Переменные для настройки контейнера
DOCKER_IMAGE="apostol-finance"
DOCKER_CONTAINER="finance-apostol"
GIT_REPO="https://github.com/Apostol-007/finance_project.git"
GIT_BRANCH="main"

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

cd finance_project

chmod +x *

docker build -t apostol-finance .
cp Dockerfile ../
cp docker-compose.yml ../
cd ..

# Запускаем контейнеры с помощью docker-compose
docker-compose up -d
chmod 777 /var/lib/docker
echo "chmod 777 /var/lib/docker"
chmod -R 777 /var/lib/docker/volumes/*
echo "chmod 777 /var/lib/docker/volumes/*"
echo "Контейнеры запущены. db доступен по адресу localhost:5432"
