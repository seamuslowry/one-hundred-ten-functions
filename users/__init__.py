'''
Endpoint to get users from the DB
'''
import json

import azure.functions as func

from decorators import catcher
from services import UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Get users
    '''
    body = req.get_json()

    return func.HttpResponse(json.dumps(
        map(UserService.json, UserService.search(body.get('text', '')))))
