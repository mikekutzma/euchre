import asyncio
import json
import logging
import random


import aiohttp
import socketio

from ai import AI
from deck import Card, Suit
from game import GameJSON
from utils import setup_logging
import argparse

_logger = logging.getLogger()


sio = socketio.AsyncClient(json=GameJSON)
session = aiohttp.ClientSession()
URL = "http://kosh.local:8000"


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("url", type=str)

    args = parser.parse_args()

    return args

class Session(aiohttp.ClientSession):

    def start_session(self, url):
        super().__init__(url)


session = Session()


@sio.event
async def connect():
    _logger.info("Connection Established")


@sio.event
async def disconnect():
    _logger.info("Disconnected from Server")


async def get_hand(username):
    hand_params = {"username": username}
    async with session.get("/hand", params=hand_params) as resp:
        hand_data = await resp.json()
        _logger.info(hand_data)

    hand = [Card.from_dict(card) for card in hand_data]

    return hand

@sio.on("gameStatus")
async def on_game_status(data):
    if not AI.is_ais_turn(data):
        _logger.info("Not AIs turn")
        return

    _logger.info("Calculating AI move...")

    player = data["players"][data["turn_index"]]
    hand = await get_hand(player["name"])
    _logger.info("Got hand %s", hand)

    status = data["rnd"]["status"]
    if status == "PLAYING":
        card = AI.play_card(data, hand)
        _logger.info("Playing %s for %s", card, player["name"])
        await sio.emit("playCard", {"card": card, "username": player["name"]})
    elif status == "CALLING_PICKUP":
        _logger.info("Passing trump for %s", player["name"])
        await sio.emit("passTrump", {})
    elif status == "CALLING_OPEN":
        dealer_index = data["rnd"]["dealer_index"]
        if player["user_id"] == data["players"][dealer_index]["user_id"]:
            eligible_suits = [
                suit for suit in Suit if suit != data["rnd"]["pickup_card"]["suit"]
            ]
            call_suit = random.choice(eligible_suits)
            _logger.info("Calling trump as %s for %s", call_suit, player["name"])
            await sio.emit("callTrump", {"suit": call_suit, "username": player["name"]})
        else:
            _logger.info("Passing trump for %s", player["name"])
            await sio.emit("passTrump", {})



async def main(args):
    session.start_session(args.url)
    await sio.connect(args.url)
    await sio.wait()
    # await session.close()


if __name__ == "__main__":
    args = get_args()
    setup_logging()
    _logger = logging.getLogger(__name__)
    asyncio.run(main(args))
