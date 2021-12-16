from Blackjack import Blackjack  # necessary?
from Blackjack import Basic  # an inheritor of an inheritor, do I need to do anything special?
from Card import Card


class CardCounter(Basic):
    """is similar to basic, but changes the players betting method based on the results from a
    counting table, does not impact playing strategy"""

    # is self.sees([card]) important here?
    # self.card_counted = 0  # started below, is that ok?
    def __init__(self):
        self.payoff(0.0)
        self.seen_cards = []  # just so that it is initiated?

    def new_shoe(self):  # switch
        """Called when the deck has been reshuffled"""
        self.check_shoe = 'new'

    def sees(self, cards):
        """Informs the player of any visible cards besides those she has been dealt"""
        for i in cards:
            # print(i)
            self.seen_cards.append(i)  # counting purposes

    def hi_lo_count(self):
        """Decrements or increases constant variable card_counted, to keep track of value of
        visible cards, which impacts betting strategy"""
        # print('Checking hi lo')
        if self.check_shoe == 'new':  # working to reset count in new shoe
            self.card_counted = 0
            self.seen_cards = []  # needing to reset the seen cards so the list is erased.
            # print('new shoe!')
            self.check_shoe = 'old'  # reset it
            return self.card_counted
        for card in self.seen_cards:
            #  print('in card counting loop')
            #  print('the card is', card)
            if card.rank_value() >= 10 or card.rank_value() == 1:  # checking for ace, rank_value not
                self.card_counted -= 1
            elif card.rank_value() in [7, 8, 9]:
                self.card_counted += 0  # probably useless, just being thurough
            elif card.rank_value() in [2, 3, 4, 5, 6]:
                self.card_counted += 1
        # print(self.card_counted)  # looks like it is working right
        return self.card_counted

    def bet(self):
        """Gets the bet from the player prior to the hand being played, modified from Blackjack
        class"""
        current_count = self.hi_lo_count()
        count_bet = 0  # temp for $
        if current_count <= 0:
            count_bet = 10
        elif current_count == 1:
            count_bet = 50
        elif current_count == 2:
            count_bet = 100
        elif current_count == 3:
            count_bet = 200
        elif current_count == 4:
            count_bet = 500
        elif current_count >= 5:
            count_bet = 1000
        # print(count_bet)
        return count_bet  # depends on count

