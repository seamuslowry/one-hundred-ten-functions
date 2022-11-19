'''
Endpoint to leave a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from models import RoundStatus
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Leave a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    if isinstance(game.status, RoundStatus):
        game.automate(user.identifier)
    else:
        game.leave(user.identifier)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
