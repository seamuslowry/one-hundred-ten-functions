'''
Endpoint to create a new game
'''
import json
import logging

import azure.functions as func

from app.decorators import auth, catcher
from app.models import Accessibility, Game, GameRole, User
from app.services import GameService


@catcher
@auth
def main(req: func.HttpRequest, user: User) -> func.HttpResponse:
    '''
    Create a new 110 game.
    '''
    logging.info('Initiating create game request.')
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
