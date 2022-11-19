'''
Endpoint to start a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Start a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])

    if user.identifier == game.organizer.identifier:
        game.start_game()

    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
