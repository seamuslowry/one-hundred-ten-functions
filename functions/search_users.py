'''
Endpoint to get users from the DB
'''
import json

import azure.functions as func

from utils.decorators import catcher
from utils.mappers.client import serialize
from utils.services import UserService

bp = func.Blueprint()


@bp.route(route="users", methods=["GET"])
@catcher
def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Get users
    '''

    return func.HttpResponse(json.dumps(
        list(map(serialize.user, UserService.search(req.params.get('searchText', ''))))))
