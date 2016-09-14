import DurakRulesHelperFunctions
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def addCard(self, card):
        """Adds a card to the hand"""
        if card != None:
            self.hand.append(card)

    def removeCard(self, index):
        """Removes the card at the given index from the hand"""
        self.hand = self.hand[:index] + self.hand[index+1:]

    def promptFirstAttack(self, defender):
        """Asks player to chose a card to begin a bout"""
        pass

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to choose a followup attack, and if none is chosen, asks whether assistance is allowed. Returns None if assistance is requested"""
        pass

    def promptAssistAttack(self, attacker, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to chose an assist attack"""
        pass

    def promptDefence(self, attacker, attack, trump):
        """Asks player to defend from an attack"""
        pass

    def promptDumpExtraCards(self, defender, inPlay, attackCount, maxAttackCount):
        """Prompts a player to give their extra cards to the defender after they cave conceded a bout"""
        pass


class AIPlayer(Player):

    def __init__(self, name): #DL - if we need to use fixed card From which the bout starts
        Player.__init__(self,name)        
        self.card_ind = None 

        """Gives a number of the card which starts the bout"""
    def changeCardInd(self, k): #DL
        self.card_ind = k         
    
    def promptFirstAttack(self, defender):
        """Start game from the known card"""
        selection = self.card_ind #index of the card - in fact, integer
        attack = self.hand[selection]
        self.removeCard(selection) #move card from the hand
        return attack

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to choose a followup attack, and if none is chosen, asks whether assistance is allowed. Returns None if assistance is requested"""
        for card in self.hand:
            if DurakRulesHelperFunctions.validAttack(card, attackCount, maxAttackCount, inPlay):
                attack = card
                self.removeCard(self.hand.index(attack))#DL
                return attack
        return "" #if the further attack is not possible, return ""
        pass

    def promptAssistAttack(self, attacker, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to chose an assist attack"""
        pass
    
    def promptDefence(self, attacker, attack, trump):
        """Asks player to defend from an attack"""
        for card in self.hand:
            if DurakRulesHelperFunctions.validDefence(attack, card, trump[-1]):
                self.removeCard(self.hand.index(card))#DL
                return card
        return ""

    def promptDumpExtraCards(self, defender, inPlay, attackCount, maxAttackCount):
        """Prompts a player to give their extra cards to the defender after they cave conceded a bout"""
        addedCards = []
        for card in self.hand:
            if DurakRulesHelperFunctions.validAttack(card, attackCount, maxAttackCount, inPlay):
                attack = card
                addedCards.append(attack)
                # attackCount += 1  # (?? - present in GameAI) 
                self.removeCard(self.hand.index(attack))
        return addedCards

