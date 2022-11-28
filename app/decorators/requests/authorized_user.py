'''Genericize handling of authorized user on a request'''
from typing import Callable

import azure.functions as func
from typing_extensions import Concatenate, ParamSpec

from app.models import User
from app.services import UserService

Param = ParamSpec("Param")


def parse_user(
        function: Callable[Concatenate[func.HttpRequest, User, Param], func.HttpResponse]
) -> Callable[Concatenate[func.HttpRequest, Param], func.HttpResponse]:
    '''Retrieve the user from the request and pass to the function'''
    def inner_function(
            req: func.HttpRequest, *args: Param.args, **kwargs: Param.kwargs) -> func.HttpResponse:
        user = UserService.from_request(req)
        return function(req, user, *args, **kwargs)
    return inner_function
