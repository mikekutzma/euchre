import logging
from os import getenv

import socketio
from euchrelib.deck import Card, Suit
from euchrelib.game import GameJSON

_logger = logging.getLogger(__name__)


class SocketController:
    def __init__(self, app):
        self.app = app
        self.sio = socketio.AsyncServer(
            async_mode="aiohttp",
            async_handlers=True,
            cors_allowed_origins=[
                "*",
                getenv("FRONTEND_URL"),
            ],
            json=GameJSON,
        )
        self.register_handlers(self.sio)
        self.sio.attach(app)

    def register_handlers(self, sio):
        handlers = {
            "registerAI": self.registerAI,
            "callTrumpOpen": self.callTrumpOpen,
            "callTrumpPickup": self.callTrumpPickup,
            "discardCard": self.discardCard,
            "passTrump": self.passTrump,
            "playCard": self.playCard,
            "startGame": self.startGame,
            "startRound": self.startRound,
            "clearTrick": self.clearTrick,
        }
        for event, handler in handlers.items():
            sio.on(event, handler=handler)

    async def registerAI(self, sid, data):
        _logger.info("Registering SID %s as AI", sid)
        self.app["AISid"] = sid

    async def update_status(self, game):
        await self.sio.emit("gameStatus", game.status, room=game.game_id)
        ai_sid = self.app["AISid"]
        if ai_sid is not None:
            await self.sio.emit("gameStatus", game.status, room=ai_sid)

    async def callTrumpPickup(self, sid, data):
        username = data.get("username")
        suit = Suit[data["suit"]]
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.set_trump(suit, sid, username=username)
        game.pickup_trump()
        await self.sio.emit("refreshHand", {}, room=game_id)
        await self.update_status(game)

    async def callTrumpOpen(self, sid, data):
        username = data.get("username")
        suit = Suit[data["suit"]]
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.set_trump(suit, sid, username=username)
        game.start_playing_round()
        await self.update_status(game)

    async def discardCard(self, sid, data):
        card = Card.from_dict(data["card"])
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.discard_card(card)
        game.start_playing_round()
        await self.update_status(game)

    async def passTrump(self, sid, data):
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.pass_trump(sid)
        await self.update_status(game)

    async def playCard(self, sid, data):
        username = data.get("username")
        card = Card.from_dict(data["card"])
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.play_card(sid, card, username=username)
        await self.update_status(game)

    async def startGame(self, sid, data):
        _logger.info("Starting game")
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.start_game()
        await self.update_status(game)
        games = [id for id, game in self.app["games"].items() if not game.live]
        await self.sio.emit("gamesUpdate", games)

    async def startRound(self, sid, data):
        _logger.info("Starting Round")
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.start_round()
        await self.update_status(game)
        await self.sio.emit("refreshHand", {}, room=game_id)

    async def clearTrick(self, sid, data):
        _logger.info("Clearing trick")
        game_id = data["gameId"]
        game = self.app["games"][game_id]
        game.rnd.trick.clear()
        await self.update_status(game)
