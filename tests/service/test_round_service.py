'''Round Service unit tests'''
from unittest import TestCase

from hundredandten.actions import Bid, Discard
from hundredandten.constants import BidAmount, SelectableSuit
from hundredandten.deck import Deck
from hundredandten.group import Group, Player
from hundredandten.round import Round
from hundredandten.trick import Trick

from service import round as RoundService


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
            bids=[Bid('', BidAmount.PASS)],
            deck=Deck(),
            trump=SelectableSuit.CLUBS
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_discard_round_conversion(self):
        '''Round discarding can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.PASS)],
            deck=Deck(),
            trump=SelectableSuit.CLUBS,
            discards=[Discard('', [])]
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))

    def test_tricks_round_conversion(self):
        '''Round playing tricks can be converted to and from a DB save'''
        initial_round = Round(
            players=Group([Player('')]),
            bids=[Bid('', BidAmount.PASS)],
            deck=Deck(),
            trump=SelectableSuit.CLUBS,
            discards=[Discard('', [])],
            tricks=[Trick(SelectableSuit.CLUBS, [])]
        )

        self.assertEqual(initial_round, RoundService.from_db(RoundService.to_db(
            initial_round)))
