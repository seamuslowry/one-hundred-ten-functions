'''
Endpoint to join a 110 game
'''
import json

import azure.functions as func

from services import GameService, UserService


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Join a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    game.join(user.identifier)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
