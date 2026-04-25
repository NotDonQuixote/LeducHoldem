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
        index = random.randrange(len(self.deck.cards))
        dealt_Card = self.deck.cards.pop(index)
        return dealt_Card
        
    def refreshdeck(self):
        self.deck.clear()
        self.deck.generateDeck()

    def round(self, player_1, player_2, round_count = 0):
        

        print("Round: " + str(round_count + 1))
        self.refreshdeck()
        card_p1 = self.deal()
        card_p2 = self.deal()
        river_card = self.deal()
        
        # Deal cards to players
        print(f"{player_1.name} has: {card_p1}")
        print(f"{player_2.name} has: {card_p2}")
        print(f"River card is: {river_card}")
        
        # Get actions from players
        valid_actions = ['call', 'fold', 'raise']
        
        # Player 1's turn
        action_p1 = self._get_player_action(player_1, valid_actions)
        if action_p1 == 'fold':
            print(f"{player_1.name} folded. {player_2.name} wins!")
            return player_2
        
        # Player 2's turn
        action_p2 = self._get_player_action(player_2, valid_actions)
        if action_p2 == 'fold':
            print(f"{player_2.name} folded. {player_1.name} wins!")
            return player_1
        
        # If both players call (or raise), compare hands
        print(f"\nFinal actions - {player_1.name}: {action_p1}, {player_2.name}: {action_p2}")
        return None  # Return winner determination logic
    
    def _get_player_action(self, player, valid_actions):
        """Get and validate player action input"""
        while True:
            action = input(f"{player.name}, enter your action ({', '.join(valid_actions)}): ").lower().strip()
            if action in valid_actions:
                return action
            else:
                print(f"Invalid action. Please enter one of: {', '.join(valid_actions)}") 

    def round_helper(card_1, card_2):
        pass

#test
#print(agent.evaluateHand(Card('Hearts', 'Queen')))
#print(agent.evaluateHand(Card('Hearts', 'King')))
#print('/?//////')
print('deck test ')
print('\n')
tst1 = Game()

for x in tst1.deck.cards:
    print(x.suit)

print("deal test")
print(tst1.deal().__toString__())
print("\n" + 'deck after dealt card: ')
for x in tst1.deck.cards:
    print(x.suit)
print('Agent csv test: ')
agent.printcsv()

#print("Write test:")
#agent.writecsv()

#print('after write csv test: ')
#agent.printcsv()
#print('\n' + 'Deck test: ')
#testgame = Game()
#print(testgame.deck.cards) #fixme
#print('deal test')
#print('\n')
#print(testgame.deal())
#TODO: player class which the agent will be. make it recieve dealt cards and have play methods.