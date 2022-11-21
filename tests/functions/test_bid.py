'''Bidding unit tests'''
import json
from unittest import TestCase, mock

from bid import main
from models import RoundStatus
from tests.helpers import (DEFAULT_USER, build_request, game,
                           read_response_body, return_input)


class TestBid(TestCase):
    '''Bidding unit tests'''

    @mock.patch('services.GameService.save', side_effect=return_input)
    @mock.patch('services.GameService.get', mock.Mock(
        return_value=game(RoundStatus.BIDDING)))
    @mock.patch('services.UserService.from_request', mock.Mock(return_value=DEFAULT_USER))
    @mock.patch('services.UserService.get', mock.Mock(return_value=DEFAULT_USER))
    def test_bid(self, game_save):
        '''On hitting the bid endpoint, the logged in user bids'''
        req = build_request(
            route_params={'id': 'id'},
            body=json.dumps({'amount': 15}).encode('utf-8'))

        resp = main(req)
        resp_dict = read_response_body(resp.get_body())

        game_save.assert_called_once()
        self.assertEqual(DEFAULT_USER.identifier, resp_dict['round']['bidder']['identifier'])
