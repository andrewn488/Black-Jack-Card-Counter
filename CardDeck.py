"""Seattle University, OMSBA 5062, Lab2 - Cards and P1 - Blackjack, Kevin Lundeen

CardDeck - class for a deck (or several decks) of standard playing cards for card games.
"""
import random

from Card import Card


class CardDeck(object):
    """A standard 52-card deck of playing cards (or several of them)

    Object Data:
        cards - list of Card objects
        top - index of last card dealt (undealt cards have index < deck.top)

    Methods:
        CardDeck(n) - new deck with 52*n cards (n defaults to 1)
        shuffle() - replace any dealt cards and randomize the deck's order
        deal() - take off the top card (and return it)
        deal_random() - take an undealt card from a random spot in the deck
        count() - total number of cards (52*n)
        dealt() - number of cards that have been dealt since last shuffle
        undealt() - number of cards that have yet to be dealt
    """

    def __init__(self, num_decks=1):
        """Starts as sorted deck of undealt cards"""
        self.cards = []
        for i in range(num_decks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.cards.append(Card(rank + suit))
        self.top = len(self.cards)  # top is the index of the last dealt card

    def __str__(self):
        """The list of cards from bottom of the deck to top followed by
        the number of undealt cards (counting from the bottom)
        >>> str(CardDeck())
        "['2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']/52"
        """
        ret = [str(card) for card in self.cards]
        return str(ret) + '/' + str(self.top)

    def __repr__(self):
        return 'CardDeck(' + str(self) + ')'

    def deal(self):
        """Remove and return the next card down on the deck.
        None is returned if there are no more cards.
        (Note: you can reset the deck with the shuffle method.)
        """
        if self.top == 0:
            return None
        self.top -= 1
        return self.cards[self.top]

    def undealt(self):
        """Number of cards left to deal."""
        return self.top

    def dealt(self):
        """Number of cards already dealt."""
        return len(self.cards) - self.top

    def count(self):
        """Total number of cards in the deck--both dealt and undealt."""
        return len(self.cards)

    def deal_random(self):
        """Deal a card selected randomly from the undealt cards."""
        if self.top == 0:
            return None
        pick = random.randint(0, self.top - 1)
        # swap picked card with top card
        self.top -= 1
        self.cards[pick], self.cards[self.top] = (self.cards[self.top],
                                                  self.cards[pick])
        return self.cards[self.top]

    def shuffle(self):
        """Randomly reorder the deck and reset it to be all undealt."""
        self.top = len(self.cards)
        card = self.deal_random()
        while card is not None:
            card = self.deal_random()
        self.top = len(self.cards)
