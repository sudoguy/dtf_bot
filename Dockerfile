FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    libffi-dev \
    musl-dev \
    postgresql-dev \
    libc-dev \
    linux-headers 
RUN pip install poetry

RUN mkdir /install

WORKDIR /install
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# RUN apk del --no-cache .build-deps

COPY . /app

WORKDIR /app
