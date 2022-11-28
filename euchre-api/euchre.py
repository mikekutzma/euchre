import logging
import pathlib

import socketio
from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import setup as setup_session

from cors import setup_cors
from game import Game
from utils import setup_logging
setup_logging()

app = web.Application()

app["games"] = {}
app["game"] = Game()

setup_session(app, SimpleCookieStorage())

from sockets import sio
sio.attach(app)

# redis = aioredis.from_url("redis://localhost:55000", )


from routes import routes
app.add_routes(routes)
app.router.add_static(
    "/", pathlib.Path(__file__).parent / "dist", show_index=True
)
setup_cors(app)


if __name__ == "__main__":
    _logger = logging.getLogger()
    web.run_app(app)
