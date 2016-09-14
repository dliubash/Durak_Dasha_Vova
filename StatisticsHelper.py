import Game
import random
def runFirstRoundWithFixedHand(hand):
    deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
            '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
            '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
            '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
    deck = list(filter(lambda x: not x in hand,deck)) #remove cards in hand from deck
    random.shuffle(deck)#shuffle deck
    deck = deck + hand # add hand back, to be drawn by the player
    g = Game.Game(1,1,deck)#initialize game with rigged deck
    g.runFirstRound()#run first round