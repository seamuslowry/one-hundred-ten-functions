'''
Endpoint to join a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Join a 110 game
    '''
    user, game, *_ = parse_request(req)
    game.join(user.identifier)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
