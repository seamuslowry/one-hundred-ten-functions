'''Genericize handling of authorized user on a request'''
from typing import Callable

import azure.functions as func

from app.models import User
from app.services import UserService


def parse_user(function: Callable[[func.HttpRequest, User],
                                  func.HttpResponse]) -> Callable[[func.HttpRequest],
                                                                  func.HttpResponse]:
    '''Retrieve the user from the request and pass to the function'''
    def inner_function(req: func.HttpRequest):
        user = UserService.from_request(req)
        return function(req, user)
    return inner_function
