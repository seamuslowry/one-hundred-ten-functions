'''
Endpoint to play a card in a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.models import Play
from app.services import CardService, GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Play a card in a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])
    initial_event_knowledge = len(game.events)

    body = req.get_json()

    game.act(Play(user.identifier, CardService.from_client(body.get('card'))))

    game = GameService.save(game)

    return func.HttpResponse(
        json.dumps(GameService.json(game, user.identifier, initial_event_knowledge)))
