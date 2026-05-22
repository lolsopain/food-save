# 1. Python asos tasviri (Python 3.13 talqini)
FROM python:3.13-slim

# 2. Ishchi katalogni belgilash
WORKDIR /app

# 3. Tizim uchun kerakli muhit o'zgaruvchilarini sozlash
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. requirements.txt faylini konteyner ichiga nusxalash
COPY requirements.txt /app/

# 5. Barcha kerakli kutubxonalarni o'rnatish
# --no-cache-dir keshni saqlamaydi va tasvir hajmini kichraytiradi
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Loyihaning barcha qolgan fayllarini konteynerga nusxalash
COPY . /app/

# 7. Statik fayllarni (CSS, JS, rasmlar) bir joyga yig'ish
RUN python manage.py collectstatic --noinput

# 8. Render uchun portni ochish
EXPOSE 10000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:10000"]