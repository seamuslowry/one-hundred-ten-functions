'''
Endpoint to select trump in a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from models import SelectableSuit, SelectTrump
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Select trump in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])

    body = req.get_json()

    game.act(SelectTrump(user.identifier, SelectableSuit[body['suit']]))

    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
