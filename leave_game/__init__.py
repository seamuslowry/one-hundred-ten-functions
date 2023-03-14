'''
Endpoint to leave a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import serialize
from app.models import RoundStatus
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Leave a 110 game
    '''
    identifier, game = parse_request(req)
    initial_event_knowledge = len(game.events)
    if isinstance(game.status, RoundStatus):
        game.automate(identifier)
    else:
        game.leave(identifier)
    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(serialize.game(game, identifier, initial_event_knowledge)))
