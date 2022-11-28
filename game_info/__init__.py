'''
Endpoint to retrieve a game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Retrieve 110 game.
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
