'''Transfrom exceptions into HTTP responses'''
from typing import Callable

import azure.functions as func

from decorators.hundred_and_ten_exception import \
    handle_exception as handle_game_exception


def handle_exception(function: Callable[[func.HttpRequest],
                                        func.HttpResponse]) -> Callable[[func.HttpRequest],
                                                                        func.HttpResponse]:
    '''Aggregate exception error handlers into one decorator'''
    return handle_game_exception(function)
