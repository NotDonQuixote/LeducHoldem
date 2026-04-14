class Card:
    def __init__ (self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __toString__(self):
        return self.rank + ' of ' + self.suit
        
class Deck:
    def __init__ (self, cards):
        self.cards = {}
    
    def generateDeck(self):
        suits = ['Hearts', 'Spades']
        ranks = ['Jack', 'Queen', 'King']
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards[card.__toString__()] = card
                
        return


test = Deck({})
test.generateDeck()

print("cards: "  + str(test.cards.keys()))


