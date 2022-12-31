'''Facilitate interaction with the user DB'''

import base64
from enum import Enum
from json import loads

import azure.functions as func

from app.mappers.db import deserialize, serialize
from app.models import GoogleUser, User
from app.services.cosmos import user_client
from app.services.mongo import m_user_client


class UserType(str, Enum):
    '''Enum value for partition keys'''
    GOOGLE = "google"
    UNKNOWN = "unknown"


MAX = 20


def from_request(req: func.HttpRequest) -> User:
    '''Create a user object from a passed request'''
    return save(__from_request(req))


def save(user: User) -> User:
    '''Save the provided user to the DB'''
    m_user_client.update_one({'id': user.identifier}, {'$set': serialize.user(user)}, upsert=True)
    return user


def search(search_text: str) -> list[User]:
    '''Retrieve the users with names like the provided'''
    return list(
        map(deserialize.user, m_user_client.find(
            {'name': {'$regex': search_text, '$options': 'i'}})))


def by_identifiers(identifiers: list[str]) -> list[User]:
    '''Retrieve the users with identifiers in the list provided'''
    return list(map(__from_db, user_client.query_items(
        "select * from user where array_contains(@identifiers, user.id) offset 0 limit @max",
        parameters=[
            {'name': '@identifiers', 'value': identifiers},
            {'name': '@max', 'value': MAX}
        ],
        enable_cross_partition_query=True
    )))


def json(user: User) -> dict:
    '''Return users as they can be provided to the client'''
    return {
        'id': user.identifier,
        'name': user.name,
        **({'picture_url': user.picture_url} if isinstance(user, GoogleUser) else {})
    }


def __from_request(req: func.HttpRequest) -> User:
    '''Create a user object from a passed request'''
    if __parse_user_type(req) == UserType.GOOGLE:
        return __google_user_from_request(req)

    return User(__parse_identifier(req), __parse_name(req))


def __from_db(user: dict) -> User:
    if user['type'] == UserType.GOOGLE:
        return GoogleUser(user['id'], user['name'], user['picture_url'])
    return User(user['id'], user['name'])


def __google_user_from_request(req: func.HttpRequest) -> GoogleUser:
    '''Create a Google user object from a passed request'''
    return GoogleUser(
        f'{UserType.GOOGLE}-{__parse_identifier(req)}',
        __get_claim(req, "name"),
        __get_claim(req, "picture"))


def __parse_user_type(req: func.HttpRequest):
    '''Get the authentication provider for the user'''
    return __get_header(req, "x-ms-client-principal-idp")


def __parse_identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return __get_header(req, "x-ms-client-principal-id")


def __parse_name(req: func.HttpRequest):
    '''Get the user's name'''
    return __get_header(req, "x-ms-client-principal-name")


def __get_claims(req: func.HttpRequest):
    '''Get the claims array from the request'''
    token = __get_header(req, "x-ms-client-principal")
    return loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []


def __get_claim(req: func.HttpRequest, claim: str):
    '''Get a specific claim from the request'''
    claims = __get_claims(req)
    return next((x for x in claims if x['typ'] == claim), {'val': ''})['val']


def __get_header(req: func.HttpRequest, key: str) -> str:
    '''Get a header with the provided key'''
    val = req.headers.get(key)
    if val:
        return val
    raise ValueError(f'Required header {key} not provided')
