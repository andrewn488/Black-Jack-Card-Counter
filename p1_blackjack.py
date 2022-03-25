# -*- coding: utf-8 -*-
"""Seattle University, OMSBA 5062, F21, P1 - Blackjack, Andrew Nalundasan

colaboration - office hours, Arunima Roy, Andrew Turner, Ian Basco, Brooke Cummins
simulate(player) - simulate playing an evening's worth of blackjack
collect_winnings(amount) - call payoff() to add or subtract bets 
visualize(player) - simulate and plot results of a blackjack strategy
overlay_bell_curve(mu, sigma, n, bins) - plot a normal curve atop an 
histogram in current pylab figure
"""


from Card import Card
from Blackjack import Blackjack, Soft17, Basic
from CardCounter import CardCounter
from CardDeck import CardDeck
import math
import numpy as np
import pylab

def simulate(player,
             dealer=Soft17(),
             hands=100,
             ndecks=6,
             penetration=0.7,
             nplayers=7):
    """simulate playing an evening's worth of blackjack
    :param player:           Blackjack object representing the player
    :param dealer:           Blackjack object representing the dealer
    :param hands:            Number of hands to simulate
    :param ndecks:           Number of decks in each shoe
    :param penetration:      Depth of shoe before reshuffling
    :param nplayers:         Number of other players present (not simulated, but cards seen)
    :return: (final, lo, hi) player's accumulated winnings
    """
    
    deck = CardDeck(ndecks)  # create shoe of cards using ndecks 
    deck.shuffle()           # shuffle the deck
    winnings = []            # append here for player's accumulated winnings
    
    def collect_winnings(amount):
        """handles payoffs to player and dealer
        call payoff() from Blackjack
        append to winnings list for player's accumulated winnings
        """
        player.payoff(amount)         # player payoff
        dealer.payoff(-amount)        # dealer payoff
        winnings.append(amount)       # keep track of winnings
    
    for hand in range(hands):
        # shuffle deck if depth of shoe exceeds penetration
        # penetration parameter keeps you starting with a freshly shuffled deck before you get to the end
        shoe_depth = deck.dealt() / deck.count()
        if shoe_depth > penetration:
            deck.shuffle()
            player.new_shoe()
            
        # place bets before dealing out the cards
        # don't need to track bets or winnings of other players
        player_bet = player.bet()
        
        # deal 2 cards for new hand and place in a list
        player_hand = [deck.deal(), deck.deal()]   # player is dealt 2 cards
        player.dealt(player_hand) 
        
        # deal 2 cards for all other players 
        for nplayer in range(nplayers):
            cards = [deck.deal(), deck.deal()]
            player.sees(cards) 
            
        ## now that player (me) and other players have their hands, set up the dealer ## 
        
        dealer_hand = [deck.deal(), deck.deal()] # dealer is dealt 2 cards just like the players
        dealer.dealt(dealer_hand)
        dealer_known: Card = dealer_hand[1]      # dealer's second card [1] is known bc face up. first card [0] unknown bc face down
        player.sees([dealer_known])              # player sees this card since it is face up
        
        # if anyone has blackjack, pay up and end game
        if player.has_bj():
            if not dealer.has_bj():                 # player has bj and dealer does not, reward is 1.5*bet
                collect_winnings(player_bet * 1.5)
            else:                                   # nobody wins or loses bets in a tie. get your bet back
                collect_winnings(0.0)
            continue                                # game must continue from here
        elif dealer.has_bj():
            # if dealer has bj, player automatically loses the hand and loses bet
            collect_winnings(-player_bet)
            continue                                # if nobody has bj, game continues
        
        # player actions: stay, hit, double
        player_action = player.choose(dealer_known)
        while player_action != 'stay' and not player.busted():
            player_action = player.choose(dealer_known)      # player stays and dealer knows what player has
            if player_action == 'hit':
                player.hit(deck.deal())                      # deal a new card with each hit
            elif player_action == 'double': 
                player_bet += player_bet                     # ante up another bet to double down
                player.hit(deck.deal())
                break                                        # only allowed 1 hit when doubling. exit the while loop
                
        # dealer actions - Soft17 strategy must hit when < 16 and stay when > 17
        while dealer.choose(dealer_known) == 'hit' and not dealer.busted():
            card = deck.deal()          # deal out a new card for a hit
            dealer.hit(card)            # dealt card goes into dealer's hand
            player.sees([card])         # hits are dealt face up, so player sees it
        
        # print("Player hand: ", player.hand)
        # print("Dealer hand: ", dealer.hand)
        
        # determine winner and collect winnings
        if player.beats(dealer):              # player wins
            # amount bet is amount paid out
            collect_winnings(player_bet)      # amount bet is gained
        elif dealer.beats(player):            # dealer wins
            collect_winnings(-player_bet)     # amount bet is lost
        else:
            collect_winnings(0)               # nothing gained or lost in a tie
    
    # calculate winnings, lo-watermark, and hi-watermark
    final = 0
    lo = 0
    hi = 0
    for winning in winnings:
        final += winning
        if final < lo: 
            lo = final
        elif final > hi:
            hi = final
    
    return (final, lo, hi)

