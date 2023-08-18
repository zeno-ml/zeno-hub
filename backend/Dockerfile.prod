FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install poetry

RUN poetry install

EXPOSE 80

CMD ["poetry", "run", "backend"]