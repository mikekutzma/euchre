import logging

import socketio

from deck import Card, Suit
from euchre import app
from game import GameJSON

_logger = logging.getLogger(__name__)


sio = socketio.AsyncServer(
    async_mode="aiohttp",
    async_handlers=True,
    cors_allowed_origins=[
        "*",
        "http://localhost:5173",
        "http://kosh.local:5173",
        "http://localhost:8000",
        "http://kosh.local:8000",
    ],
    json=GameJSON,
)


@sio.on("callTrump")
async def on_call_trump(sid, data):
    username = data.get("username")
    suit = Suit[data["suit"]]
    app["game"].call_trump(suit, sid, username=username)
    await sio.emit("gameStatus", app["game"].status)


@sio.on("passTrump")
async def on_pass_trump(sid, data):
    app["game"].pass_trump(sid)
    await sio.emit("gameStatus", app["game"].status)


@sio.on("playCard")
async def on_play_card(sid, data):
    username = data.get("username")
    card = Card.from_dict(data["card"])
    app["game"].play_card(sid, card, username=username)
    await sio.emit("gameStatus", app["game"].status)


@sio.on("startGame")
async def startGame(sid, data):
    _logger.info("Starting game")
    app["game"].start_game()
    await sio.emit("gameStatus", app["game"].status)


@sio.on("startRound")
async def startRound(sid, data):
    _logger.info("Starting Round")
    app["game"].start_round()
    await sio.emit("gameStatus", app["game"].status)
    await sio.emit("refreshHand", {});


@sio.on("clearTrick")
async def clearTrick(sid, data):
    _logger.info("Clearing trick")
    app["game"].rnd.trick.clear()
    await sio.emit("gameStatus", app["game"].status)
