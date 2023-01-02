from aiohttp import web
from dotenv import load_dotenv

from .sockets import SocketController

load_dotenv(".env")
app = web.Application()
sio = SocketController(app)
