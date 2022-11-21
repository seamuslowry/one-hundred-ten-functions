'''Round Service unit tests'''
from unittest import TestCase

from models import (Bid, BidAmount, Deck, Discard, Group, Player, Round,
                    RoundRole, SelectableSuit, SelectTrump, Trick)
from services import round as RoundService


class TestRoundService(TestCase):
    '''Unit tests to ensure round translations work as expected'''

    def test_blank_round_conversion(self):
        '''Initial round can be converted to and from a DB save'''
        initial_round = Round()

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_no_trump_round_conversion(self):
        '''Round in bidding can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.PASS)],
            deck=Deck()
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_trump_round_conversion(self):
        '''Round in discard can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.FIFTEEN)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS)
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_discard_round_conversion(self):
        '''Round discarding can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.FIFTEEN)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS),
            discards=[Discard('', [])]
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_tricks_round_conversion(self):
        '''Round playing tricks can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.FIFTEEN)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS),
            discards=[Discard('', [])],
            tricks=[Trick(SelectableSuit.CLUBS, [])]
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_blank_round_client_conversion(self):
        '''Initial round can be converted to client json'''
        initial_round = Round(
            players=Group([Player('', roles={RoundRole.DEALER})]),
        )

        self.assertIsNotNone(RoundService.json(initial_round, ''))

    def test_no_trump_round_client_conversion(self):
        '''Round in bidding can be converted to client json'''
        initial_round = Round(
            players=Group([Player('1', roles={RoundRole.DEALER}), Player('2')]),
            bids=[Bid('2', BidAmount.PASS)],
            deck=Deck()
        )

        self.assertIsNotNone(RoundService.json(initial_round, ''))

    def test_trump_round_client_conversion(self):
        '''Round in discard can be converted to client json'''
        initial_round = Round(
            players=Group([Player('1', roles={RoundRole.DEALER}), Player('2')]),
            bids=[Bid('1', BidAmount.FIFTEEN), Bid('2', BidAmount.PASS)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS)
        )

        self.assertIsNotNone(RoundService.json(initial_round, ''))

    def test_discard_round_client_conversion(self):
        '''Round discarding can be converted to client json'''
        initial_round = Round(
            players=Group([Player('1', roles={RoundRole.DEALER}), Player('2')]),
            bids=[Bid('1', BidAmount.FIFTEEN), Bid('2', BidAmount.PASS)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS),
            discards=[Discard('1', [])]
        )

        self.assertIsNotNone(RoundService.json(initial_round, ''))

    def test_tricks_round_client_conversion(self):
        '''Round playing tricks can be converted to client json'''
        initial_round = Round(
            players=Group([Player('1', roles={RoundRole.DEALER}), Player('2')]),
            bids=[Bid('1', BidAmount.FIFTEEN), Bid('2', BidAmount.PASS)],
            deck=Deck(),
            selection=SelectTrump('', SelectableSuit.CLUBS),
            discards=[Discard('1', []), Discard('2', [])],
            tricks=[Trick(SelectableSuit.CLUBS, [])]
        )

        self.assertIsNotNone(RoundService.json(initial_round, ''))
