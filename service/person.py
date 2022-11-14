'''Facilitate interaction with persons in the DB'''

from typing import Union

from hundredandten.constants import GameRole
from hundredandten.group import Person, Player

from service import card


def to_db(person: Union[Person, Player]) -> dict:
    '''Convert the provided person into the dict structure used by the DB'''
    return {
        'identifier': person.identifier,
        'roles': list(map(lambda r: r.name, person.roles)),
        'automate': person.automate,
        **({'hand': list(map(card.to_db, person.hand))} if isinstance(person, Player) else {})
    }


def person_from_db(person: dict) -> Person:
    '''Convert the provided dict from the DB into a Person instance'''
    return Person(
        identifier=person['identifier'],
        automate=person['automate'],
        roles=set(map(lambda r: GameRole[r], person['roles']))
    )


def player_from_db(person: dict) -> Player:
    '''Convert the provided dict from the DB into a Player instance'''
    return Player(
        identifier=person['identifier'],
        automate=person['automate'],
        roles=set(map(lambda r: GameRole[r], person['roles'])),
        hand=list(map(card.from_db, person['hand']))
    )
