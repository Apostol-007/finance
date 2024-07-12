#!/bin/bash

# Переменные для настройки контейнера
#DOCKER_IMAGE="apostol-finance"
#DOCKER_CONTAINER="finance-apostol"
#GIT_REPO="https://github.com/Apostol-007/finance.git"
#GIT_BRANCH="master"
#PROJECT_DIR="finance_project"

# Проверяем, что Docker установлен и доступен
#docker -v >/dev/null 2>&1
#if [ $? -ne 0 ]; then
#  echo "Ошибка: Docker не установлен или не доступен."
#  exit 1
#fi

# Удаляем старый контейнер, если он существует
#docker stop $DOCKER_CONTAINER >/dev/null 2>&1
#docker rm $DOCKER_CONTAINER >/dev/null 2>&1

# Подгружаем код из репозитория Git
#git clone -b $GIT_BRANCH $GIT_REPO

#cd finance

# Строим Docker образ из Dockerfile внутри репозитория
#docker build -t $DOCKER_IMAGE .

# Запускаем Docker контейнер
#docker run -d -p 8000:8000 --name $DOCKER_CONTAINER $DOCKER_IMAGE
#echo "Контейнер запущен. Доступен по адресу http://localhost:8000/"
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
