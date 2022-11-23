'''
Endpoint to undo a pre-pass in a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from models import Unpass
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Unpass in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])

    game.act(Unpass(user.identifier))

    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
