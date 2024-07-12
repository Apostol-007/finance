# Используем официальный образ Python
FROM python:3.10

RUN mkdir /app
# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

ADD requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Открываем порт 8000 для доступа
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver"]

