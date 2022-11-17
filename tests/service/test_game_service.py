'''Game Service unit tests'''
from unittest import TestCase

from models import Game
from service import GameService
from service.cosmos import game_client


class TestGameService(TestCase):
    '''Unit tests to ensure game translations work as expected'''

    def test_game_conversion(self):
        '''Game can be converted to and from a DB save'''
        initial_game = Game(id='test', seed='test_game')

        self.assertEqual(initial_game, GameService.from_db(GameService.to_db(initial_game)))

    def test_game_save(self):
        '''Game can be saved to the DB'''
        game = Game(id='test', seed='test_game')

        game_client.upsert_item.return_value = GameService.to_db(game)

        self.assertIsNotNone(GameService.save(game))
        game_client.upsert_item.assert_called_once()
