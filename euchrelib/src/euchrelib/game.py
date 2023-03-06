import json
import logging
import random
import uuid
from copy import deepcopy
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from importlib_resources import files

from .deck import Card, Deck, Suit

_logger = logging.getLogger(__name__)
NPLAYERS = 4

SAMPLE_NAMES = ["Kosh", "Linus", "Scamp"]


@dataclass
class Player:
    name: str
    team: int
    sids: List[str] = field(default_factory=list)
    hand: List[Card] = field(default_factory=list)
    isAI: bool = False
    user_id: str = field(init=False)

    def __post_init__(self):
        self.user_id = str(uuid.uuid4())

    def add_sid(self, sid):
        if sid is not None:
            self.sids = sorted(list(set([sid, *self.sids])))

    def play_card(self, card: Card):
        self.hand.remove(card)

    def pickup_card(self, card: Card):
        self.hand.append(card)

    def discard_card(self, card: Card):
        self.hand.remove(card)

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)


@dataclass
class Trick:
    trump: Optional[Suit] = None
    led: Optional[Suit] = None
    cards: Dict[Player, Card] = field(default_factory=dict)
    done: bool = False
    winner: Optional[Player] = None

    def play_card(self, user, card):
        self.cards[user] = card
        if not self.led:
            self.led = card.get_effective_suit(self.trump)
        if len(self.cards) >= NPLAYERS:
            self.done = True
            self.calc_winner()

    def calc_winner(self):
        cards = list(self.cards.values())
        m = cards[0]
        for c in cards[1:]:
            m = Card.max(m, c, trump=self.trump, led=self.led)

        for u, c in self.cards.items():
            if c == m:
                self.winner = u
                break
        return u

    def clear(self):
        trump = self.trump
        self.__init__(trump=trump)


class RoundStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    CALLING_PICKUP = "CALLING_PICKUP"
    CALLING_OPEN = "CALLING_OPEN"
    PLAYING = "PLAYING"
    PICKUP_DISCARD = "PICKUP_DISCARD"


@dataclass
class Round:
    dealer_index: int = 3
    calling_team_index: Optional[int] = None
    trump: Optional[Suit] = None
    score: List[int] = field(default_factory=lambda: [0, 0])
    done: bool = False
    status: RoundStatus = RoundStatus.NOT_STARTED
    pickup_card: Optional[Card] = None
    trick: Trick = field(default_factory=Trick)
    winner: Optional[int] = None

    def play_card(self, player, card):
        self.trick.play_card(player, card)
        if self.trick.done:
            winner = self.trick.winner
            self.score[winner.team] += 1

        if sum(self.score) >= Deck.HAND_SIZE:
            self.done = True
            self.winner = self.score.index(max(self.score))

    def get_points(self):
        if self.winner == self.calling_team_index:
            if self.score[self.winner] >= Deck.HAND_SIZE:
                return 2
            else:
                return 1
        else:
            return 2


@dataclass
class Team:
    team_name: str = field(init=False)

    def __post_init__(self):
        self.team_name = self.generate_name()

    def generate_name(self):
        data_text = files("euchrelib.data").joinpath("animals.txt").read_text()
        animals = [line.strip() for line in data_text.splitlines() if line.strip()]

        animal = random.choice(animals)
        return animal.title() + "s"


