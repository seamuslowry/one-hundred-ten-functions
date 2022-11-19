'''
Endpoint to invite players to a 110 game
'''
import json

import azure.functions as func

from decorators import catcher
from services import GameService, UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Invite to join a 110 game
    '''
    user = UserService.from_request(req)
    game = GameService.get(req.route_params['id'])

    body = req.get_json()
    invitees = body.get('invitees', [])

    for invitee in invitees:
        game.invite(user.identifier, invitee)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
