'''
Endpoint to play a card in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import serialize
from app.models import Play
from app.parsers import parse_request
from app.services import CardService, GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Play a card in a 110 game
    '''
    user, game = parse_request(req)
    initial_event_knowledge = len(game.events)

    body = req.get_json()

    game.act(Play(user.identifier, CardService.from_client(body.get('card'))))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(serialize.game(game, user.identifier, initial_event_knowledge)))
