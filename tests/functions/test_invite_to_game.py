'''Invite to game unit tests'''
import json
from unittest import TestCase, mock

from invite_to_game import main
from models import Game, GameRole, Group, Person
from tests.helpers import (DEFAULT_ID, DEFAULT_USER, build_request,
                           read_response_body, return_input)


class TestInviteToGame(TestCase):
    '''Invite to Game unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.UserService.save', mock.Mock(side_effect=return_input))
    @mock.patch('services.GameService.get', mock.Mock(
        return_value=Game(people=Group([Person(DEFAULT_ID, roles={GameRole.PLAYER})]))))
    @mock.patch('services.UserService.get', mock.Mock(return_value=DEFAULT_USER))
    def test_invites_game(self, game_save):
        '''On hitting the invite endpoint the logged in player invites the listed users'''
        invitee = 'invitee'
        req = build_request(
            route_params={'id': 'id'},
            body=json.dumps({'invitees': [invitee]}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertIn(invitee, map(lambda pd: pd['identifier'], resp_dict['invitees']))
