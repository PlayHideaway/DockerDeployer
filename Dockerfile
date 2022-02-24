FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


ENV DOCKER=1

RUN apt-get update && apt-get install docker-compose

RUN pip install fastapi-responses aiodocker 


COPY ./app /app/app


