'''Facilitate interaction with the game DB'''

from models import Accessibility, Game, Group
from services import person
from services import round as round_service
from services.cosmos import game_client


def save(game: Game) -> Game:
    '''Save the provided game to the DB'''
    return from_db(game_client.upsert_item(to_db(game)))


def to_db(game: Game) -> dict:
    '''Convert the provided game into the dict structure used by the DB'''
    return {
        'id': game.id,
        'name': game.name,
        'seed': game.seed,
        'accessibility': game.accessibility.name,
        'people': list(map(person.to_db, game.people)),
        'rounds': list(map(round_service.to_db, game.rounds))
    }


def from_db(game: dict) -> Game:
    '''Convert the provided dict from the DB into a Game instance'''
    return Game(
        id=game['id'],
        name=game['name'],
        seed=game['seed'],
        accessibility=Accessibility[game['accessibility']],
        people=Group(list(map(person.person_from_db, game['people']))),
        rounds=list(map(round_service.from_db, game['rounds']))
    )


def json(game: Game) -> dict:
    '''Convert the provided game into the structure it should provide the client'''
    return {
        'id': game.id,
        'name': game.name,
        'accessibility': game.accessibility.name,
        'people': list(map(person.json, game.people)),
        'rounds': list(map(round_service.json, game.rounds))
    }
