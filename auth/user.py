'''
Pull out user-related information from the request headers.

Classes:
    User
    GoogleUser
'''

import base64
import json

import azure.functions as func


class User:
    '''A class to interact with users using information from the request'''

    def __init__(self, identifier, name, picture_url):
        self.identifier = identifier
        self.name = name
        self.picture_url = picture_url

    def to_json(self):
        '''Return a JSON representation of the user'''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a user object from a passed request'''
        if __user_type(req) == "google":
            return GoogleUser.from_request(req)

        raise NotImplementedError()


class GoogleUser(User):
    '''A class to interact with Google authenticated users using information from the request'''
    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a Google user object from a passed request'''
        return GoogleUser(
            __identifier(req),
            __name(req),
            __picture_url(req))


def __user_type(req: func.HttpRequest):
    '''Get the authentication provider for the user'''
    return req.headers.get("x-ms-client-principal-idp")


def __identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return req.headers.get("x-ms-client-principal-id")


def __name(req: func.HttpRequest):
    '''Get the user's name'''
    return __get_claim(req, "name")


def __picture_url(req: func.HttpRequest):
    '''Get the URL for the user's picture'''
    return __get_claim(req, "picture")


def __get_claims(req: func.HttpRequest):
    token = req.headers.get("x-ms-client-principal")
    return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []


def __get_claim(req: func.HttpRequest, claim: str):
    claims = __get_claims(req)
    return next((x for x in claims if x['typ'] == claim), {'val': None})['val']
