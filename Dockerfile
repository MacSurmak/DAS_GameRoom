# Используем официальный образ Python
FROM python:3.13-slim

ENV TZ="Europe/Moscow"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями *отдельно*
COPY requirements.txt .

# Устанавливаем зависимости (включая playwright) *ДО* копирования остального кода
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

# Копируем *остальные* файлы проекта
COPY . .

# Запускаем бота
CMD ["python", "bot.py"]