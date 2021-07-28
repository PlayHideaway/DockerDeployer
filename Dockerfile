FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


ENV DOCKER=1

RUN pip install fastapi-responses


COPY ./app /app/app


