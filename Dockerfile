FROM python:3.12-slim

WORKDIR /app

# Tizim uchun kerakli paketlarni o'rnatamiz
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Pip-ni yangilab, gunicorn va whitenoise-ni kafolatlangan holda o'rnatamiz
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn whitenoise

COPY . .

# Render muhitida SECRET_KEY topilmay qolsa, qurilish jarayoni (build) sinib qolmasligi uchun vaqtincha default qiymat beramiz
ENV SECRET_KEY=temporary-secret-key-for-building-purposes

# Statik fayllarni (CSS, JS, rasmlar) bir joyga yig'ish
RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:10000"]