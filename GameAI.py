"""now only 2 players - NO ASSIST ATTACK (later will be added from Ben's code)"""
import random
import DurakRulesHelperFunctions
from random import randint
from Player import AIPlayer
class Game:
    
    def __init__(self, deck = [],hand_attack = [], card_ind=None, num_rounds=None, myfile = ""):
        
        numAIPlayers = 2
        
        """File to write comments. If is ""  - nothing happens"""        
        self.myfile = myfile
    
        """Number of game rounds"""
        self.num_rounds = num_rounds

        """Starting hand is missing? It should not be!"""        
        if hand_attack == []:
            raise ValueError('Hand is empty!')

        """randomize initial card in given hand if card_ind is missing"""        
        if card_ind is None and len(hand_attack) > 0:
            card_ind = self.randInt(len(hand_attack))
        
        """initialize deck (if it is [], create and shuffle)"""        
        if deck == []:
            self.deck = ['6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',\
                         '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',\
                         '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',\
                         '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
            random.shuffle(self.deck)
        else:
            self.deck = deck
                      
        self.printComments("deck = "+ str(self.deck) + '\n')
        self.printComments("length of deck = "+ str(len(self.deck)) + '\n')
            
        """remove cards in hand from deck"""                    
        self.deck = list(filter(lambda x: not x in hand_attack,self.deck)) 
        
        self.printComments("filtered deck = "+ str(self.deck) + '\n')
        self.printComments("length of filtered deck = "+ str(len(self.deck)) + '\n')

        """define the trump"""                                  
        self.trump = self.deck[0]
        
        """initialize 2 players"""                      
        self.players = []
        for i in range(numAIPlayers):
            self.players.append(AIPlayer("Player " + str(i+1)))

        """deal hands"""                      
        for i in range(len(hand_attack)):
                self.players[0].addCard(hand_attack[i]) #1st hand is fixed
                self.players[1].addCard(self.drawCard()) #defender obtains random cards
        self.players[0].changeCardInd(card_ind)

        
    def allRounds(self):
        """"now we skip the rule about starting player with minimal trump"""
        """num_rounds is None in case we want the whole game - maximum number of rounds"""
        #self.players = DurakRulesHelperFunctions.playOrder(self.players,self.trump[-1])

        """"If num_rounds is not None, only specified number of them is played; otherwise till the end of game"""
        roundsCounter = 0    
        new_card_ind = 0

        while len(self.players) > 1 and ((self.num_rounds is None) or (self.num_rounds is not None and roundsCounter < self.num_rounds)): #in the end players without cards are removed
            self.printComments("Round " + str(roundsCounter) + '\n')
            self.printComments("attacker.card_ind in begin of round: " + str(self.players[0].card_ind) + '\n' )
            self.printComments("defender.card_ind in begin of round: " + str(self.players[1].card_ind) + '\n' )
            self.printComments(self.players[0].name + " is Player 0 at the beginning"  + '\n')
             
            self.runOneRound()                    

            new_card_ind = self.randInt(  max(1,len(self.players[0].hand)) )  #random start of next round
            self.players[0].changeCardInd(new_card_ind) #card which starts next round since now player 0 is next attacker
            
            self.players = list(filter(lambda x: len(x.hand) != 0, self.players)) #remove players who have run out of cards
            roundsCounter += 1

            #self.printComments("attacker.card_ind in end of round: " + str(self.players[0].card_ind) )
            #self.printComments("defender.card_ind in end of round: " + str(self.players[1].card_ind) )
                  
            #self.printComments(self.players[0].name + " is Player 0 at the end")
                  
                  
        if len(self.players) == 1: #if only one player has cards, they are the loser
            self.printComments(self.players[0].name + " is the only player still holding cards! They are the Durak!" + '\n')
            return self.players[0].name #somebody loses the game if the whole game was played
        
        if len(self.players) == 0: #if all players have run out of cards, game is a draw
            self.printComments("No one has any cards left! This round is a draw." + '\n')
        return "draw" #if nobody loses, it is a draw
    
                                             
                                        
    def runOneRound(self):
        
        res = [[]*6]*2
        self.printComments("Welcome to Durak. The Trump card is " + self.trump + '\n')

        self.printComments("Note: when prompted for the index of a card, the indices start at 0." + '\n')
        
        attacker = self.players[0] #attacker is first in the turn order
        defender = self.players[1] #defender is next
        


        self.printComments("attacker.card_ind: " + str(attacker.card_ind) + '\n')
        self.printComments("defender.card_ind: " + str(defender.card_ind) + '\n')

        self.printComments("attacker.hand: " + str(attacker.hand) + '\n')
        self.printComments("defender.hand: " + str(defender.hand) + '\n')

        
        inPlay = [] #cards that have been played this bout
        attackCount = 0
        
        """ Maximum number of attacks is either 6 or the number of cards the defender has, whichever is smaller """
        maxAttackCount = min(len(defender.hand), 6) 
        self.printComments("attacker.hand index " + str(attacker.card_ind) + '\n')  
        
        attack = attacker.promptFirstAttack(defender)
        inPlay.append(attack) #add card to field
        
        self.printComments("inPlay: " + str(inPlay) + '\n')

        
        attackCount += 1
        defence = defender.promptDefence(attacker, attack, self.trump)                        
        self.printComments(defender.name + " has defended with a " + defence + ". The cards currently in play are:" + '\n')

           
        
        while defence != "" and attack != "":
            inPlay.append(defence)        
            attack = attacker.promptFollowupAttack(defender, inPlay, attackCount, maxAttackCount) #attacker continues his movement
            if attack != "": #if the attacker attacked
                inPlay.append(attack) #add card to field
                self.printComments(attacker.name + " has attacked with a " + attack + ". The cards currently in play are:" + '\n')
                self.printComments(str(inPlay) + '\n')         
                attackCount += 1
                defence = defender.promptDefence(attacker, attack, self.trump)
                self.printComments(defender.name + " has defended with a " + defence + ". The cards currently in play are:" + '\n')
                self.printComments(str(inPlay) + '\n')         
                self.printComments("attacker.hand: " + str(attacker.hand) + '\n')
                self.printComments("defender.hand: " + str(defender.hand) + '\n')

                
                
        if defence == "": #defender has chosen not to defend
            self.printComments(defender.name + " has conceded the attack." + '\n')
            for player in [self.players[0]]+self.players[2:]: #in fact, for 2 Players it is only attacker
                dumpedCards = player.promptDumpExtraCards(defender, inPlay, attackCount, maxAttackCount)
                inPlay += dumpedCards
                attackCount += len(dumpedCards)
            self.printComments("The following cards have been added to " + defender.name + "'s hand:" + '\n')
            self.printComments(str(inPlay) + '\n')
            defender.hand += inPlay #if the defender concedes, add cards in play to their hand
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard())
            self.players = self.players[2:] + self.players[:2] #defenders turn is skipped if they concede


  

        if attack == "": #attacker has chosen to stop attacking
            self.printComments("The attack has ended. the following cards have been removed from play:" + '\n')
            self.printComments(str(inPlay) + '\n')
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard()) 
            self.players = self.players[1:] + self.players[:1] #attacker moves to end of turn order, defender attacks next

        
                
        self.printComments("Your cards are now: " + str(attacker.hand) + '\n')
        self.printComments("Defender cards are now: " + str(defender.hand) + '\n')
        
        res[0] = self.returnHand(attacker)
        res[1] = self.trump
        
        self.printComments('\n')
        self.printComments('\n')

        return res

    
    
    
    
    def drawCard(self):
        """Removes the last card in the deck and returns its value"""
        if self.deck != []:
            dealtCard = self.deck[-1]
            self.deck = self.deck[:-1]
            return dealtCard

    def returnHand(self,player):
        return player.hand
    
    def randInt(self, maximum):
        return randint(0,maximum-1)
    
    def printComments(self,text):
        if self.myfile != "":
            with open(self.myfile, 'a') as the_file:
                the_file.write(text)