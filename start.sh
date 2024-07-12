#!/bin/bash

# Применяем миграции
python /app/manage.py migrate

# Запускаем сервер
python /app/manage.py runserver
