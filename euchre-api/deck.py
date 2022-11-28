from dataclasses import dataclass
from enum import Enum
from random import shuffle
from typing import List

from dacite import Config as DaciteConfig
from dacite import from_dict


class GameObject:
    @classmethod
    def from_dict(cls, data):
        config = DaciteConfig(cast=[Number, Suit])
        return from_dict(data_class=cls, data=data, config=config)


class Number(str, Enum):
    # Commenting these out for a Euchre deck
    # two = "2"
    # three = "3"
    # four = "4"
    # five = "5"
    # six = "6"
    # seven = "7"
    # eight = "8"
    nine = "9"
    ten = "10"
    jack = "jack"
    queen = "queen"
    king = "king"
    ace = "ace"

    @property
    def order(self):
        ordermap = {
            "9": 7,
            "10": 8,
            "jack": 9,
            "queen": 10,
            "king": 11,
            "ace": 12,
        }
        return ordermap[self.value]

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order

    def __gt__(self, other):
        return self.order > other.order


class Suit(str, Enum):
    hearts = "hearts"
    spades = "spades"
    diamonds = "diamonds"
    clubs = "clubs"

    def get_off(self):
        if self == Suit.hearts:
            return Suit.diamonds
        elif self == Suit.diamonds:
            return Suit.hearts
        elif self == Suit.clubs:
            return Suit.spades
        elif self == Suit.spades:
            return Suit.clubs


@dataclass
class Card(GameObject):
    number: Number
    suit: Suit

    def istrump(self, trump: Suit) -> bool:
        return self.get_effective_suit(trump) == trump

    def get_effective_suit(self, trump: Suit) -> Suit:
        if self.number == Number.jack and self.suit == trump.get_off():
            return trump

        return self.suit

    @classmethod
    def max(self, c1: "Card", c2: "Card", led: Suit, trump: Suit) -> "Card":
        # First check trumps since we need to deal with jacks
        if c1.istrump(trump) and c2.istrump(trump):
            # If both numbers are same, they must be jack
            if c1.number == c2.number:
                if c1.suit == trump:
                    return c1
                else:
                    return c2

            # If it's not trump, it must be the off J
            for c in (c1, c2):
                if c.suit != trump:
                    return c

            # Only other J is top card
            for c in (c1, c2):
                if c.number == Number.jack:
                    return c

            # Okay so just return normal max number
            return max((c1, c2), key=lambda c: c.number)

        # Next just check if one is trump:
        for c in (c1, c2):
            if c.istrump(trump):
                return c

        # Realistically, one must be the led trump, else who cares
        if not c1.suit == led:
            return c2
        elif not c2.suit == led:
            return c1
        else:
            # Both must be led suit
            return max((c1, c2), key=lambda c: c.number)


class Deck:
    HAND_SIZE = 5

    def __init__(self):
        self._cards: List[Card] = []
        for number in Number:
            for suit in Suit:
                card = Card(number=number, suit=suit)
                self._cards.append(card)
        shuffle(self._cards)

    def dealone(self):
        card = self._cards.pop()
        return card

    def dealhand(self):
        return [self.dealone() for _ in range(self.HAND_SIZE)]
