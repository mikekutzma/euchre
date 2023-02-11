# syntax=docker/dockerfile:1
FROM ubuntu:latest
ARG DOTENV_FILE

RUN apt-get update -y && \
    apt-get install -y python3.10 python3-pip

# Need this for the newer pypoject.toml packaging to work
RUN python3 -m pip install --upgrade pip

COPY ./euchrelib /euchrelib
RUN python3 -m pip install /euchrelib

COPY ./euchre-ai /app
COPY $DOTENV_FILE /app/.env
WORKDIR /app

RUN python3 -m pip install -r ./requirements.txt

LABEL name="euchre-ai"

CMD python3 client.py --retry 3 --wait 10
