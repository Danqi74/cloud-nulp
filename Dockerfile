FROM python:3.11-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли проєкту
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Встановлюємо gunicorn
RUN pip install gunicorn

# Експортуємо порт
EXPOSE 8080

# Команда запуску
# main:application – це твій WSGI entrypoint із .wsgi/.swgi
CMD ["gunicorn", "-b", "0.0.0.0:8080", "gunicorn:application"]
