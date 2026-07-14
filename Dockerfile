FROM python:3.12

WORKDIR /app

# 레이어 캐싱으로 인해 먼저 COPY 함
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py migrate --noinput &&\
    python manage.py runserver 0.0.0.0:8000