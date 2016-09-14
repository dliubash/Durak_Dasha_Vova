from functools import reduce


def validDefence(attack, defence, trumpSuit):
    """Returns True if the defence card is a valid defender, given the trump"""
    if attack[-1] != trumpSuit and defence[-1] == trumpSuit:
        #if the attack is not a trump and the defence is, defence succeeds.
        return True
    if attack[-1] == defence[-1] and higherValue(defence[:-1], attack[:-1]):
        #if the attack and defence are of the same suit, and the defence
        #is higher, defence succeeds
        return True
    #otherwise, the defence fails
    return False

def validAttack(attack, attackCount, maxAttackCount, inPlay):
    if attackCount == maxAttackCount:
        return False
    for card in inPlay:
        if attack[:-1] in card:
            return True
    return False

def playOrder(players, trump):
    """Takes a list of players and reorders them so that the one with the \
       lowest valued trump goes first"""
    hands = []
    for player in players:
        hands.append(player.hand)
    minHeldTrump = minTrump(list(map(lambda x: minTrump(x,trump), hands)),trump)
    for i in range(len(players)):
        if minHeldTrump in players[i].hand:
            return players[i:] + players [:i]

def higherValue(card1, card2):
    """Returns True when card1 has higher value than card2, false otherwise)"""
    order = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for value in order:
        if card2 == value:
            return True
        if card1 == value:
            return False
    #if neither card is in the order, returns false to avoid None-type operations
    return False

def minTrump(hand, trump):
    """Returns lowest valued trump in the given hand"""
    trumps =  list(filter(lambda x: False if x==None else trump in x, hand))
    if trumps == []:
        return None
    return reduce(lambda x,y: y if higherValue(x[0],y[0]) else x, trumps)
