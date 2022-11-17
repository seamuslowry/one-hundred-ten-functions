'''Wrap dependency classes for use in this package'''
from hundredandten.actions import Bid, Discard, Play, SelectTrump, Unpass
from hundredandten.constants import (Accessibility, BidAmount, CardNumber,
                                     GameRole, GameStatus, RoundRole,
                                     RoundStatus, SelectableSuit,
                                     UnselectableSuit)
from hundredandten.deck import Card, Deck
from hundredandten.group import Group, Person, Player
from hundredandten.round import Round
from hundredandten.trick import Trick

ServerlessBid = Bid
ServerlessDiscard = Discard
ServerlessPlay = Play
ServerlessSelectTrump = SelectTrump
ServerlessUnpass = Unpass
ServerlessCard = Card
ServerlessDeck = Deck
ServerlessPlayer = Player
ServerlessPerson = Person
ServerlessGroup = Group
ServerlessRound = Round
ServerlessTrick = Trick
ServerlessAccessibility = Accessibility
ServerlessBidAmount = BidAmount
ServerlessCardNumber = CardNumber
ServerlessGameRole = GameRole
ServerlessGameStatus = GameStatus
ServerlessRoundRole = RoundRole
ServerlessRoundStatus = RoundStatus
ServerlessSelectableSuit = SelectableSuit
ServerlessUnselectableSuit = UnselectableSuit
