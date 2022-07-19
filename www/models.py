from enum import Enum, auto
from sqlalchemy import Enum as DBEnum, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .extensions import db


class Rank(Enum):
    ACE = auto()
    TWO = auto()
    TREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()


class Suit(Enum):
    CLUB = auto()
    DIAMOND = auto()
    HEART = auto()
    SPADE = auto()


class Deck(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    size = Column(Integer, server_default='52')
    cards = relationship('Card', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.size}-card deck'


class Card(db.Model):

    __table_args__ = (
        UniqueConstraint('rank', 'suit', 'deck_id'),
    )

    id = Column(Integer, primary_key=True)
    rank = Column(DBEnum(Rank), nullable=False)
    suit = Column(DBEnum(Suit), nullable=False)
    deck_id = Column(Integer, ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return f'{self.rank} of {self.suit}s'
