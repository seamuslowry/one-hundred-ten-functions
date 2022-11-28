'''Transfrom errors into HTTP responses'''
from typing import Callable

import azure.functions as func
from typing_extensions import Concatenate, ParamSpec

from app.decorators.errors.hundred_and_ten_error import \
    handle_error as handle_game_error

Param = ParamSpec("Param")


def handle_error(
    function: Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]
) -> Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]:
    '''Aggregate error handlers into one decorator'''
    return handle_game_error(function)
