'''
Endpoint to undo a pre-pass in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import Unpass
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Unpass in a 110 game
    '''
    user, game, initial_event_knowledge = parse_request(req)

    game.act(Unpass(user.identifier))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
