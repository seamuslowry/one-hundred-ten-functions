'''Genericize handling of game exceptions'''
from typing import Callable

import azure.functions as func

from models import HundredAndTenError


def handle_exception(function: Callable[[func.HttpRequest],
                                        func.HttpResponse]) -> Callable[[func.HttpRequest],
                                                                        func.HttpResponse]:
    '''Handle a game exception by returning a 400'''
    def inner_function(req: func.HttpRequest):
        try:
            return function(req)
        except HundredAndTenError as exception:
            return func.HttpResponse(status_code=400, body=str(exception))
    return inner_function
