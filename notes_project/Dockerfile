# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем зависимости для psycopg2 и других пакетов
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Создаём директорию проекта
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект (включая entrypoint.sh)
COPY . /app/

# Делаем entrypoint.sh исполняемым
RUN chmod +x ./entrypoint.sh

# Запускаем сервер Django через entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]