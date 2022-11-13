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
    Create a new 110 game.
    '''
    logging.info('Initiating create game request.')

    user = User.from_request(req)

    logging.debug('Creating game for %s', user.identifier)

    game = HundredAndTen()
    game.join(user.identifier)

    db_game = GameService.to_db(game)

    cosmos.set(func.Document.from_dict(db_game))

    logging.debug('Game %s created successfully', db_game['id'])

    return func.HttpResponse(json.dumps(db_game))
