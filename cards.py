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
                self.cards.append(card)
                
        return

class Game():
    def __init__(self):
        self.deck = Deck([])
        self.deck.generateDeck()

    def deal(self):
        dealt_Card = random.choice(self.deck.cards)
        return dealt_Card.__toString__()
        
    def refreshdeck(self):
        self.deck = Deck({})
        self.deck.generateDeck()

#test
#print(agent.evaluateHand(Card('Hearts', 'Queen')))
#print(agent.evaluateHand(Card('Hearts', 'King')))
#print('/?//////')
print('Agent csv test: ')
agent.printcsv()

#print('\n' + 'Deck test: ')
#testgame = Game()
#print(testgame.deck.cards) #fixme
#print('deal test')
#print('\n')
#print(testgame.deal())
#TODO: player class which the agent will be. make it recieve dealt cards and have play methods.