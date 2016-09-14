import csv
import random
import numpy
from CardCombs import CardCombs
from ObjectiveFunction import Utility
import GameAI
from download_stats import printArray3D

#hand - hand to attack; card_ind - number of the card to attack
def OneRoundWithFixedHand(hand_attack=[],card_ind=None):
    New_hand = []
    deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
            '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
            '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
            '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
    deck = list(filter(lambda x: not x in hand_attack,deck)) #remove cards in hand from deck
    random.shuffle(deck) #shuffle deck
    g = GameAI.Game(deck,hand_attack,card_ind)#initialize game with rigged deck
    New_hand = g.runOneRound() #run one round
    
    return New_hand

def MainLoop_each(deck,N=0):
    max_amount = 6 #max amount of cards in hand
    U = numpy.zeros((N,36))
    hand0, hand1 = [],[]
    deck_upd=[]
    #H = []
    
    deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
            '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
            '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
            '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
    L=len(deck)
    
    for k in range(L):
        hand0 = []
        hand0.append(deck[k])
        deck_upd = list(filter(lambda x: not x in hand0,deck))
        random.shuffle(deck_upd)
        for i in range(max_amount-1):
            hand0.append(deck_upd[i])
        #H.append(hand0)
        
        for j in range(N):
            Res = OneRoundWithFixedHand(hand0,0)
            u0 = Utility(hand0, Res[1])
            u1 = Utility(Res[0],Res[1])
            U[j][k] = (u1-u0)
            ##print(U[i][j])
            
    
        
        
      
    i=0
    with open('test.csv', 'w',newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        while i<N:
            wr.writerow(U[i])
            i+=1  
    
    return U
   
            
    
    
    
    
    