'''Facilitate interaction with the game DB'''

from hundredandten import HundredAndTen
from hundredandten.constants import Accessibility
from hundredandten.group import Group

from service import person
from service import round as round_service
from service.cosmos import game_client


def save(game: HundredAndTen) -> HundredAndTen:
    '''Save the provided game to the DB'''
    return from_db(game_client.upsert_item(to_db(game)))


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
        accessibility=Accessibility[game['accessibility']],
        people=Group(list(map(person.person_from_db, game['people']))),
        rounds=list(map(round_service.from_db, game['rounds']))
    )


def to_client(game: HundredAndTen) -> dict:
    '''Convert the provided game into the structure it should provide the client'''
    return to_db(game)
