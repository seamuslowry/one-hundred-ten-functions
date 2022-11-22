'''Unpassing unit tests'''
from unittest import TestCase, mock

from models import RoundStatus
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)
from unpass import main


class TestUnpass(TestCase):
    '''Unpassing unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.GameService.get', mock.Mock(
        return_value=game(RoundStatus.BIDDING)))
    @mock.patch('services.UserService.from_request', mock.Mock(return_value=DEFAULT_USER))
    @mock.patch('services.UserService.get', mock.Mock(return_value=DEFAULT_USER))
    def test_unpass(self, game_save):
        '''On hitting the unpass endpoint, the logged in user unpasses'''
        req = build_request(route_params={'id': 'id'})

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertEqual(DEFAULT_USER.identifier, resp_dict['round']['active_player']['identifier'])
        self.assertFalse(resp_dict['round']['active_player']['prepassed'])
