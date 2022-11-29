'''
Endpoint to discard cards in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import Discard
from app.parsers import parse_request
from app.services import CardService, GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Dsicard in a 110 game
    '''
    user, game, initial_event_knowledge = parse_request(req)

    body = req.get_json()

    game.act(Discard(user.identifier, [CardService.from_client(c) for c in body.get('cards')]))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
