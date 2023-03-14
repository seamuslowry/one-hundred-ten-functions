'''
Parse models off an HTTP request
'''
from typing import Tuple

import azure.functions as func

from app.mappers.client import deserialize
from app.models import Game
from app.services import GameService


def parse(req: func.HttpRequest) -> Tuple[str, Game]:
    '''
    Parse the request for the models
    '''
    game_id = req.route_params.get('game_id', None)
    game = GameService.get(game_id) if game_id else Game()

    return (deserialize.user_id(req), game)
