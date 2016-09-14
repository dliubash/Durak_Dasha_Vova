import random
import DurakRulesHelperFunctions
from Player import AIPlayer
class Game:
    def __init__(self, deck=[],hand_attack = [], card_ind=None):
        #initialize and shuffle deck
        numAIPlayers = 2
        
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
        for i in range(6):
                self.players[0].addCard(hand_attack[i]) #1st hand is fixed
                self.players[1].addCard(self.drawCard()) #defender obtains random cards
        self.players[0].changeCardInd(card_ind)

                                         
                                        
    def runOneRound(self):
        
        res = [[]*6]*2
        #print("Welcome to Durak. The Trump card is " + self.trump)

        #print("Note: when prompted for the index of a card, the indices start at 0.")
        
        attacker = self.players[0] #attacker is first in the turn order
        defender = self.players[1] #defender is next


        #print("attacker.card_ind: " + str(attacker.card_ind))#debug
        #print("defender.card_ind: " + str(defender.card_ind))#debug

        #print("attacker.hand: ", attacker.hand)#debug
        #print("defender.hand: ", defender.hand)#debug

        
        inPlay = [] #cards that have been played this bout
        attackCount = 0
        maxAttackCount = min(len(defender.hand), 6) #maximum number of attacks is either 6 or the number of cards the defender has, whichever is smaller
        #print("attacker.hand index " + str(attacker.card_ind))  #debug
        
        attack = attacker.promptFirstAttack(defender)
        inPlay.append(attack) #add card to field
        
        #print("inPlay: ", inPlay)#debug

        
        attackCount += 1
        defence = defender.promptDefence(attacker, attack, self.trump)                        
        #print(defender.name + " has defended with a " + defence + ". The cards currently in play are:")

           
        
        while defence != "" and attack != "":
            inPlay.append(defence)
            #print(inPlay)         
            attack = attacker.promptFollowupAttack(defender, inPlay, attackCount, maxAttackCount)
            if attack != "": #if the attacker attacked
                inPlay.append(attack) #add card to field
                #print(attacker.name + " has attacked with a " + attack + ". The cards currently in play are:")
                #print(inPlay)         
                attackCount += 1
                defence = defender.promptDefence(attacker, attack, self.trump)
                #print(defender.name + " has defended with a " + defence + ". The cards currently in play are:")
                #print("attacker.hand: ", attacker.hand)#debug
                #print("defender.hand: ", defender.hand)#debug

                
                
        if defence == "": #defender has chosen not to defend
            #print(defender.name + " has conceded the attack.")
            for player in [self.players[0]]+self.players[2:]: #in fact, for 2 Players it is only attacker
                dumpedCards = player.promptDumpExtraCards(defender, inPlay, attackCount, maxAttackCount)
                inPlay += dumpedCards
                attackCount += len(dumpedCards)
            #print("The following cards have been added to " + defender.name + "'s hand:")
            #print(inPlay)
            defender.hand += inPlay #if the defender concedes, add cards in play to their hand
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard())


  

        if attack == "": #attacker has chosen to stop attacking
            #print("The attack has ended. the following cards have been removed from play:")
            #print(inPlay)
            for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                if len(player.hand) < 6:
                    for _ in range(min(6 - len(player.hand), len(self.deck))):
                        player.addCard(self.drawCard()) 

        
                
        #print("Your cards are now: ", attacker.hand)
        #print("Defender cards are now: ",defender.hand)
        
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
