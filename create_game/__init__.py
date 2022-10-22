'''
Expose a function for Azure Functions to call to create a new game
'''
import json
import logging

import azure.functions as func
from auth.user import User


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Currently, return found authentication information for the user.
    Eventually, create a new 110 game.
    '''
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(User.from_request(req).to_json())
