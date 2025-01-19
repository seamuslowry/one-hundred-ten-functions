'''
Endpoint to create a new game
'''
import json
import logging

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import serialize
from app.models import Accessibility, Game, GameRole
from app.parsers import parse_request
from app.services import GameService

bp = func.Blueprint()


@bp.route(route="create", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Create a new 110 game.
    '''
    logging.info('Initiating create game request.')

    identifier, *_ = parse_request(req)

    logging.debug('Creating game for %s', identifier)

    body = req.get_json()

    game = Game()
    game.join(identifier)
    game.people.add_role(identifier, GameRole.ORGANIZER)
    game.name = body.get('name', f'{identifier} Game')
    game.accessibility = Accessibility[body.get('accessibility', Accessibility.PUBLIC.name)]

    game = GameService.save(game)

    logging.debug('Game %s created successfully', game.seed)

    return func.HttpResponse(json.dumps(serialize.game(game, identifier)))
