FROM python:3.6-alpine

RUN mkdir /install
WORKDIR /install

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    libc-dev \
    linux-headers \ 
    && \
    apk add --no-cache \
    postgresql-dev

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN apk del --no-cache .build-deps

COPY . /app

WORKDIR /app
