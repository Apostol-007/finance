# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем requirements.txt в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt > logs.txt 2>&1

# Копируем все файлы проекта в рабочую директорию
COPY . /app/

# Открываем порт 8000 для доступа
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "finance/manage.py", "runserver"]

