'''Select Trump unit tests'''
import json
from unittest import TestCase, mock

from app.models import RoundStatus
from select_trump import main
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)


class TestSelectTrump(TestCase):
    '''Trump Selection unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('select_trump.parse_request',
                mock.Mock(return_value=(DEFAULT_USER, game(RoundStatus.TRUMP_SELECTION))))
    def test_bid(self, game_save):
        '''On hitting the trump selection endpoint, the logged in user selects trump'''
        trump = 'CLUBS'

        req = build_request(
            route_params={'game_id': 'id'},
            body=json.dumps({'suit': trump}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertEqual(trump, resp_dict['round']['trump'])
        self.assertEqual(trump, resp_dict['results'][-1]['suit'])
