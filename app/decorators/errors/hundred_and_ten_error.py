'''Genericize handling of game errors'''
from typing import Callable

import azure.functions as func
from typing_extensions import Concatenate, ParamSpec

from app.models import HundredAndTenError

Param = ParamSpec("Param")


def handle_error(
    function: Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]
) -> Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]:
    '''Handle a game error by returning a 400'''
    def inner_function(
            req: func.HttpRequest, *args: Param.args, **kwargs: Param.kwargs) -> func.HttpResponse:
        try:
            return function(req, *args, **kwargs)
        except HundredAndTenError as exception:
            return func.HttpResponse(status_code=400, body=str(exception))
    return inner_function
