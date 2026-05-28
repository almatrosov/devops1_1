# Используем легковесный официальный образ Python
FROM python:3.10-slim

# Устанавливаем системные зависимости, необходимые для компиляции драйвера БД psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Настраиваем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код бэкенда
COPY app.py .

# Декларируем, что контейнер ожидает подключения на порту 5000 (внутри сети Docker)
EXPOSE 5000

# Инструкция для запуска приложения
CMD ["python", "app.py"]