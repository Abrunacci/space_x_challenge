FROM python:3.10

RUN apt update

ENV PYTHONPATH=/app/src

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r Docker/development/requirements.txt
RUN poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev")
EXPOSE 3000