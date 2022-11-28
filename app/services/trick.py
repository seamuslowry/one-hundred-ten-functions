'''Facilitate interaction with tricks in the DB'''

from app.models import Play, SelectableSuit, Trick
from app.services import card


def to_db(trick: Trick) -> dict:
    '''Convert the provided trick into the dict structure used by the DB'''
    return {
        'plays': list(map(__play_to_db, trick.plays)),
        'round_trump': trick.round_trump.name
    }


def from_db(trick: dict) -> Trick:
    '''Convert the provided dict from the DB into a Trick instance'''
    return Trick(
        round_trump=SelectableSuit[trick['round_trump']],
        plays=list(map(__play_from_db, trick['plays']))
    )


def __play_to_db(play: Play) -> dict:
    '''Convert the provided play into the dict structure used by the DB'''
    return {
        'identifier': play.identifier,
        'card': card.to_db(play.card)
    }


def __play_from_db(play: dict) -> Play:
    '''Convert the provided dict from the DB into a Play instance'''
    return Play(
        identifier=play['identifier'],
        card=card.from_db(play['card'])
    )


def json(trick: Trick) -> dict:
    '''Convert the provided trick into the structure it should provide the client'''
    winning_play = trick.winning_play

    return {
        'winning_play': __play_json(winning_play) if winning_play else None,
        'bleeding': trick.bleeding,
        'plays': list(map(__play_json, trick.plays)),
    }


def __play_json(play: Play) -> dict:
    '''Convert the provided play into the structure it should provide the client'''
    return {
        'identifier': play.identifier,
        'card': card.json(play.card)
    }
