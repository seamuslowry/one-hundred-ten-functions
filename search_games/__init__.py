'''
Endpoint to get games from the DB
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Get games
    '''
    user, *_ = parse_request(req)

    return func.HttpResponse(
        json.dumps(
            list(
                map(
                    lambda g: GameService.json(g, user.identifier),
                    GameService.search(GameService.SearchType.WAITING, user.identifier)))))
