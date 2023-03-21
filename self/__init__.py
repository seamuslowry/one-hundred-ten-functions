'''
Endpoint to update yourself in the DB
'''
import json

import azure.functions as func

from app.decorators import catcher
from app.mappers.client import deserialize, serialize
from app.parsers import parse_request
from app.services import UserService


@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Create or update the user
    '''

    overwrite = req.method.upper() == 'PUT'

    identifier, *_ = parse_request(req)

    existing_user = UserService.by_identifier(identifier)
    provided_user = deserialize.user(req, req.get_json())

    save_user = provided_user if overwrite or not existing_user else existing_user

    return func.HttpResponse(json.dumps(
        serialize.user(UserService.save(save_user))))
