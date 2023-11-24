FROM python:3.10

RUN apt update

ENV PYTHONPATH=/app/src \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r Docker/development/requirements.txt
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt
EXPOSE 3000