'''Event service unit tests'''
from unittest import TestCase

from app.models import (Bid, BidAmount, Card, CardNumber, Discard, GameEnd,
                        GameStart, Play, RoundEnd, RoundStart, SelectableSuit,
                        SelectTrump, TrickEnd, TrickStart)
from app.services import CardService, EventService

card = Card(CardNumber.ACE, SelectableSuit.CLUBS)

raw_events = [
    GameStart(),
    RoundStart(dealer='dealer', hands={'1': [card]}),
    Bid('1', BidAmount.FIFTEEN),
    SelectTrump('1', SelectableSuit.CLUBS),
    Discard('1', [card]),
    TrickStart(),
    Play('1', card),
    TrickEnd('1'),
    RoundEnd({'1': 15}),
    GameEnd('1')
]


def index_of(event_type: type) -> int:
    '''Get the index of the event of the pass type'''
    return next(i for i, v in enumerate(raw_events) if isinstance(v, event_type))


class TestEventService(TestCase):
    '''Event service unit tests'''

    def test_event_conversion_without_details(self):
        '''Events can be converted when no one matches the identifier'''
        json_events = EventService.json(raw_events, 'noMatch')

        round_start_index = index_of(RoundStart)
        discard_index = index_of(Discard)

        self.assertEqual(len(raw_events), len(json_events))
        self.assertEqual(1, json_events[round_start_index]['hands']['1'])
        self.assertEqual(1, json_events[discard_index]['discards'])

    def test_event_conversion_with_details(self):
        '''Events can be converted when the client matches the identifier'''
        bid_index = index_of(Bid)
        json_events = EventService.json(raw_events, raw_events[bid_index].identifier)

        round_start_index = index_of(RoundStart)
        discard_index = index_of(Discard)

        self.assertEqual(len(raw_events), len(json_events))
        self.assertEqual([CardService.json(card)], json_events[round_start_index]['hands']['1'])
        self.assertEqual([CardService.json(card)], json_events[discard_index]['discards'])
