'''
Expose a function for Azure Functions to call to create a new game
'''
import json
import logging

import azure.functions as func
from hundredandten import HundredAndTen

from auth.user import User
from service import GameService


def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    '''
    Currently, return found authentication information for the user.
    Eventually, create a new 110 game.
    '''
    logging.info('Python HTTP trigger function processed a request.')

    user = User.from_request(req)

    game = HundredAndTen()
    game.join(user.identifier)

    db_game = GameService.to_db_dict(game)

    cosmos.set(func.Document.from_dict(db_game))

    return func.HttpResponse(json.dumps(db_game))
