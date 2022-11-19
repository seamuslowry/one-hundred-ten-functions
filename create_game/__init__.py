'''
Endpoint to create a new game
'''
import json
import logging

import azure.functions as func

from decorators import catcher
from models import Game, GameRole
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Create a new 110 game.
    '''
    logging.info('Initiating create game request.')

    user = UserService.from_request(req)

    logging.debug('Creating game for %s', user.identifier)

    game = Game()
    game.name = req.get_json().get('name', f'{user.name}\'s Game')
    game.join(user.identifier)
    game.people.add_role(user.identifier, GameRole.ORGANIZER)

    game = GameService.save(game)

    logging.debug('Game %s created successfully', game.seed)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
