'''
Endpoint to invite players to a 110 game
'''
import json

import azure.functions as func

from app.decorators import auth, catcher, game_id
from app.models import Game, User
from app.services import GameService


@catcher
@game_id
@auth
def main(req: func.HttpRequest, user: User, game: Game) -> func.HttpResponse:
    '''
    Invite to join a 110 game
    '''

    body = req.get_json()
    invitees = body.get('invitees', [])

    for invitee in invitees:
        game.invite(user.identifier, invitee)
    game = GameService.save(game)

    return func.HttpResponse(json.dumps(GameService.json(game, user.identifier)))
