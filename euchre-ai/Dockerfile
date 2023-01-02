# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3.10 python3-pip

# Need this for the newer pypoject.toml packaging to work
RUN python3 -m pip install --upgrade pip

COPY ./euchrelib /euchrelib
RUN python3 -m pip install /euchrelib

COPY ./euchre-ai /app
COPY ./.env.prod /app/.env
WORKDIR /app

RUN python3 -m pip install -r ./requirements.txt

CMD python3 client.py --retry 3 --wait 10
