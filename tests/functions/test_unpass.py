'''Unpassing unit tests'''
from unittest import TestCase, mock

from app.models import RoundStatus
from rescind_prepass import main
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)


class TestUnpass(TestCase):
    '''Unpassing unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('rescind_prepass.parse_request',
                mock.Mock(return_value=(DEFAULT_USER, game(RoundStatus.BIDDING))))
    def test_unpass(self, game_save):
        '''On hitting the unpass endpoint, the logged in user unpasses'''
        req = build_request(route_params={'game_id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertEqual(DEFAULT_USER.identifier, resp_dict['round']['active_player']['identifier'])
        self.assertFalse(resp_dict['round']['active_player']['prepassed'])
        self.assertEqual([], resp_dict['results'])