def visualize(trials, player=Basic()):
    """simulate and plot results of a blackjack strategy
    :param trials:   number of trials to simulate
    :param player:   player Blackjack object to simulate
    """
    # initialize data for plot
    winnings = []
    hi_watermark = []
    lo_watermark = []
    
    # loop over trials
    for i in range(trials):
        # collect data for the trials by calling simulate()
        final, lo, hi = simulate(player)
        # append return numbers to empty lists (return (final, lo, hi))
        winnings.append(final)
        lo_watermark.append(lo)
        hi_watermark.append(hi)
        
    # print("Winnings = ", winnings)
    # print("\nhi watermark = ", hi_watermark)
    # print("\nlo watermark = ", lo_watermark)
    
    # use numpy to calculate mean and stdev of winnings
    mean = np.mean(winnings)
    stdev = np.std(winnings)
    
    # create histogram and get n and bins as specified in guidance
    # use unpack_variable to debug "ValueError: too many values to unpack (expected 2)"
        # approach taken from: https://careerkarma.com/blog/python-valueerror-too-many-values-to-unpack-expected-2/
    n, bins, unpack_variable = pylab.hist(winnings, bins=20)
    
    # overlay calculated variables into the function as provided below
    overlay_bell_curve(mean, stdev, n, bins)
    
    # calculate range for worst moment 
    lo_min = np.min(lo_watermark)
    # use for flexible placement on chart on y-axis
    y_max = np.max(n)
    
    # add title and axis labels 
    pylab.title(f'Winnings for 99-hand night of Blackjack\n\$10-\$1000 wager ramp, hi-lo counting ({trials} trials)')
    pylab.xlabel("$-winnings")
    pylab.ylabel("Trials")
    
    # add stdev lines
    for i in range(-3, 4, 1):    # (start, stop, stride)
        pylab.axvline(mean - stdev * i, ls='dashed', color='lightgrey')
        
    # add annotations and other features of the plot
    pylab.annotate(f'Mean = ${mean:.0f}', (mean, y_max))                  # set annotation at (mean, highest point of the plot)
    pylab.annotate(f'Std.Dev. = ${stdev:.0f}', (mean + stdev, y_max/2))   # set annotation at (1st stdev, middle of plot)
    pylab.annotate(f'Worst Moment = ${lo_min:.0f}', (lo_min, y_max/4) )   # set annotation at (lowest point, lower 4th of the plot)
    
    # add red dot and red arrow for "worst moment"
    # learned arrow annotation from matplotlib documentation: https://matplotlib.org/stable/tutorials/text/annotations.html
    pylab.annotate(f'', (lo_min, 4), (lo_min, y_max/4 - 4), 
                    arrowprops = dict(headwidth=11, headlength=y_max/10, facecolor='red', edgecolor='black'))
    pylab.scatter(lo_min, 0, s=60, color = 'red') # make a red dot at the lowest end of the distribution
    
    # need bins as specified in guidance
    return bins

def overlay_bell_curve(mu, sigma, n, bins):
    """Overlay a normal curve atop an histogram on current pylab figure.
    :param mu:    mean
    :param sigma: standard deviation
    :param n:     number of events tracked in histogram
    :param bins:  number of bins in histogram
    """
    def f(x):
        """probability density function of normal distribution
        math.pow - Find value of x raised to the power of y: https://www.w3schools.com/python/ref_math_pow.asp
        math.exp - Return 'E' raised to the power of different numbers: https://www.w3schools.com/python/ref_math_exp.asp
        """
        proportion = 1 / (sigma * math.sqrt(2 * math.pi))          # proportion part of the formula
        raised_to = math.pow(x - mu, 2) / (-2 * sigma * sigma)     # e raised to this (from formula)
        return proportion * math.exp(raised_to)                    # proportion * e**raised_to
    
    """calculate scale
    unscaled, total area under pdf == 1.0
    need to calculate scale to match the area in the rectangles of the histogram
    example: bins = 10, range_min = -1000, range_max = 1000, trials = 500
        avg_bar_height = 500/10 # 50, bar_width = (1000 - -1000)/10 # 200
        scale = 50 * 200 * 10 # 10_000
    """
    # calculate number of bins and number of trials for the overlay
    n_bins = len(bins)
    tot_n = sum(n)
    
    # calculate max and min range of the x-axis. estimate as (mu +- 3.5*sigma) and convert to int type
    range_max = int(mu + 3.5*sigma)
    range_min = int(mu - 3.5*sigma)
    
    # calculate bar width and average bar height as described in guidance
    bar_width = (range_max - range_min) / n_bins
    avg_bar_height = tot_n / n_bins
    
    # calculate scale
    scale = avg_bar_height * bar_width * n_bins

    # get x and y range using calculated scale
    x = range(range_min, range_max, 100)   # stride of 100
    y = []
    for xi in x:
        y.append(scale * f(xi))    # call f(x) for pdf of normal distribution
        
    # plot the overlay
    pylab.plot(x, y, ls = 'solid', color = 'orange')


if __name__ == "__main__":
    # visualize(1000, player=Basic())
    # visualize(1000, player=Soft17())
    visualize(1000, player=CardCounter())
