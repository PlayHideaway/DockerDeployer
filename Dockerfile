FROM python:slim

ENV DOCKER=1

RUN pip install aiohttp


COPY src /src

CMD [ "python", "/src/main.py"]

