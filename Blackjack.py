"""Blackjack, Kevin Lundeen, cpsc 5910, R18, Seattle University

Blackjack - blackjack card-game player
Soft17 - Blackjack with typical dealer strategy 
Basic - Blackjack with basic strategy
"""
from Card import Card


class Blackjack(object):
    """Blackjack card-game player. The player represents an automaton that
    plays the blackjack game. 
    
    This base class handles the game logistics:
        hand - list of cards in player's hand
        value - the sum of the point values for the cards in the hand (Ace=1)
        soft_value() - point value, promoting any Ace to 11, if possible
        busted() - True if value > 21
        has_bj() - True if hand is A + ten card
        beats(other) - True if this hand beats the other (higher points but not busted, etc.)
        
    There are also methods to track the progress of play
        bet() - Gets the bet from the player prior to the hand being played
        dealt(cards) - Informs the player of her first two cards dealt during the deal
        choose(dlr_up) - Player informs the dealer of her choice, 'stay', 'hit', or 'double'
        hit(card) - Card dealt in response to a 'hit' or 'double' choice
        payoff(winnings) - Player is paid chips or chips taken (or 0 for tie)
        new_shoe() - Called when the deck has been reshuffled
        sees(cards) - Informs the player of any visible cards besides those she has been dealt

    And there are descriptive methods:
        __str__() - Shows synopsis of current hand
        title() - Descriptive heading for reports for this player
    """

    def __init__(self):
        self.payoff(0.0)

    def __str__(self):
        return 'Bj[{}]{}{}'.format(','.join(map(str, self.hand)), self.value,
                                   ('or' + str(self.soft_value())
                                    if self.value != self.soft_value() else ''))

    def title(self):
        """Descriptive heading for reports for this player"""
        return '$100 wager, no strategy (never hits)'

    def soft_value(self):
        """point value, promoting any Ace to 11, if possible
        >>> bj = Blackjack()
        >>> bj.dealt([Card('Ah'),Card('Ad'),Card('8s')])
        >>> bj.soft_value()
        20
        """
        if self.value <= 11 and self.has_ace:
            return self.value + 10
        else:
            return self.value

    def dealt(self, cards):
        """Informs the player of her first two cards dealt during the deal"""
        for card in cards:
            self.hit(card)

    def hit(self, card):
        """Card dealt in response to a 'hit' or 'double' choice"""
        self.hand.append(card)
        self.sees([card])
        if card.rank == 'A':
            self.has_ace = True
            self.value += 1
        elif card.rank in ['T', 'J', 'Q', 'K']:
            self.value += 10
        else:
            self.value += card.rank_value()

    def payoff(self, winnings):
        """Player is paid chips or chips taken (or 0 for tie)"""
        self.hand = []
        self.value = 0
        self.has_ace = False

    def busted(self):
        """True if value > 21
        >>> bj = Blackjack()
        >>> bj.dealt([Card('9h'),Card('Td'),Card('8s')])
        >>> bj.busted()
        True
        >>> bj = Blackjack()
        >>> bj.dealt([Card('9h'),Card('Td'),Card('2s')])
        >>> bj.busted()
        False
        """
        return self.value > 21

    def has_bj(self):
        """True if hand is A + ten card
        >>> bj = Blackjack()
        >>> bj.dealt([Card('9h'),Card('Td'),Card('2s')])
        >>> bj.has_bj()
        False
        >>> bj = Blackjack()
        >>> bj.dealt([Card('Ah'),Card('Td')])
        >>> bj.has_bj()
        True
        """
        return len(self.hand) == 2 and self.value == 11 and self.has_ace

    def beats(self, other):
        """True if this hand beats the other (higher points but not busted, etc.)
        >>> bj = Blackjack(); other = Blackjack()
        >>> bj.dealt([Card('9h'),Card('Td'),Card('2s')])
        >>> other.dealt([Card('3s'),Card('Ad')])
        >>> bj.beats(other)
        True
        
        Blackjack beats 21
        >>> bj = Blackjack(); other = Blackjack()
        >>> bj.dealt([Card('Ah'),Card('Td')])
        >>> other.dealt([Card('3s'),Card('Ad'),Card('7d')])
        >>> bj.beats(other)
        True

        Ties are False (does not beat)        
        >>> bj = Blackjack(); other = Blackjack()
        >>> bj.dealt([Card('7h'),Card('Td'),Card('4d')])
        >>> other.dealt([Card('3s'),Card('Ad'),Card('7d')])
        >>> bj.beats(other)
        False
        """
        if self.busted():
            return False
        elif other.busted():
            return True
        elif self.soft_value() > other.soft_value():
            return True
        elif self.has_bj() and not other.has_bj():
            return True
        else:
            return False

    def choose(self, dlr_up):
        """Player informs the dealer of her choice, 'stay', 'hit', or 'double'"""
        return 'stay'

    def bet(self):
        """Gets the bet from the player prior to the hand being played"""
        return 100  # $100

    def new_shoe(self):
        """Called when the deck has been reshuffled"""
        pass

    def sees(self, cards):
        """Informs the player of any visible cards besides those she has been dealt"""
        pass


