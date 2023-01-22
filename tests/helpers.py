'''Helpers to perform common functions during testing'''
import json
from typing import Optional

import azure.functions as func

import create_game
import leave_game
import start_game
from app.dtos.client import CompletedGame, StartedGame, WaitingGame

DEFAULT_ID = 'id'
DEFAULT_NAME = 'name'


def build_request(method='GET', body=None, route_params=None,
                  headers: Optional[dict[str, str]] = None, params=None):
    '''Build a request defaulting common values for the arguments'''
    return func.HttpRequest(
        method=method, body=json.dumps(body).encode('utf-8') if body else b'',
        route_params=route_params, url='',
        headers={'x-ms-client-principal-idp': 'unknown', 'x-ms-client-principal-id': DEFAULT_ID,
                 'x-ms-client-principal-name': DEFAULT_NAME, **(headers or {})},
        params=params)


def read_response_body(body: bytes):
    '''Read the response body and return it as a dict'''
    return json.loads(body.decode('utf-8'))


def lobby_game(organizer: str = DEFAULT_ID, organizer_name: str = DEFAULT_NAME) -> WaitingGame:
    '''Get a started game waiting for the players'''
    resp = create_game.main(
        build_request(
            headers={'x-ms-client-principal-id': organizer,
                     'x-ms-client-principal-name': organizer_name},
            body={'name': 'test game'}))
    return read_response_body(resp.get_body())


def started_game() -> StartedGame:
    '''Get a started game waiting for the first move'''
    created_game: WaitingGame = lobby_game()
    resp = start_game.main(
        build_request(
            route_params={'game_id': created_game['id']},
            headers={'x-ms-client-principal-id': created_game['organizer']['identifier']}))
    return read_response_body(resp.get_body())


def completed_game() -> CompletedGame:
    '''Get a completed game'''
    game = started_game()

    active_player = game['round']['active_player']
    assert active_player

    resp = leave_game.main(
        build_request(
            route_params={'game_id': game['id']},
            headers={'x-ms-client-principal-id': active_player['identifier']}))
    return read_response_body(resp.get_body())
