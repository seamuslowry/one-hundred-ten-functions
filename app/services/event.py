'''Facilitate interaction with events on the game'''
from enum import Enum

from app.models import (Bid, Discard, Event, GameEnd, GameStart, Play,
                        RoundEnd, RoundStart, SelectTrump, TrickEnd,
                        TrickStart)
from app.services import card


class EventType(str, Enum):
    '''Enum value for event types to client'''
    GAME_START = 1
    ROUND_START = 2
    BID = 3
    SELECT_TRUMP = 4
    DISCARD = 5
    TRICK_START = 6
    PLAY = 7
    TRICK_END = 8
    ROUND_END = 9
    GAME_END = 10


def json(events: list[Event], client: str) -> list[dict]:
    '''Convert the provided list of events into the structure it should provide the client'''
    return __json(events, client)


def __json(events: list[Event], client: str) -> list[dict]:
    return list(map(lambda e: __json_with_users(e, client), events))


def __json_with_users(event: Event, client: str) -> dict:
    '''Convert the provided event into the structure it should provide the client'''
    ret = {}
    if isinstance(event, GameStart):
        ret = __game_start_json()
    if isinstance(event, RoundStart):
        ret = __round_start_json(event, client)
    if isinstance(event, Bid):
        ret = __bid_json(event)
    if isinstance(event, SelectTrump):
        ret = __select_trump_json(event)
    if isinstance(event, Discard):
        ret = __discard_json(event, client)
    if isinstance(event, TrickStart):
        ret = __trick_start_json()
    if isinstance(event, Play):
        ret = __play_json(event)
    if isinstance(event, TrickEnd):
        ret = __trick_end_json(event)
    if isinstance(event, RoundEnd):
        ret = __round_end_json(event)
    if isinstance(event, GameEnd):
        ret = __game_end_json(event)
    return ret


def __game_start_json() -> dict:
    return {
        "type": EventType.GAME_START.name
    }


def __round_start_json(event: RoundStart, client: str) -> dict:
    return {
        "type": EventType.ROUND_START.name,
        "dealer": event.dealer,
        "hands": ({identifier: list(map(card.json, hand))
                   if identifier == client else len(hand)
                   for identifier, hand in event.hands.items()})
    }


def __bid_json(event: Bid) -> dict:
    return {
        "type": EventType.BID.name,
        "identifier": event.identifier,
        "amount": event.amount.value
    }


def __select_trump_json(event: SelectTrump) -> dict:
    return {
        "type": EventType.SELECT_TRUMP.name,
        "identifier": event.identifier,
        "suit": event.suit.name
    }


def __discard_json(event: Discard, client: str) -> dict:
    return {
        "type": EventType.DISCARD.name,
        "identifier": event.identifier,
        "discards": (list(map(card.json, event.cards))
                     if client == event.identifier else len(event.cards))
    }


def __trick_start_json() -> dict:
    return {
        "type": EventType.TRICK_START.name
    }


def __play_json(event: Play) -> dict:
    return {
        "type": EventType.PLAY.name,
        "identifier": event.identifier,
        "card": card.json(event.card)
    }


def __trick_end_json(event: TrickEnd) -> dict:
    return {
        "type": EventType.TRICK_END.name,
        "winner": event.winner
    }


def __round_end_json(event: RoundEnd) -> dict:
    return {
        "type": EventType.ROUND_END.name,
        "scores": event.scores
    }


def __game_end_json(event: GameEnd) -> dict:
    return {
        "type": EventType.GAME_END.name,
        "winner": event.winner
    }
