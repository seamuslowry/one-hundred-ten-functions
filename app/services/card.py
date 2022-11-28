'''Facilitate interaction with cards in the DB'''

from app.models import Card, CardNumber, SelectableSuit, UnselectableSuit


def to_db(card: Card) -> dict:
    '''Convert the provided card into the dict structure used by the DB'''
    return {
        'suit': card.suit.name,
        'number': card.number.name
    }


def from_db(card: dict) -> Card:
    '''Convert the provided dict from the DB into a Card instance'''

    return __from_json(card)


def from_client(card: dict) -> Card:
    '''Convert the provided dict from the client into a Card instance'''

    return __from_json(card)


def json(card: Card) -> dict:
    '''Convert the provided card into the structure it should provide the client'''
    return {
        'suit': card.suit.name,
        'number': card.number.name
    }


def __from_json(card: dict) -> Card:
    '''Convert the provided dict from JSON into a Card instance'''

    suit = None

    try:
        suit = SelectableSuit[card['suit']]
    except KeyError:
        pass

    try:
        suit = UnselectableSuit[card['suit']]
    except KeyError:
        pass

    assert suit

    return Card(
        suit=suit,
        number=CardNumber[card['number']]
    )
