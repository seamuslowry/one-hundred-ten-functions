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


def identifier(req: func.HttpRequest):
    '''Get the unique identifier for the user'''
    return req.headers.get("x-ms-client-principal-id")


def email(req: func.HttpRequest):
    '''Get the user's email'''
    return req.headers.get("x-ms-client-principal-name")


def name(req: func.HttpRequest):
    '''Get the user's name'''
    return __get_claim(req, "name")


def picture_url(req: func.HttpRequest):
    '''Get the URL for the user's picture'''
    return __get_claim(req, "picture")


def __get_claims(req: func.HttpRequest):
    token = req.headers.get("x-ms-client-principal")
    return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []


def __get_claim(req: func.HttpRequest, claim: str):
    claims = __get_claims(req)
    return next((x for x in claims if x['typ'] == claim), {'val': None})['val']
