FROM python:3.6-stretch

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update

CMD ["/usr/local/bin/gunicorn", "-b", ":8000", "app:app"]

EXPOSE 8000
