'''
Endpoint to retrieve all events a game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.parsers import parse_request
from app.services import EventService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Retrieve events on a 110 game.
    '''
    user, game = parse_request(req)

    return func.HttpResponse(
        json.dumps(EventService.json(game.events, user.identifier)))
