'''
Endpoint to invite players to a 110 game
'''
import json

import azure.functions as func

from app.decorators import auth, catcher
from app.models import User
from app.services import GameService, UserService


@catcher
@auth
def main(req: func.HttpRequest, user: User) -> func.HttpResponse:
    '''
    Invite to join a 110 game
    '''
    game = GameService.get(req.route_params['id'])

    body = req.get_json()
    invitees = body.get('invitees', [])

    for invitee in invitees:
        game.invite(user.identifier, invitee)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
