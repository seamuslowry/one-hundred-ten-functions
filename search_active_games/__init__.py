'''
Endpoint to get active games from the DB
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Get active games
    '''
    user, *_ = parse_request(req)

    body = req.get_json()
    max_count = body.get('max', 20)
    search_text = body.get('searchText', '')
    active = body.get('active', True)

    return func.HttpResponse(
        json.dumps(
            list(map(lambda g: GameService.json(g, user.identifier),
                     GameService.search_playing(search_text, max_count, user.identifier, active)))))
