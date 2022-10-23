'''
Expose a function for Azure Functions to call to create a new game
'''
import logging
import uuid

import azure.functions as func
from auth.user import User


def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    '''
    Currently, return found authentication information for the user.
    Eventually, create a new 110 game.
    '''
    logging.info('Python HTTP trigger function processed a request.')

    cosmos.set(func.Document.from_dict({
        'id': '1',
        'uuid': str(uuid.uuid4())
    }))

    return func.HttpResponse(User.from_request(req).to_json())
