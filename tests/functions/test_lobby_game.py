'''Lobby Game unit tests'''
from unittest import TestCase

import create_game
import invite_to_game
from app.dtos.client import WaitingGame
from app.models import GameStatus
from tests.helpers import build_request, read_response_body


class TestLobbyGame(TestCase):
    '''Unit tests to ensure games that are waiting for players work as expected'''

    def test_create_game(self):
        '''New game can be created'''
        organizer = 'organizer'
        resp = create_game.main(
            build_request(
                headers={'x-ms-client-principal-id': organizer},
                body={'name': 'create test'}))
        game: WaitingGame = read_response_body(resp.get_body())

        self.assertEqual(organizer, game['organizer']['identifier'])
        self.assertEqual(0, len(game['players']))
        self.assertEqual(0, len(game['invitees']))
        self.assertEqual(GameStatus.WAITING_FOR_PLAYERS.name, game['status'])

    def test_organizer_invite_to_game(self):
        '''Organizer can be invite players to a game'''
        invitee = 'invitee'

        resp = create_game.main(
            build_request(
                body={'name': 'invite test'}))
        created_game: WaitingGame = read_response_body(resp.get_body())

        resp = invite_to_game.main(
            build_request(
                route_params={'game_id': created_game['id']},
                headers={'x-ms-client-principal-id': created_game['organizer']['identifier']},
                body={'invitees': [invitee]}))
        invited_game: WaitingGame = read_response_body(resp.get_body())

        self.assertEqual(created_game['id'], invited_game['id'])
        self.assertEqual(0, len(invited_game['players']))
        self.assertEqual(1, len(invited_game['invitees']))
        self.assertEqual(invitee, invited_game['invitees'][0]['identifier'])
        self.assertEqual(GameStatus.WAITING_FOR_PLAYERS.name, invited_game['status'])

    def test_invitee_invite_to_game(self):
        '''Invited players cannot invite players to a game'''
        invitee = 'invitee'
        second_invitee = 'second'

        resp = create_game.main(
            build_request(
                body={'name': 'invite test'}))
        created_game: WaitingGame = read_response_body(resp.get_body())

        # invite the original
        resp = invite_to_game.main(
            build_request(
                route_params={'game_id': created_game['id']},
                headers={'x-ms-client-principal-id': created_game['organizer']['identifier']},
                body={'invitees': [invitee]}))

        # new invitee cannot invite
        failed_invite = invite_to_game.main(
            build_request(
                route_params={'game_id': created_game['id']},
                headers={'x-ms-client-principal-id': invitee},
                body={'invitees': [second_invitee]}))
        self.assertEqual(400, failed_invite.status_code)
