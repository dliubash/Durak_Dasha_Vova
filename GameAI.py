import random
import DurakRulesHelperFunctions
from random import randint
from Player import AIPlayer
class Game:
    def __init__(self, deck = [],hand_attack = [], card_ind=None, num_rounds=None):
        #initialize and shuffle deck
        numAIPlayers = 2
        
        self.num_rounds = num_rounds
        
        if hand_attack == []:
            raise ValueError('Hand is empty!')
        
        if card_ind is None and len(hand_attack) > 0:
            card_ind = randint(0,len(hand_attack)-1)
            #print(card_ind, " is index of starting card. OK")
        
        if deck == []:
            self.deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
                         '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
                         '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
                         '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
            random.shuffle(self.deck)
        else:
            self.deck = deck
        self.trump = self.deck[0]
        #initialize 2 players
        self.players = []
        for i in range(numAIPlayers):
            self.players.append(AIPlayer("Player " + str(i+1)))
        #deal hands
        for i in range(len(hand_attack)):
                self.players[0].addCard(hand_attack[i]) #1st hand is fixed
                self.players[1].addCard(self.drawCard()) #defender obtains random cards
        self.players[0].changeCardInd(card_ind)

        
    def allRounds(self):
        """"now we skip the rule about starting player with minimal trump"""
        """num_rounds is None if we want the whole game - maximum number of rounds"""
        #self.players = DurakRulesHelperFunctions.playOrder(self.players,self.trump[-1])

        roundsCounter = 0    #If num_rounds is not None, only specified number of them is played; otherwise till the end of game
        new_card_ind = 0

        while len(self.players) > 1 and ((self.num_rounds is None) or (self.num_rounds is not None and roundsCounter < self.num_rounds)): #in the end players without cards are removed
            print("Round ", roundsCounter)
            print("attacker.card_ind in begin of round: " + str(self.players[0].card_ind) )
            print("defender.card_ind in begin of round: " + str(self.players[1].card_ind) )
            print(self.players[0].name + " is Player 0 at the beginning")
             
            self.runOneRound()                    

            new_card_ind = randint(0, max(1, len(self.players[0].hand) ) -1) #random start of next round
            self.players[0].changeCardInd(new_card_ind) #card which starts next round since now player 0 is next attacker
            
            self.players = list(filter(lambda x: len(x.hand) != 0, self.players)) #remove players who have run out of cards
            roundsCounter += 1

            #print("attacker.card_ind in end of round: " + str(self.players[0].card_ind) )
            #print("defender.card_ind in end of round: " + str(self.players[1].card_ind) )
                  
            #print(self.players[0].name + " is Player 0 at the end")
                  
                  
        if len(self.players) == 1: #if only one player has cards, they are the loser
            print(self.players[0].name + " is the only player still holding cards! They are the Durak!")
            return self.players[0].name #somebody loses the game
        
        if len(self.players) == 0: #if all players have run out of cards, game is a draw
            print("No one has any cards left! This round is a draw.")
        return "draw" #if nobody loses, it is a draw
    
                                             
                                        
    def runOneRound(self):
        
        res = [[]*6]*2
        print("Welcome to Durak. The Trump card is " + self.trump)

        print("Note: when prompted for the index of a card, the indices start at 0.")
        
        attacker = self.players[0] #attacker is first in the turn order
        defender = self.players[1] #defender is next
        


        print("attacker.card_ind: " + str(attacker.card_ind))#debug
        print("defender.card_ind: " + str(defender.card_ind))#debug

        print("attacker.hand: ", attacker.hand)#debug
        print("defender.hand: ", defender.hand)#debug

        
        inPlay = [] #cards that have been played this bout
        attackCount = 0
        maxAttackCount = min(len(defender.hand), 6) #maximum number of attacks is either 6 or the number of cards the defender has, whichever is smaller
        print("attacker.hand index " + str(attacker.card_ind))  #debug
        
        attack = attacker.promptFirstAttack(defender)
        inPlay.append(attack) #add card to field
        
        print("inPlay: ", inPlay)#debug

        
        attackCount += 1
        defence = defender.promptDefence(attacker, attack, self.trump)                        
        print(defender.name + " has defended with a " + defence + ". The cards currently in play are:")

           
        
        while defence != "" and attack != "":
            inPlay.append(defence)
            #print(inPlay)         
            attack = attacker.promptFollowupAttack(defender, inPlay, attackCount, maxAttackCount)
            if attack != "": #if the attacker attacked
                inPlay.append(attack) #add card to field
                print(attacker.name + " has attacked with a " + attack + ". The cards currently in play are:")
                print(inPlay)         
                attackCount += 1
                defence = defender.promptDefence(attacker, attack, self.trump)
                print(defender.name + " has defended with a " + defence + ". The cards currently in play are:")
                print("attacker.hand: ", attacker.hand)#debug
                print("defender.hand: ", defender.hand)#debug

                
                
        if defence == "": #defender has chosen not to defend
            print(defender.name + " has conceded the attack.")
            for player in [self.players[0]]+self.players[2:]: #in fact, for 2 Players it is only attacker
                dumpedCards = player.promptDumpExtraCards(defender, inPlay, attackCount, maxAttackCount)
                inPlay += dumpedCards
                attackCount += len(dumpedCards)
            print("The following cards have been added to " + defender.name + "'s hand:")
            print(inPlay)
            defender.hand += inPlay #if the defender concedes, add cards in play to their hand
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard())
            self.players = self.players[2:] + self.players[:2] #defenders turn is skipped if they concede


  

        if attack == "": #attacker has chosen to stop attacking
            print("The attack has ended. the following cards have been removed from play:")
            print(inPlay)
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard()) 
            self.players = self.players[1:] + self.players[:1] #attacker moves to end of turn order, defender attacks next

        
                
        print("Your cards are now: ", attacker.hand)
        print("Defender cards are now: ",defender.hand)
        
        res[0] = self.returnHand(attacker)
        res[1] = self.trump
        
        return res

    
    
    
    
    def drawCard(self):
        """Removes the last card in the deck and returns its value"""
        if self.deck != []:
            dealtCard = self.deck[-1]
            self.deck = self.deck[:-1]
            return dealtCard

    def returnHand(self,player):
        return player.hand
