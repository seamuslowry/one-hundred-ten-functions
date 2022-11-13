'''Facilitate interaction with cards in the DB'''

from hundredandten.deck import Card


def to_db(card: Card) -> dict:
    '''Convert the provided card into the dict structure used by the DB'''
    return {
        'suit': card.suit.name,
        'number': card.number.name
    }
