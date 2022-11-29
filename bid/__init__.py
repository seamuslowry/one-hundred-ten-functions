'''
Endpoint to place a bid in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import Bid, BidAmount
from app.parsers import parse_request
from app.services import GameService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Bid in a 110 game
    '''
    user, game, initial_event_knowledge = parse_request(req)

    body = req.get_json()

    game.act(Bid(user.identifier, BidAmount(body['amount'])))

    game = GameService.save(game)

    return func.HttpResponse(json.dumps(
        GameService.json(
            game,
            user.identifier,
            initial_event_knowledge)))
