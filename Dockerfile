FROM python:3.9


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true

WORKDIR /code
COPY . /code
RUN pip install poetry==1.4.2
RUN poetry install --no-root

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

CMD gunicorn main:app --workers 2 --threads 1 --bind 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker --timeout 250
