FROM python:3.8-slim-buster

WORKDIR /test_task

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD gunicorn --bind 0.0.0.0:80 main:app -w 2