FROM docker.io/library/python:3.11-slim

WORKDIR /build

RUN apt-get -qy update \
    && apt-get -qy install procps tini

COPY rootfs /

RUN pip3 install --upgrade pip \
    && pip3 install poetry

COPY pyproject.toml .
COPY src /build/src

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --verbose

ENTRYPOINT ["/usr/bin/tini", "--"]
