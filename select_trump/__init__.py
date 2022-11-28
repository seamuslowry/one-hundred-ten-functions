'''
Endpoint to select trump in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import SelectableSuit, SelectTrump
from app.services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Select trump in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    initial_event_knowledge = len(game.events)

    body = req.get_json()

    game.act(SelectTrump(user.identifier, SelectableSuit[body['suit']]))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
