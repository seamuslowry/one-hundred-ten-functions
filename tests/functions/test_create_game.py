'''Create game unit tests'''
from unittest import TestCase, mock

from create_game import main
from tests.helpers import build_request, read_response_body


class TestCreateGame(TestCase):
    '''Create Game unit tests'''

    @mock.patch('service.GameService.save', return_value={})
    def test_creates_game(self, save):
        '''On hitting the create request a game is created and returned'''
        req = build_request()
        saved_value = {'id': 'new-id'}

        save.return_value = saved_value

        resp = main(req)

        save.assert_called_once()
        self.assertEqual(read_response_body(resp.get_body()), saved_value)
