'''Game Service unit tests'''
from unittest import TestCase

from app.models import Game, Group, Player, Round, RoundRole
from app.services import GameService
from app.services.cosmos import game_client


class TestGameService(TestCase):
    '''Unit tests to ensure game translations work as expected'''

    def test_game_conversion(self):
        '''Game can be converted to and from a DB save'''
        initial_game = Game(id='test', seed='test_game')

        self.assertEqual(initial_game, GameService.from_db(GameService.to_db(initial_game)))

    def test_waiting_game_client_conversion(self):
        '''Game can be converted to client json while waiting'''
        initial_game = Game(id='test', seed='test_game')

        waiting_json = GameService.json(initial_game, '')
        self.assertIsNotNone(waiting_json)
        self.assertNotIn('round', waiting_json)
        self.assertIn('accessibility', waiting_json)

    def test_started_game_client_conversion(self):
        '''Game can be converted to client json once started'''
        initial_game = Game(id='test', seed='test_game', rounds=[Round(
            players=Group([Player(identifier='', roles={RoundRole.DEALER})]))])

        started_json = GameService.json(initial_game, '')
        self.assertIsNotNone(started_json)
        self.assertIn('round', started_json)
        self.assertNotIn('accessibility', started_json)

    def test_game_save(self):
        '''Game can be saved to the DB'''
        game = Game(id='test', seed='test_game')

        game_client.upsert_item.return_value = GameService.to_db(game)

        self.assertIsNotNone(GameService.save(game))
        game_client.upsert_item.assert_called_once()

    def test_game_get(self):
        '''Game can be retrieved to the DB'''
        game = Game(id='test', seed='test_game')

        game_client.read_item.return_value = GameService.to_db(game)

        self.assertIsNotNone(GameService.get(game.id))
        game_client.read_item.assert_called_once()
