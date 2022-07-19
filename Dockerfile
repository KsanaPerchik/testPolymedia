FROM python:3.9-alpine

ENV DEBIAN_FRONTEND noninteractive

RUN pip install --no-cache-dir flask flask-smorest flask-sqlalchemy requests pytest

WORKDIR /www

COPY ./www /www

RUN mkdir /www/tests

ENV DEBIAN_FRONTEND teletype
