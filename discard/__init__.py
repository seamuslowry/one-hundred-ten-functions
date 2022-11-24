'''
Endpoint to discard cards in a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from models import Discard
from services import CardService, GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Dsicard in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    initial_event_knowledge = len(game.events)

    body = req.get_json()

    game.act(Discard(user.identifier, [CardService.from_client(c) for c in body.get('cards')]))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
