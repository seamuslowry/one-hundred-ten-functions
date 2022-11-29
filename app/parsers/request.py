'''
Parse models off an HTTP request
'''
from typing import Tuple

import azure.functions as func

from app.models import Game, User
from app.services import GameService, UserService


def parse(req: func.HttpRequest) -> Tuple[User, Game, int]:
    '''
    Parse the request for the models
    '''
    game_id = req.route_params.get('id', None)
    game = GameService.get(game_id) if game_id else Game()
    event_count = len(game.events)

    return (UserService.from_request(req), game, event_count)
