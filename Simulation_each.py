import csv
import random
import numpy
from CardCombs import CardCombs
from ObjectiveFunction import Utility
import GameAI


#hand - hand to attack; card_ind - number of the card to attack
def OneRoundWithFixedHand(deck=[],hand_attack = [], card_ind = None, myfile = ""):
    New_hand = []
    #deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
    #        '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
    #        '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
    #        '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
    
    if deck == []:
        deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
                '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
                '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
                '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
        random.shuffle(deck) 
    deck = list(filter(lambda x: not x in hand_attack,deck)) #remove cards in hand from deck
#shuffle deck
    #g = GameAI.Game(deck,hand_attack,card_ind)#initialize game with rigged deck
    g = GameAI.Game(deck, hand_attack, card_ind, 1, myfile)
    New_hand = g.runOneRound() #run one round
   
    return New_hand

def someRoundsWithFixedHand(deck=[],hand_attack = [], card_ind = None, num_rounds=0, myfile = ""):
    #New_hand = []
    #deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
    #        '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
    #        '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
    #        '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
    
    if deck == []:
        deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
                '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
                '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
                '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
        random.shuffle(deck) 
    deck = list(filter(lambda x: not x in hand_attack,deck)) #remove cards in hand from deck
    #g = GameAI.Game(deck,hand_attack,card_ind)#initialize game with rigged deck
    g = GameAI.Game(deck, hand_attack, card_ind, num_rounds, myfile)
    g.allRounds() #run one round


def MainLoop_each(deck,N=0):
    max_amount = 6 #max amount of cards in hand
    U = numpy.zeros((N,36))
    T = [[]*N]*36
    T = numpy.empty((N,36),dtype=object)
    hand0, hand1 = [],[]
    deck_upd=[]
    #H = []
    
    deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
            '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
            '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
            '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
    L=len(deck)
    
    for k in range(L): 
        hand0 = []
        hand0.append(deck[k])
        deck_upd = list(filter(lambda x: not x in hand0,deck))
        
        for j in range(N):
            random.shuffle(deck_upd) #!!!!!!!!!!!!!!!!!!!!SHUFFLE
            
            for i in range(max_amount-1):
                """take card from the end of deck similarly to the GameAI and append to fixed 1st attacker hand"""
                hand0.append(deck_upd[-i]) 
                
            Res = OneRoundWithFixedHand(deck_upd,hand0,0,"")
            T[j][k] = Res[1]
            u0 = Utility(hand0, Res[1])
            u1 = Utility(Res[0],Res[1])
            U[j][k] = (u1-u0)
            ##print(U[i][j])
            
    
        
        
      
    i=0
    with open('Utility_1M.csv', 'w',newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        while i<N:
            wr.writerow(U[i])
            i+=1
            
    i=0
    with open('Trumps_1M.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        while i<N:
            wr.writerow(T[i])
            i+=1    
    
    return U
   
            
    
    
    
    
    