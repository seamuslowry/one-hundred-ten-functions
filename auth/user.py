'''Pull out user-related information from the request headers.'''

import base64
import json

import azure.functions as func
from serialization.serializable import Serializable


class User(Serializable):
    '''A class to interact with users using information from the request'''

    def __init__(self, identifier: str, name: str):
        self.identifier = identifier
        self.name = name

    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a user object from a passed request'''
        if parse_user_type(req) == "google":
            return GoogleUser.from_request(req)

        return User(parse_identifier(req), parse_name(req))


class GoogleUser(User):
    '''A class to interact with Google authenticated users using information from the request'''

    def __init__(self, identifier, name, picture_url):
        super().__init__(identifier, name)
        self.picture_url = picture_url

    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a Google user object from a passed request'''
        return GoogleUser(
            parse_identifier(req),
            get_claim(req, "name"),
            get_claim(req, "picture"))


def parse_user_type(req: func.HttpRequest):
    '''Get the authentication provider for the user'''
    return get_header(req, "x-ms-client-principal-idp")


def parse_identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return get_header(req, "x-ms-client-principal-id")


def parse_name(req: func.HttpRequest):
    '''Get the user's name'''
    return get_header(req, "x-ms-client-principal-name")


def get_claims(req: func.HttpRequest):
    '''Get the claims array from the request'''
    token = get_header(req, "x-ms-client-principal")
    return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []


def get_claim(req: func.HttpRequest, claim: str):
    '''Get a specific claim from the request'''
    claims = get_claims(req)
    return next((x for x in claims if x['typ'] == claim), {'val': None})['val']


def get_header(req: func.HttpRequest, key: str) -> str:
    '''Get a header with the provided key'''
    val = req.headers.get(key)
    if val:
        return val
    raise ValueError(f'Required header {key} not provided')
