#!/bin/bash

# Переменные
REPO_URL="https://github.com/Apostol-007/finance.git"
PROJECT_DIR="finance_project"

# Удаляем старую копию проекта, если она существует
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
fi

# Клонируем репозиторий
git clone $REPO_URL $PROJECT_DIR

# Переходим в директорию проекта
cd $PROJECT_DIR

# Создаем Docker образ
docker build -t finance_app .

# Запускаем Docker контейнер
docker run -p 8000:8000 finance_app
