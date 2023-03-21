'''
Endpoint to update yourself in the DB
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import deserialize, serialize
from app.services import UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Update the user
    '''

    return func.HttpResponse(json.dumps(
        serialize.user(UserService.save(deserialize.user(req, req.get_json())))))
