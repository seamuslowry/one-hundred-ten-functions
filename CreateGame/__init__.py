import json
import logging
from auth import user

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(json.dumps({'id': user.id(req), 'identifier': user.identifier(req), 'name': user.name(req), 'picture': user.picture_url(req)}))