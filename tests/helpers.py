'''Helpers to perform common functions during testing'''
import json
from typing import Optional

import azure.functions as func

DEFAULT_ID = 'id'


def build_request(method='GET', body=b'', route_params=None,
                  headers: Optional[dict[str, str]] = None, params=None):
    '''Build a request defaulting common values for the arguments'''
    return func.HttpRequest(
        method=method, body=body, route_params=route_params, url='',
        headers={'x-ms-client-principal-idp': 'unknown', 'x-ms-client-principal-id': DEFAULT_ID,
                 'x-ms-client-principal-name': 'name',
                 **(headers or {})},
        params=params)


def read_response_body(body: bytes) -> dict:
    '''Read the response body and return it as a dict'''
    return json.loads(body.decode('utf-8'))


def return_input(param):
    '''Return the parameter; useful for mocks'''
    return param
