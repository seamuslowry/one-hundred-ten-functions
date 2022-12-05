'''Event log unit tests'''
from unittest import TestCase, mock

from app.models import RoundStatus
from events import main
from tests.helpers import DEFAULT_USER, build_request, game, read_response_body


class TestEvents(TestCase):
    '''Get Events unit tests'''

    @mock.patch('events.parse_request',
                mock.Mock(return_value=(DEFAULT_USER,
                                        game(RoundStatus.BIDDING))))
    def test_get_events(self):
        '''On hitting the events endpoint the events are retrieved'''
        req = build_request(route_params={'game_id': 'id'})

        resp = main(req)
        resp_list = read_response_body(resp.get_body())

        self.assertGreater(len(resp_list), 0)
