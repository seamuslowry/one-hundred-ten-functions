'''Facilitate interaction with persons in the DB'''

from typing import Union

from hundredandten.group import Person, Player

from service import card


def to_db_dict(person: Union[Person, Player]) -> dict:
    '''Convert the provided person into the dict structure used by the DB'''
    return {
        'identifier': person.identifier,
        'roles': list(map(lambda r: r.name, person.roles)),
        'automate': person.automate,
        **({'hand': list(map(card.to_db_dict, person.hand))} if isinstance(person, Player) else {})
    }
