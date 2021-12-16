"""Seattle University, OMSBA 5062, P1 - Blackjack, Kevin Lundeen

visualize(player) - simulate and plot results of a blackjack strategy
simulate(player) - simulate playing an evening's worth of blackjack
overlay_bell_curve(mu, sigma, n, bins) - plot a normal curve atop an
histogram in current pylab figure
"""

from Card import Card
from Blackjack import Blackjack
from Blackjack import Basic
from Blackjack import Soft17
from CardDeck import CardDeck
from CardCounter import CardCounter
import pylab
import math
import statistics
import random


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
    final = 0
    lo = 0  # temporary
    hi = 0  # temporary
    winnings = 0
    new_deck = CardDeck(ndecks)
    new_deck.shuffle()  # shuffling the cards within the deck now
    player.new_shoe()
    dealer.new_shoe()
    for i in range(hands):
        if new_deck.dealt() / new_deck.count() >= penetration:
            new_deck.shuffle()
            player.new_shoe()
            dealer.new_shoe()
            # print('The deck has been shuffled')  # not needed
        current_bet = player.bet()  # gets bet from player
        #print(current_bet)
        for i in range(nplayers):  # deals 2 cards each
            card_others1 = new_deck.deal()
            player.sees([Card(card_others1)])  # trying to make sure player can see other cards
            # dealt
            card_others2 = new_deck.deal()
            player.sees([Card(card_others2)])
        #print('bet:', current_bet)
        # deck.deal()  # debugging purposes
        t_card1 = str(new_deck.deal())  # first new card
        # print(t_card1)
        t_card2 = str(new_deck.deal())
        t_card3 = new_deck.deal()
        t_card4 = new_deck.deal()
        player.dealt([Card(t_card1), Card(t_card2)])
        # print(player.soft_value())
        dealer.dealt([Card(t_card3), Card(t_card4)])
        player.sees([Card(t_card3), Card(t_card4)])  # making sure that the player sees the cards
        # print(dealer.soft_value())
        choice1 = player.choose(Card(t_card4))
        # print(choice1)
        while choice1 == 'hit':
            t_card5 = new_deck.deal()
            player.hit(Card(t_card5))  # working!
            choice1 = player.choose(Card(t_card4))
            # print(choice1)
        if choice1 == 'double':
            # player.bet() = 2 * int(player.bet())  # NEED TO ASSIGN NEW VARIABLE
            current_bet *= 2
            t_card5 = new_deck.deal()
            player.hit(Card(t_card5))
            # print(choice1)
        choice2 = dealer.choose(choice1)
        while choice2 == 'hit':
            t_card6 = new_deck.deal()
            # print(t_card6)
            dealer.hit(Card(t_card6))
            player.sees([Card(t_card6)])
            choice2 = dealer.choose(Card(t_card4))  # because this is the dealers choice right?
        if player.busted() or dealer.beats(player):
            winnings -= int(current_bet)
            # print('loss')
            if winnings <= lo:
                lo = winnings
        elif player.beats(dealer):
            # print('win')
            if player.has_bj():
                winnings += current_bet * 1.5
            else:
                winnings += current_bet
            if winnings >= hi:
                hi = winnings  # should allow for count
        else:
            winnings += 0  # no gain or loss
        player.payoff(winnings)  # clear player
        dealer.payoff(0)  # clear dealer
    final = winnings
    # print(final, lo, hi)
    return (final, lo, hi)  # working!!


# john = Soft17()
# simulate(john)
# simulate(dealer)
# simulate(player=Basic())  #build from here
#simulate(player=CardCounter(), hands=2)
#simulate(player= CardCounter(), ndecks=1)

def overlay_bell_curve(mu, sigma, n, bins):
    """Overlay a normal curve atop an histogram on current pylab figure.
    :param mu:    mean
    :param sigma: standard deviation
    :param n:     number of events tracked in histogram
    :param bins:  number of bins in histogram
    """
    def f(x):
        """probability density function of normal distribution"""
        return ((1 / (sigma * (2 * math.pi) ** 0.5)) * math.exp(
                    ((x - mu) ** 2) / (-2 * sigma ** 2)))

    range_low = mu - (3.5 * sigma)
    range_high = mu + (3.5 * sigma)
    diff = (range_high - range_low) / bins
    x_list = []
    y_list = []
    y_cord = 0  # temporary
    while range_low <= range_high:
        y_cord = f(range_low)
        y_list.append(y_cord)
        x_list.append(range_low)
        range_low += sigma/10
    y_list = [i * ((diff) * (n / bins) * bins) for i in y_list]  # is it big enough?
    #  print(y_list)
    #  print(x_list)
    pylab.plot(x_list, y_list)

def visualize(trials, player=Basic()):  # works well
    """simulate and plot results of a blackjack strategy
    :param trials:   number of trials to simulate
    :param player:   player Blackjack object to simulate
    """
    rounds = []
    for i in range(trials):  # is this too crude?
        final, lo, hi = simulate(player)
        rounds.append(final)  # just a list, not a dictionary
    pylab.figure(random.randint(0, 100))
    pylab.hist(rounds, 20)
    pylab.xlabel('$-winnings')
    pylab.ylabel('Trials')
    n = len(rounds)
    tot = 0.0
    mu = statistics.mean(rounds)
    sigma = statistics.stdev(rounds)
    n = trials
    bins = 20  # just hard coded
    pylab.axvline(x=mu, linestyle='--', color='grey')
    pylab.axvline(x=(mu - sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu + sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu - 2 * sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu + 2 * sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu + sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu - 3 * sigma), linestyle='--', color='grey')
    pylab.axvline(x=(mu + 3 * sigma), linestyle='--', color='grey')
    #  print(rounds.count(max(rounds)))
    pylab.annotate('mean = $%s' % round(mu), xy=(mu, (n*.13)))

    pylab.annotate("Std.Dev = $%s" % round(sigma), xy=(round(sigma + mu), round((n*.07))))

    pylab.annotate('Worst Moment = $%s' % min(rounds), xy=(min(rounds), (n*.001)), xytext=(min(
        rounds), (n*.02)),
                arrowprops=dict(facecolor='red',
                                shrink=0.05))  # credit to https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html
    if isinstance(player, CardCounter):
        pylab.title(
        'Winnings for 99 hand night of Blackjack, \n \$10-\$1000 wager ramp, hi-lo counting ( %s '
        'trials)' % n)
    else:
        pylab.title(
        'Winnings for 99 hand night of Blackjack, \n \$100 wagers, Basic strategy ( %s trials)' % n)
    #  print(mu, sigma, n, bins)  # appears to be working great
    overlay_bell_curve(mu, sigma, n, bins)  # just wanting to call it and pass values through
    pylab.show()



if __name__ == '__main__': #plotting the bell curve on a different axis
    visualize(1000, player=Basic())  # basic
    visualize(1000, player=CardCounter())

#visualize(1000)
#visualize(1000, player=CardCounter())
