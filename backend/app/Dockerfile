FROM python:3.6-stretch

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y supervisor

CMD service supervisod start