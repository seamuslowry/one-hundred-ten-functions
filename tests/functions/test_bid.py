'''Bidding unit tests'''
import json
from unittest import TestCase, mock

from app.models import RoundStatus
from bid import main
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)


class TestBid(TestCase):
    '''Bidding unit tests'''

    @mock.patch('app.services.GameService.save', side_effect=return_input)
    @mock.patch('bid.parse_request',
                mock.Mock(return_value=(DEFAULT_USER, game(RoundStatus.BIDDING))))
    def test_bid(self, game_save):
        '''On hitting the bid endpoint, the logged in user bids'''
        req = build_request(
            route_params={'id': 'id'},
            body=json.dumps({'amount': 15}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertEqual(DEFAULT_USER.identifier,
                         resp_dict['round']['bidder']['identifier'])
        self.assertEqual(DEFAULT_USER.identifier, resp_dict['results'][-1]['identifier'])
