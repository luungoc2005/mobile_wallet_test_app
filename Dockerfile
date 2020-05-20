FROM python:3.7-slim
MAINTAINER Ngoc Nguyen <ngoc.nguyen@2359media.com>

RUN apt-get update && apt-get install -y cron libpq-dev gcc

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN python manage.py crontab add
CMD python manage.py runserver 0.0.0.0:8000
