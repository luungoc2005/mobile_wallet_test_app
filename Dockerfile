FROM python:3.7-slim
MAINTAINER Ngoc Nguyen <ngoc.nguyen@2359media.com>

ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000
