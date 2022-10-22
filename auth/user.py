'''
Pull out user-related information from the request headers.

Functions:
  identifier(req) -> string
  email(req) -> string
  name(req) -> string
  picture_url -> string
'''

import base64
import json

import azure.functions as func


class User:
    '''A class to interact with users using information from the request'''

    def __init__(self, identifier, email, name, picture_url):
        self.identifier = identifier
        self.email = email
        self.name = name
        self.picture_url = picture_url

    @staticmethod
    def from_request(req: func.HttpRequest):
        '''Create a user object from a passed request'''
        return User(
            User.__identifier(req),
            User.__email(req),
            User.__name(req),
            User.__picture_url(req))

    @staticmethod
    def __identifier(req: func.HttpRequest):
        '''Get the unique identifier for the user'''
        return req.headers.get("x-ms-client-principal-id")

    @staticmethod
    def __email(req: func.HttpRequest):
        '''Get the user's email'''
        return req.headers.get("x-ms-client-principal-name")

    @staticmethod
    def __name(req: func.HttpRequest):
        '''Get the user's name'''
        return User.__get_claim(req, "name")

    @staticmethod
    def __picture_url(req: func.HttpRequest):
        '''Get the URL for the user's picture'''
        return User.__get_claim(req, "picture")

    @staticmethod
    def __get_claims(req: func.HttpRequest):
        token = req.headers.get("x-ms-client-principal")
        return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []

    @staticmethod
    def __get_claim(req: func.HttpRequest, claim: str):
        claims = User.__get_claims(req)
        return next((x for x in claims if x['typ'] == claim), {'val': None})['val']
