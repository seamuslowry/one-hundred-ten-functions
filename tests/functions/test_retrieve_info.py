'''Retrieve Info unit tests'''
from unittest import TestCase

import events
import game_info
import players
import search_games
from app.dtos.client import CompletedGame, Event, StartedGame, User
from app.mappers.constants import EventType
from tests.helpers import (build_request, completed_game, read_response_body,
                           started_game)


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

        # get that game's events
        resp = events.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_events: list[Event] = read_response_body(resp.get_body())
        self.assertIsNotNone(original_game['results'])
        assert original_game['results']
        self.assertNotEqual(original_game['results'], [])
        self.assertGreaterEqual(len(retrieved_events), len(original_game['results']))
        self.assertEqual(
            retrieved_events[len(retrieved_events)-len(original_game['results']):],
            original_game['results'])
        self.assertEqual(retrieved_events[-1]['type'], EventType.GAME_END.name)

    def test_game_players(self):
        '''Can retrieve user information for players on a game'''
        original_game: StartedGame = started_game()
        active_player = original_game['round']['active_player']
        assert active_player
        # get that game's players
        resp = players.main(
            build_request(
                route_params={'game_id': original_game['id']})
        )
        retrieved_users: list[User] = read_response_body(resp.get_body())
        user = next(
            u for u in retrieved_users
            if u['identifier'] == active_player['identifier'])
        self.assertIsNotNone(user['name'])
