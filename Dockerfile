FROM python:3.9


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install poetry

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . /code

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

CMD gunicorn main:app --workers 2 --threads 1 --bind 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker --timeout 250
