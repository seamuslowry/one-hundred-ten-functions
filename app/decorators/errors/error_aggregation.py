'''Transfrom errors into HTTP responses'''
from typing import Callable

import azure.functions as func

from app.decorators.errors.hundred_and_ten_error import \
    handle_error as handle_game_error


def handle_error(function: Callable[[func.HttpRequest],
                                    func.HttpResponse]) -> Callable[[func.HttpRequest],
                                                                    func.HttpResponse]:
    '''Aggregate error handlers into one decorator'''
    return handle_game_error(function)
