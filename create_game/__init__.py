'''
Expose a function for Azure Functions to call to create a new game

Functions:
    main(req) -> res
'''
import json
import logging

import azure.functions as func
from auth import user


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Currently, return found authentication information for the user.
    Eventually, create a new 110 game.
    '''
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(json.dumps({'id': user.identifier(req), 'identifier': user.email(
        req), 'name': user.name(req), 'picture': user.picture_url(req)}))
