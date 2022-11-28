'''Searching users unit tests'''
from unittest import TestCase, mock

from search_users import main
from tests.helpers import DEFAULT_USER, build_request, read_response_body


class TestSearchUsers(TestCase):
    '''User search unit tests'''

    @mock.patch('app.services.UserService.search', mock.Mock(return_value=[DEFAULT_USER]))
    def test_user_search(self):
        '''On hitting the user search endpoint, matching users are returned'''
        req = build_request(params={'searchText': 'id'})

        resp = main(req)
        resp_list = read_response_body(resp.get_body())

        self.assertEqual(1, len(resp_list))
