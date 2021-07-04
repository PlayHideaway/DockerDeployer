FROM python:slim


RUN pip install aiohttp


COPY src /src
COPY test /test

CMD [ "python", "/src/main.py"]

