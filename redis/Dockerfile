# syntax=docker/dockerfile:1
FROM redis:latest
ARG DOTENV_FILE

COPY $DOTENV_FILE /.env
COPY ./redis/redis.conf /redis.conf
COPY ./redis/entrypoint.sh /entrypoint.sh

LABEL name="euchre-redis"

CMD /entrypoint.sh
