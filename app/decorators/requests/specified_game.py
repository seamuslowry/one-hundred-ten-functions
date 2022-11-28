'''Genericize retrieving a game from a request'''
from typing import Callable

import azure.functions as func
from typing_extensions import Concatenate, ParamSpec

from app.models import Game
from app.services import GameService

Param = ParamSpec("Param")


def parse_game(
        function: Callable[Concatenate[func.HttpRequest, Game, Param], func.HttpResponse]
) -> Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]:
    '''Retrieve the game from the request and pass to the function'''
    def inner_function(
            req: func.HttpRequest, *args: Param.args, **kwargs: Param.kwargs) -> func.HttpResponse:
        game = GameService.get(req.route_params['id'])
        return function(req, game, *args, **kwargs)
    return inner_function
