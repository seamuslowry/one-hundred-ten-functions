'''Facilitate interaction with the person DB'''

from hundredandten.group import Person


def to_db_dict(person: Person) -> dict:
    '''Convert the provided person into the dict structure used by the DB'''
    return {
        'identifier': person.identifier,
        'roles': list(map(lambda r: r.name, person.roles)),
        'automate': person.automate
    }
