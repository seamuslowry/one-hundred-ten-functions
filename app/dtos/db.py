'''Format of a game of Hundred and Ten in the DB'''

from typing import Optional, TypedDict


class Card(TypedDict):
    '''A class to model the DB format of a card'''
    suit: str
    number: str


class Person(TypedDict):
    '''A class to model the DB format of a person'''
    id: str
    roles: list[str]
    automate: bool


class Player(Person):
    '''A class to model the DB format of a player'''
    hand: list[Card]


class Bid(TypedDict):
    '''A class to model the DB format of a Hundred and Ten bid'''
    identifier: str
    amount: int


class Play(TypedDict):
    '''A class to model the DB format of a Hundred and Ten play'''
    identifier: str
    card: Card


class Trick(TypedDict):
    '''A class to model the DB format of a Hundred and Ten trick'''
    plays: list[Play]
    round_trump: str


class Deck(TypedDict):
    '''A class to model the DB format of a Hundred and Ten deck'''
    seed: str
    pulled: int


class Discard(TypedDict):
    '''A class to model the DB format of a Hundred and Ten discard'''
    identifier: str
    cards: list[Card]
    kept: list[Card]


class Round(TypedDict):
    '''A class to model the DB format of a Hundred and Ten round'''
    players: list[Player]
    bids: list[Bid]
    deck: Deck
    trump: Optional[str]
    discards: list[Discard]
    tricks: list[Trick]


class Game(TypedDict):
    '''A class to model the DB format of a Hundred and Ten game'''
    id: str
    status: str
    name: str
    seed: str
    accessibility: str
    people: list[Person]
    rounds: list[Round]
    active_player: Optional[str]
    winner: Optional[str]


class User(TypedDict):
    '''A class to model the DB format of a Hundred and Ten user'''
    id: str
    name: str
    type: str
    picture_url: Optional[str]
