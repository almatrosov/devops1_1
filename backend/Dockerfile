FROM python:3.10-slim

WORKDIR /app

# Устанавливаем системные зависимости для сборки psycopg2 (библиотеки Postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \    libpq-dev gcc \    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5001

CMD ["python", "app.py"]