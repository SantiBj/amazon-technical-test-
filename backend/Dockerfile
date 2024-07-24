FROM python:3.12.2-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
