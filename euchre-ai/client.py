import argparse
import asyncio
import logging
import random
from os import getenv
from time import sleep

import aiohttp
import socketio
from dotenv import load_dotenv
from euchrelib.deck import Card, Suit
from euchrelib.game import GameJSON

from ai import AI
from utils import setup_logging

_logger = logging.getLogger()


sio = socketio.AsyncClient(json=GameJSON)
session = aiohttp.ClientSession()
load_dotenv(".env")


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url", type=str, required=False, default=getenv("API_CONTAINER_URL")
    )
    parser.add_argument("--retry", type=int, required=False, default=0)
    parser.add_argument("--wait", type=int, required=False, default=10)

    args = parser.parse_args()

    return args


class Session(aiohttp.ClientSession):
    def start_session(self, url):
        super().__init__(url)


session = Session()


@sio.event
async def connect():
    _logger.info("Connection Established")
    await sio.emit("registerAI", {})


@sio.event
async def disconnect():
    _logger.info("Disconnected from Server")


async def get_hand(username, game_id):
    hand_params = {"username": username, "gameId": game_id}
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
    game_id = data["game_id"]
    hand = await get_hand(player["name"], game_id)
    _logger.info("Got hand %s", hand)

    status = data["rnd"]["status"]
    if status == "PLAYING":
        card = AI.play_card(data, hand)
        _logger.info("Playing %s for %s", card, player["name"])
        await sio.emit(
            "playCard", {"card": card, "username": player["name"], "gameId": game_id}
        )
    elif status == "CALLING_PICKUP":
        _logger.info("Passing trump for %s", player["name"])
        await sio.emit("passTrump", {"gameId": game_id})
    elif status == "CALLING_OPEN":
        dealer_index = data["rnd"]["dealer_index"]
        if player["user_id"] == data["players"][dealer_index]["user_id"]:
            eligible_suits = [
                suit for suit in Suit if suit != data["rnd"]["pickup_card"]["suit"]
            ]
            call_suit = random.choice(eligible_suits)
            _logger.info("Calling trump as %s for %s", call_suit, player["name"])
            await sio.emit(
                "callTrump",
                {"suit": call_suit, "username": player["name"], "gameId": game_id},
            )
        else:
            _logger.info("Passing trump for %s", player["name"])
            await sio.emit("passTrump", {"gameId": game_id})
    elif status == "PICKUP_DISCARD":
        card = AI.discard_card(data, hand)
        _logger.info("Discarding %s for %s", card, player["name"])
        await sio.emit(
            "discardCard", {"card": card, "username": player["name"], "gameId": game_id}
        )

    else:
        _logger.error("Unknown status %s", status)


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
