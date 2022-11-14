'''Facilitate interaction with cards in the DB'''

from hundredandten.constants import (CardNumber, SelectableSuit,
                                     UnselectableSuit)
from hundredandten.deck import Card


def to_db(card: Card) -> dict:
    '''Convert the provided card into the dict structure used by the DB'''
    return {
        'suit': card.suit.name,
        'number': card.number.name
    }


def from_db(card: dict) -> Card:
    '''Convert the provided dict from the DB into a Card instance'''

    selectable_suit = None
    unselectable_suit = None

    try:
        selectable_suit = SelectableSuit[card['suit']]
    except KeyError:
        pass

    try:
        unselectable_suit = UnselectableSuit[card['suit']]
    except KeyError:
        pass

    if not (selectable_suit and unselectable_suit):
        raise KeyError('Invalid suit passed for card')

    return Card(
        suit=selectable_suit or unselectable_suit,
        number=CardNumber[card['number']]
    )
