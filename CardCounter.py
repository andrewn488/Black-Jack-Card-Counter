# -*- coding: utf-8 -*-
"""Seattle University, OMSBA 5062, F21, P1 - Blackjack, Andrew Nalundasan

CardCounter - class for card counting strategy using the hi-lo counting strategy to bring down the house. Inherits from Basic
"""


from Blackjack import Basic

class CardCounter(Basic):
    """Inherits from Basic and implements card counting strategy"""
    def __init__(self):
        self.count = 0
        self.payoff(0.0)
        
    def title(self):
        """Descriptive heading for reports for this player"""
        return 'CardCounter strategy, bets range between $10 - $1000'
    
    def new_shoe(self):
        """When the deck is reshuffled, player sets their mental count back to 0"""
        self.count = 0
    
    def sees(self, cards):
        """Informs the player of any visible cards besides those she has been dealt
        player keeps mental count of cards according to rank value
        """
        for card in cards:
            card_count = 0
            card_rank = card.rank_value()   # taken from Basic
            if card_rank in [2, 3, 4, 5, 6]:
                card_count += 1 
            elif card_rank in ['T', 'J', 'Q', 'K', 'A']:
                card_count -= 1
                
            self.count += card_count
        
    def bet(self):
        """Makes bet according to the mental count
        Lower counts return lower bets, higher counts return higher bets
        Bets set according to provided guidance"""
        
        count = self.count
            
        if count <= 0:
            return 10
        elif count == 1:
            return 50
        elif count == 2:
            return 100
        elif count == 3:
            return 200
        elif count == 4:
            return 500
        elif count >= 5:
            return 1000
        
