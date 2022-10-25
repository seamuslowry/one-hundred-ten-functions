'''Helpers to perform common functions during testing'''
from typing import Optional

import azure.functions as func


def build_request(
        method='GET', url='', body=b'', headers: Optional[dict[str, str]] = None, params=None):
    '''Build a request defaulting common values for the arguments'''
    return func.HttpRequest(
        method=method, body=body, url=url,
        headers={'x-ms-client-principal-idp': 'unknown', 'x-ms-client-principal-id': 'id',
                 'x-ms-client-principal-name': 'name',
                 **(headers or {})},
        params=params)