@dataclass
class Game:
    deck: Deck = field(default_factory=Deck)
    players: List[Player] = field(default_factory=list)
    score: List[int] = field(default_factory=lambda: [0, 0])
    rnd: Round = field(default_factory=Round)
    live: bool = False
    game_id: str = field(init=False)
    turn_index: int = 0
    teams: List[Team] = field(init=False)

    def __post_init__(self):
        self.game_id = str(uuid.uuid4())
        self.teams = [Team(), Team()]

    def shuffle(self):
        self.deck = Deck()

    def start_game(self):
        for i in range(NPLAYERS - len(self.players)):
            name = SAMPLE_NAMES[i]
            self.add_player(name, sid=None, isAI=True)
        self.live = True
        self.start_round()

    def start_round(self):
        trump_card = self.deal()
        new_round = Round(
            dealer_index=(self.rnd.dealer_index + 1) % NPLAYERS,
            status=RoundStatus.CALLING_PICKUP,
            pickup_card=trump_card,
        )

        self.rnd = new_round

        self.turn_index = (self.rnd.dealer_index + 1) % len(self.players)
        self.turn = self.players[self.turn_index].name
        self.dealer = self.players[self.rnd.dealer_index].name

    def deal(self):
        self.shuffle()
        for player in self.players:
            player.hand = self.deck.dealhand()

        trump_card = self.deck.dealone()
        return trump_card

    def add_player(self, username, sid, isAI=False):
        player = self.get_player(username)
        if player is None:
            team = len(self.players) % 2
            player = Player(name=username, team=team, isAI=isAI)
            self.players.append(player)

        player.add_sid(sid)
        return player

    def get_player(self, username) -> Optional[Player]:
        for player in self.players:
            if username == player.name:
                return player
        return None

    def get_players(self) -> List[Dict[str, Any]]:
        data = []
        for player in self.players:
            pd = asdict(player)
            del pd["sids"]
            del pd["hand"]
            data.append(pd)
        return data

    def get_hand(self, username) -> List[Card]:
        player = self.get_player(username)
        if player is not None:
            return player.hand
        return []

    def play_card(self, sid, card, username=None):
        if username is not None:
            player = self.get_player(username)
        else:
            player = self.get_player_by_sid(sid)

        player.play_card(card)

        self.rnd.play_card(player, card)

        if self.rnd.done:
            self.score[self.rnd.winner] += self.rnd.get_points()
        else:
            if self.rnd.trick.done:
                self.turn_index = self.players.index(self.rnd.trick.winner)
            else:
                self.turn_index = (self.turn_index + 1) % NPLAYERS

    def get_player_by_sid(self, sid):
        for player in self.players:
            if sid in player.sids:
                return player

        return None

    def pass_trump(self, sid=None, player=None):
        if self.turn_index == self.rnd.dealer_index:
            self.rnd.status = RoundStatus.CALLING_OPEN

        self.turn_index = (self.turn_index + 1) % NPLAYERS

    def set_trump(self, suit, sid=None, username=None):
        if username is None:
            player = self.get_player_by_sid(sid)
        else:
            player = self.get_player(username)
        self.rnd.calling_team_index = player.team
        self.rnd.trump = suit
        self.rnd.trick.trump = suit

    def start_playing_round(self):
        self.rnd.status = RoundStatus.PLAYING
        self.turn_index = (self.rnd.dealer_index + 1) % NPLAYERS

    def pickup_trump(self):
        self.rnd.status = RoundStatus.PICKUP_DISCARD
        self.turn_index = self.rnd.dealer_index
        self.players[self.rnd.dealer_index].pickup_card(self.rnd.pickup_card)

    def discard_card(self, card):
        self.players[self.rnd.dealer_index].discard_card(card)
        self.rnd.status = RoundStatus.PLAYING
        self.turn_index = (self.rnd.dealer_index + 1) % NPLAYERS

    @property
    def status(self) -> Dict:
        trick_cards = {
            player.name: asdict(card) for player, card in self.rnd.trick.cards.items()
        }
        game_copy = deepcopy(self)
        game_copy.rnd.trick.cards = {}

        data = asdict(game_copy)
        data["rnd"]["trick"]["cards"] = trick_cards
        if len(self.players):
            data["turn"] = self.players[self.turn_index].name
        del data["deck"]
        for player in data["players"]:
            player["n_cards"] = len(player["hand"])
            del player["hand"]

        return data


def status_factory(data):
    out = {}
    for key, value in data:
        if isinstance(key, Player):
            out[key.name] = value
        else:
            out[key] = value
    return out


class GameEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Deck):
            return obj._cards

        elif isinstance(obj, Game):
            return obj.status

        elif is_dataclass(obj):
            return asdict(obj)

        return super().default(obj)


class GameJSON:
    @classmethod
    def dumps(cls, *args, **kwargs):
        return json.dumps(*args, **kwargs, cls=GameEncoder)

    @classmethod
    def loads(cls, *args, **kwargs):
        return json.loads(*args, **kwargs)
