FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

RUN poetry install

EXPOSE 8000