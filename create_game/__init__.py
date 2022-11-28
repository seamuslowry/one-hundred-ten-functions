'''
Endpoint to create a new game
'''
import json
import logging

import azure.functions as func

from app.decorators import catcher
from app.models import Accessibility, Game, GameRole
from app.services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Create a new 110 game.
    '''
    logging.info('Initiating create game request.')

    user = UserService.from_request(req)

    logging.debug('Creating game for %s', user.identifier)

    body = req.get_json()

    game = Game()
    game.join(user.identifier)
    game.people.add_role(user.identifier, GameRole.ORGANIZER)
    game.name = body.get('name', f'{user.name}\'s Game')
    game.accessibility = Accessibility[body.get('accessibility', Accessibility.PUBLIC.name)]

    game = GameService.save(game)

    logging.debug('Game %s created successfully', game.seed)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
