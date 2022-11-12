'''
Expose a function for Azure Functions to call to create a new game
'''
import logging
import uuid

import azure.functions as func
from hundredandten import HundredAndTen

from auth.user import User


def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    '''
    Currently, return found authentication information for the user.
    Eventually, create a new 110 game.
    '''
    logging.info('Python HTTP trigger function processed a request.')

    user = User.from_request(req)

    game = HundredAndTen()
    game.join(user.identifier)

    cosmos.set(func.Document.from_dict({
        'id': game.seed,
        'seed': game.seed,
        'people': list(map(
            lambda p: {
                'identifier': p.identifier,
                'roles': list(map(lambda r: r.name, p.roles)),
                'automate': p.automate
            },
            game.people)),
        'rounds': []
    }))

    return func.HttpResponse(User.from_request(req).to_json())
