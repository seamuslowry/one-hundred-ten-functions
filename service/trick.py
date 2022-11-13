'''Facilitate interaction with tricks in the DB'''

from hundredandten.actions import Play
from hundredandten.trick import Trick

from service import card


def to_db(trick: Trick) -> dict:
    '''Convert the provided trick into the dict structure used by the DB'''
    return {
        'plays': list(map(play_to_db_dict, trick.plays)),
    }


def play_to_db_dict(play: Play) -> dict:
    '''Convert the provided play into the dict structure used by the DB'''
    return {
        'identifier': play.identifier,
        'card': card.to_db(play.card)
    }
