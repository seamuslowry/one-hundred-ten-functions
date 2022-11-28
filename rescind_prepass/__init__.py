'''
Endpoint to undo a pre-pass in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import Unpass
from app.services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Unpass in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    initial_event_knowledge = len(game.events)

    game.act(Unpass(user.identifier))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
