'''
Endpoint to invite players to a 110 game
'''
import json

import azure.functions as func

from app.decorators import catcher, parse_game, parse_user
from app.models import Game, User
from app.services import GameService


@catcher
@parse_game
@parse_user
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
