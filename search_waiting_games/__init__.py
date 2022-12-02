'''
Endpoint to get games from the DB
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import GameRole
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Get games
    '''
    user, *_ = parse_request(req)

    body = req.get_json()
    string_role = body.get('gameRole', None)
    role = GameRole[string_role] if string_role else None
    max_count = body.get('max', 20)
    search_text = body.get('searchText', '')

    return func.HttpResponse(
        json.dumps(
            list(
                map(
                    lambda g: GameService.json(g, user.identifier),
                    GameService.search_waiting(search_text, max_count, user.identifier, role)))))
