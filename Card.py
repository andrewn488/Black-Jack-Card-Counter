"""Seattle University, OMSBA 5062, Lab2 - Cards and P1 - Blackjack, Kevin Lundeen

Card - class for a standard playing card for card games.
"""


class Card(object):
    """Card - class for a standard playing card for card games.

    Class Data:
        Card.suits - dictionary of suit names keyed by one-character abbreviation
        Card.ranks - dictionary of card rank values keyed by abbreviation (2, 3, ..., 9, T, J, Q, K, A)
        Card.rank_names - dictionary of long names for some special ranks (e.g, Ace)
        Card.suit_order - arbitrary suit ordering for sorting (Clubs, Diamonds, Hearts, then Spades)
        Card.rank_order - also for sorting

    Object Data:
        rank and suit (as one-character codes)

    Methods and Overloads:
        supports comparisons, various constructions, and is hashable
        name() - long name of a card, e.g., Ace of Spades
        rank_value() - rank value
    
    Comparison ordering: 
        by rank (aces high), then by suit (alphabetically)
    """
    suits = {'S': 'Spades', 'H': 'Hearts', 'C': 'Clubs', 'D': 'Diamonds'}
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
             '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    rank_names = {'A': 'Ace', '2': 'Deuce', 'T': 'Ten', 'J': 'Jack',
                  'Q': 'Queen', 'K': 'King'}

    suit_order = {0: 'C', 1: 'D', 2: 'H', 3: 'S'}
    rank_order = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8',
                  7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}

    def __init__(self, card):
        """Card value is passed in a two-character string where the
        first character is one of Card.ranks.keys() and the second
        character is one of Card.suits.keys().
        >>> Card('3H')  # three of hearts
        Card('3H')
        >>> Card('as')  # ace of spades
        Card('AS')
        >>> Card('44')
        Traceback (most recent call last):
            ...
        ValueError: 4 is not a card suit

        Can also be constructed from an ordinal number between 0 and 51.
        The number is the placement in a sorted deck.
        >>> Card(0)
        Card('2C')
        >>> Card(1)
        Card('3C')
        >>> Card(13)
        Card('2D')
        >>> Card(51)
        Card('AS')

        Can also be constructed from another Card.
        >>> Card(Card('ad'))
        Card('AD')
        """
        if isinstance(card, Card):
            rank = card.rank
            suit = card.suit
        elif isinstance(card, int):
            if not 0 <= card <= 51:
                raise ValueError(str(card) + ' is not a valid ordinal card num')
            rank = Card.rank_order[card % 13]
            suit = Card.suit_order[card // 13]
        else:
            rank, suit = tuple(card.upper())
            if suit not in Card.suits:
                raise ValueError(suit + ' is not a card suit')
            if rank not in Card.ranks:
                raise ValueError(rank + ' is not a card rank')
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        >>> str(Card('2D'))
        '2D'
        """
        return self.rank + self.suit

    def __repr__(self):
        """
        >>> repr(Card('2D'))
        "Card('2D')"
        """
        return "Card('" + str(self) + "')"

    def __eq__(self, other):
        """
        >>> Card('3h') == Card('3H')
        True
        >>> Card('3h') != Card('4h')
        True
        """
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        """
        >>> Card('3h') < Card('3h')
        False
        >>> Card('3h') < Card('4h')
        True
        >>> Card('TD') > Card('tc')
        True
        """
        return (Card.ranks[self.rank] < Card.ranks[other.rank]
                or (self.rank == other.rank and self.suit < other.suit))

    def __le__(self, other):
        """
        >>> Card('2C') <= Card('AC')
        True
        """
        return self == other or self < other

    def __hash__(self):
        """Make cards hashable (usable as a key to a dictionary). """
        return hash(str(self))

    def name(self):
        """Return a long name for this card.
        >>> Card('ah').name()
        'Ace of Hearts'
        """
        # the get method for a dict is a key lookup with a backup value if the key isn't there
        rankName = Card.rank_names.get(self.rank, str(self.rank))
        return rankName + ' of ' + Card.suits[self.suit]

    def rank_value(self):
        """Return the rank value of this card.
        >>> Card('kd').rank_value()
        13
        """
        return Card.ranks[self.rank]
