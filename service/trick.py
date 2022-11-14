'''Facilitate interaction with tricks in the DB'''

from hundredandten.actions import Play
from hundredandten.constants import SelectableSuit
from hundredandten.trick import Trick

from service import card


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
