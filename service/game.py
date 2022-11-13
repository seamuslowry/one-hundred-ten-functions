'''Facilitate interaction with the game DB'''

from hundredandten import HundredAndTen

from service import person


def to_db(game: HundredAndTen) -> dict:
    '''Convert the provided game into the dict structure used by the DB'''
    return {
        'id': game.seed,
        'seed': game.seed,
        'accessibility': game.accessibility.name,
        'people': list(map(person.to_db, game.people)),
        'rounds': []
    }
