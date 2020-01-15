FROM python:3.6-stretch

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update

EXPOSE 8000
