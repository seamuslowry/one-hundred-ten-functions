'''Facilitate interaction with persons in the DB'''

from typing import Optional, Union

from hundredandten.constants import GameRole, RoundRole
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
        roles=set(map(lambda r: RoundRole[r], person['roles'])),
        hand=list(map(card.from_db, person['hand']))
    )


def json(person: Union[Person, Player], identifier: Optional[str] = '') -> dict:
    '''Convert the provided person or player into the structure it should provide the client'''
    return {
        'identifier': person.identifier,
        'roles': list(map(lambda r: r.name, person.roles)),
        # hand should only be provided if the client is this individual
        **({'hand': list(map(card.json, person.hand))}
           if identifier == person.identifier and isinstance(person, Player) else {})
    }
