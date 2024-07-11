# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную среды PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем requirements.txt в контейнер и устанавливаем зависимости
COPY requirements.txt .

# Устанавливаем зависимости с помощью pip
RUN pip install -r requirements.txt

# Копируем все файлы проекта в текущую директорию контейнера
COPY . .

# Экспортируем порт 8000 для веб-сервера Django
EXPOSE 8000

# Команда для запуска сервера Django внутри контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
