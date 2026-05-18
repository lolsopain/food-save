FROM python:3.12-slim

WORKDIR /app

# Muhim tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Pip-ni yangilab, talablarni va gunicorn-ni aniq o'rnatamiz
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

# Portni Render talabiga moslab 10000 qilamiz
EXPOSE 10000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:10000"]