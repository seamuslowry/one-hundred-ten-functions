'''
Endpoint to start a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Start a 110 game
    '''
    user, game = parse_request(req)

    if user.identifier == game.organizer.identifier:
        game.start_game()

    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier, 0)))
