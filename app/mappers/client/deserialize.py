'''A module to convert client objects to models'''

import azure.functions as func

from app import models
from app.dtos import client
from app.mappers.shared.deserialize import card as __deserialize_card


def user_id(req: func.HttpRequest) -> str:
    '''Create a user object from a passed request'''
    return __parse_identifier(req)


def card(c_card: client.Card) -> models.Card:
    '''Create a card object from a passed client card'''
    return __deserialize_card(c_card)


def __parse_identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return __get_header(req, "x-ms-client-principal-id")


def __get_header(req: func.HttpRequest, key: str) -> str:
    '''Get a header with the provided key'''
    val = req.headers.get(key)
    if val:
        return val
    raise ValueError(f'Required header {key} not provided')
