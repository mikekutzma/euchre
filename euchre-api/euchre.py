import asyncio
import logging
from os import getenv
from typing import Dict, List

import asyncpg
import socketio
from aiohttp import web
from aiohttp_session import setup as setup_session
from dotenv import load_dotenv
from euchrelib.game import Game

from api.cors import setup_cors
from api.postgres_storage import PostgresStorage
from api.routes import routes
from api.sockets import SocketController
from api.utils import setup_logging

setup_logging()


async def init_app():
    load_dotenv(".env")
    app = web.Application()
    sio = SocketController(app)
    app["sio"] = sio
    games: Dict[str, List[Game]] = {}
    app["games"] = games
    app["AISid"] = None
    dboptions = {"database": "euchre", "user": "mike"}

    setup_session(
        app,
        PostgresStorage(
            pg_pool=await asyncpg.create_pool(**dboptions)
        ),
    )

    app.add_routes(routes)
    setup_cors(app)
    return app

async def test(pool):
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""SELECT * from users""")
    _logger.info("Got rows")
    _logger.info(row)
    _logger.info("Done")


if __name__ == "__main__":
    _logger = logging.getLogger()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=getenv("API_CONTAINER_PORT"), loop=loop)
