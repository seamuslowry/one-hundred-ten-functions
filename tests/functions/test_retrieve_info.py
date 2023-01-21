'''Retrieve Info unit tests'''
from unittest import TestCase

import events
import game_info
import search_games
from app.dtos.client import CompletedGame, Event
from app.mappers.constants import EventType
from tests.helpers import build_request, completed_game, read_response_body


class TestRetrieveInfo(TestCase):
    '''Unit tests to the client can query for info as necessary'''

    def test_search_winner(self):
        '''Can search by winner'''
        game: CompletedGame = completed_game()

        # search games
        resp = search_games.main(
            build_request(
                body={
                    'winner': game['winner']['identifier']
                })
        )
        games = read_response_body(resp.get_body())
        self.assertIn(game, games)

    def test_game_info(self):
        '''Can retrieve information about a game'''
        original_game: CompletedGame = completed_game()

        # get that game's info
        resp = game_info.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        game = read_response_body(resp.get_body())
        self.assertEqual(game, original_game)

    def test_game_events(self):
        '''Can retrieve event information about a game'''
        original_game: CompletedGame = completed_game()

        # get that game's info
        resp = events.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_events: list[Event] = read_response_body(resp.get_body())
        self.assertGreater(len(retrieved_events), 0)
        self.assertEqual(retrieved_events[-1]['type'], EventType.GAME_END.name)
