import asyncio
import logging
import urllib
from os import getenv
from typing import Dict, List

import socketio
from aiohttp import web
from aiohttp_session import setup as setup_session
from dotenv import load_dotenv
from euchrelib.game import Game
from get_docker_secret import get_docker_secret
from redis import asyncio as aioredis

from api.cors import setup_cors
from api.redis_storage import RedisConfig, RedisStorage
from api.routes import routes
from api.sockets import SocketController
from api.utils import setup_logging

setup_logging()
_logger = logging.getLogger()


async def init_app():
    load_dotenv(".env")
    app = web.Application()
    sio = SocketController(app)
    app["sio"] = sio
    games: Dict[str, List[Game]] = {}
    app["games"] = games
    app["AISid"] = None

    redisconf = RedisConfig(
        host=get_docker_secret("redishost"),
        port=get_docker_secret("redisport"),
        username=get_docker_secret("redisuser"),
        password=get_docker_secret("redispasswd"),
        decode_responses=True,
    )
    redis = await aioredis.Redis(**redisconf.to_dict())
    app["redis"] = redis
    setup_session(
        app,
        RedisStorage(redis=redis),
    )

    app.add_routes(routes)
    setup_cors(app)
    return app


if __name__ == "__main__":
    _logger = logging.getLogger()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=getenv("API_CONTAINER_PORT"), loop=loop)
