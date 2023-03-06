from typing import Dict, List

from euchrelib.deck import Suit, Card


class AI:
    @classmethod
    def is_ais_turn(cls, data):
        live = (
            data["live"]
            and not data["rnd"]["done"]
            and not data["rnd"]["trick"]["done"]
        )
        isAI = data["players"][data["turn_index"]]["isAI"]
        return live and isAI

    @classmethod
    def play_card(cls, gameStatus: Dict, hand: List):
        trump = Suit[gameStatus["rnd"]["trick"]["trump"]]
        _led = gameStatus["rnd"]["trick"].get("led")
        if _led is None:
            led = None
        else:
            led = Suit[_led]

        if led is None:
            return hand[0]
        else:
            # Something has been led
            followed = [card for card in hand if card.get_effective_suit(trump) == led]
            if followed:
                # Need to follow if we can
                return followed[0]
            else:
                return hand[0]
    @classmethod
    def discard_card(cls, gameStatus: Dict, hand:List):
        pickup_card = Card.from_dict(gameStatus["rnd"]["pickup_card"])
        discardable_cards = [card for card in hand if card != pickup_card]

        # Need to implement some smarter logic here
        return discardable_cards[0]
