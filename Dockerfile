FROM python:3.9

WORKDIR /code
COPY ./api /code
COPY requirements.txt /code

RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

CMD gunicorn main:app --workers 5 --threads 1 --bind 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker --timeout 250
