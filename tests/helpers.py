'''Helpers to perform common functions during testing'''
import azure.functions as func


def build_request(method='GET', url='', body=b'', headers=None, params=None):
    '''Build a request defaulting common values for the arguments'''
    return func.HttpRequest(
        method=method,
        body=body,
        url=url,
        headers=headers,
        params=params
    )
