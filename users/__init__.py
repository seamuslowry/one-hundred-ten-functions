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

    return func.HttpResponse(json.dumps(
        list(map(UserService.json, UserService.search(req.params.get('searchText', ''))))))