class Soft17(Blackjack):
    """Standard American dealer strategy"""

    def title(self):
        """Descriptive heading for reports for this player"""
        return 'dealer soft-17 policy'

    def choose(self, dlr_up):
        """hits on 16, stays on 17, except hits on soft 17 (Ace plus 6)
        >>> d = Soft17()
        >>> d.dealt([Card('Jh'),Card('7s')])
        >>> d.choose(Card('3h'))
        'stay'
        >>> d = Soft17()
        >>> d.dealt([Card('As'),Card('6d')])
        >>> d.choose(Card('2d'))
        'hit'
        >>> d = Soft17()
        >>> d.dealt([Card('As'),Card('3d'),Card('2h'),Card('Ad')])
        >>> d.choose(Card('3h'))
        'hit'
        """
        if self.has_bj():
            return 'stay'
        if self.value > 16:
            return 'stay'
        elif self.has_ace and self.soft_value() > 17:
            return 'stay'
        else:
            return 'hit'


class Basic(Blackjack):
    """Basic ideal strategy. E.g., see wikipedia for betting chart."""
    hard_strategy = {16: 5 * 's' + 5 * 'h',
                     15: 5 * 's' + 5 * 'h',
                     14: 5 * 's' + 5 * 'h',
                     13: 5 * 's' + 5 * 'h',
                     12: 2 * 'h' + 3 * 's' + 5 * 'h',
                     11: 10 * 'h',
                     10: 8 * 'h' + 2 * 'h',
                     9: 'h' + 4 * 'h' + 5 * 'h',
                     8: 10 * 'h',
                     7: 10 * 'h',
                     6: 10 * 'h',
                     5: 10 * 'h',
                     4: 10 * 'h'}
    hard_strategy2 = {16: 5 * 's' + 5 * 'h',
                      15: 5 * 's' + 5 * 'h',
                      14: 5 * 's' + 5 * 'h',
                      13: 5 * 's' + 5 * 'h',
                      12: 2 * 'h' + 3 * 's' + 5 * 'h',
                      11: 10 * 'd',
                      10: 8 * 'd' + 2 * 'h',
                      9: 'h' + 4 * 'd' + 5 * 'h',
                      8: 10 * 'h',
                      7: 10 * 'h',
                      6: 10 * 'h',
                      5: 10 * 'h',
                      4: 10 * 'h'}
    soft_strategy = {10: 10 * 's',
                     9: 4 * 's' + 's' + 5 * 's',
                     8: 5 * 's' + 2 * 's' + 3 * 'h',
                     7: 'h' + 4 * 'h' + 5 * 'h',
                     6: 2 * 'h' + 3 * 'h' + 5 * 'h',
                     5: 2 * 'h' + 3 * 'h' + 5 * 'h',
                     4: 3 * 'h' + 2 * 'h' + 5 * 'h',
                     3: 3 * 'h' + 2 * 'h' + 5 * 'h',
                     2: 10 * 'h'}
    soft_strategy2 = {10: 10 * 's',
                      9: 4 * 's' + 'd' + 5 * 's',
                      8: 5 * 'd' + 2 * 's' + 3 * 'h',
                      7: 'h' + 4 * 'd' + 5 * 'h',
                      6: 2 * 'h' + 3 * 'd' + 5 * 'h',
                      5: 2 * 'h' + 3 * 'd' + 5 * 'h',
                      4: 3 * 'h' + 2 * 'd' + 5 * 'h',
                      3: 3 * 'h' + 2 * 'd' + 5 * 'h',
                      2: 10 * 'h'}
    xlate = {'s': 'stay', 'd': 'double', 'h': 'hit'}

    def title(self):
        """Descriptive heading for reports for this player"""
        return '$100 wager, basic strategy'

    def choose(self, dlr_up):
        """Choice is best choice statistically for a full deck."""
        if self.has_bj() or self.value > 16:
            return 'stay'

        # get row from correct strategy table
        if len(self.hand) == 2:  # allowed to double
            if self.has_ace and self.value <= 10:
                row = Basic.soft_strategy2[self.value]
            else:
                row = Basic.hard_strategy2[self.value]
        else:  # not allowed to double
            if self.has_ace and self.value <= 10:
                row = Basic.soft_strategy[self.value]
            else:
                row = Basic.hard_strategy[self.value]

        # get column
        if dlr_up.rank == 'A':
            col = 9  # last choice is for aces
        elif dlr_up.rank_value() >= 10:
            col = 8  # ten-point card 10, J, Q, K
        else:
            col = dlr_up.rank_value() - 2  # table starts out for 2, 3, ...

        return Basic.xlate[row[col]]
