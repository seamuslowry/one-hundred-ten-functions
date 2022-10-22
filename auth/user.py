'''
Pull out user-related information from the request headers.

Classes:
    User
    GoogleUser
'''

import base64
import json

import azure.functions as func


def parse_user_type(req: func.HttpRequest):
    '''Get the authentication provider for the user'''
    return req.headers.get("x-ms-client-principal-idp")


def parse_identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return req.headers.get("x-ms-client-principal-id")


def parse_name(req: func.HttpRequest):
    '''Get the user's name'''
    return get_claim(req, "name")


def parse_picture_url(req: func.HttpRequest):
    '''Get the URL for the user's picture'''
    return get_claim(req, "picture")


def get_claims(req: func.HttpRequest):
    '''Get the claims array from the request'''
    token = req.headers.get("x-ms-client-principal")
    return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []


def get_claim(req: func.HttpRequest, claim: str):
    '''Get a specific claim from the request'''
    claims = get_claims(req)
    return next((x for x in claims if x['typ'] == claim), {'val': None})['val']


class User:
    '''A class to interact with users using information from the request'''

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def to_json(self):
        '''Return a JSON representation of the user'''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a user object from a passed request'''
        if parse_user_type(req) == "google":
            return GoogleUser.from_request(req)

        raise NotImplementedError("Unauthenticated or authenticated with an unknown value")


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
            parse_name(req),
            parse_picture_url(req))
