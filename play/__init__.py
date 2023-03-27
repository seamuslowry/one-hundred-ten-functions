'''
Endpoint to play a card in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import deserialize, serialize
from app.models import Play
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Play a card in a 110 game
    '''
    identifier, game = parse_request(req)
    initial_event_knowledge = len(game.events)

    body = req.get_json()

    game.act(Play(identifier, deserialize.card(body.get('card'))))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(serialize.game(game, identifier, initial_event_knowledge)))
