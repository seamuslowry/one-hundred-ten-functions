import azure.functions as func
import base64
import json

def id(req: func.HttpRequest):
  return req.headers.get("x-ms-client-principal-id")

def identifier(req: func.HttpRequest):
  return req.headers.get("x-ms-client-principal-name")

def name(req: func.HttpRequest):
  return __get_claim(req, "name")

def picture_url(req: func.HttpRequest):
  return __get_claim(req, "picture")

def __get_claims(req: func.HttpRequest):
  token = req.headers.get("x-ms-client-principal")
  return json.loads(base64.b64decode(token).decode('utf-8'))['claims'] if token else []

def __get_claim(req: func.HttpRequest, claim: str):
  claims = __get_claims(req)
  return next((x for x in claims if x['typ'] == claim), {'val': None})['val']