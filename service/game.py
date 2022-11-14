'''Facilitate interaction with the game DB'''

from hundredandten import HundredAndTen
from hundredandten.group import Group

from service import person
from service import round as round_service


def to_db(game: HundredAndTen) -> dict:
    '''Convert the provided game into the dict structure used by the DB'''
    return {
        'id': game.seed,
        'seed': game.seed,
        'accessibility': game.accessibility.name,
        'people': list(map(person.to_db, game.people)),
        'rounds': list(map(round_service.to_db, game.rounds))
    }


def from_db(game: dict) -> HundredAndTen:
    '''Convert the provided dict from the DB into a HundredAndTen instance'''
    return HundredAndTen(
        seed=game['seed'],
        accessibility=game['accessibility'],
        people=Group(list(map(person.person_from_db, game['people']))),
        rounds=list(map(round_service.from_db, game['rounds']))
    )