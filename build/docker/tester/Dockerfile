FROM python:3.10.2-alpine

RUN set -eux && \
    apk add --no-cache \
        openssl-dev \
        postgresql-libs \
        musl-dev \
        gcc \
        g++ \
        libffi-dev \
        postgresql-dev

COPY assets/requirements.txt /

RUN python -m pip install -r /requirements.txt --upgrade
