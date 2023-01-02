import logging
from os import getenv
from typing import Dict, List

import socketio
from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import setup as setup_session
from euchrelib.game import Game

from api import app, sio
from api.cors import setup_cors
from api.utils import setup_logging

setup_logging()


games: Dict[str, List[Game]] = {}
app["games"] = games
app["AISid"] = None

setup_session(app, SimpleCookieStorage())

from api.routes import routes

app.add_routes(routes)
setup_cors(app)


if __name__ == "__main__":
    _logger = logging.getLogger()
    web.run_app(app, port=getenv("API_PORT"))
