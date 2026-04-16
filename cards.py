import random
import agent

class Card:
    def __init__ (self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __toString__(self):
        return self.rank + ' of ' + self.suit
        
class Deck:
    def __init__ (self, cards):
        self.cards = cards
    
    def generateDeck(self):
        suits = ['Hearts', 'Spades']
        ranks = ['Jack', 'Queen', 'King']
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards[card.__toString__()] = card
                
        return

class game():
    def __init__(self):
        self.deck = Deck({})
        self.deck.generateDeck()

    def deal():
        pass

#test
print(agent.evaluateHand(Card('Hearts', 'Queen')))
print(agent.evaluateHand(Card('Hearts', 'King')))
agent.printcsv
#TODO: player class which the agent will be. make it recieve dealt cards and have play methods.