import random
import agent

class Card:
    def __init__ (self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
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
                value = 0
                card = Card(suit, rank, value + 1)
                self.cards.append(card)
                
        return

class Game():
    def __init__(self):
        self.deck = Deck([])
        self.deck.generateDeck()

    def deal(self):
        index = random.randrange(len(self.deck.cards))
        dealt_Card = self.deck.cards.pop(index)
        print("dealt Card: " + dealt_Card.__toString__())
        return dealt_Card
        
    def refreshdeck(self):
        self.deck.cards.clear()
        self.deck.generateDeck()

    def round(self, player_1, player_2, round_count = 0):
        #players can be an agent.

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
        print(f"\nShowdown - {player_1.name}: {action_p1}, {player_2.name}: {action_p2}")
        return None  # Return winner determination logic
    
    def _get_player_action(self, player, valid_actions):
        while True:
            action = input(f"{player.name}, enter your action ({', '.join(valid_actions)}): ").lower().strip()
            if action in valid_actions:
                return action
            else:
                print(f"Invalid action. Please enter one of: {', '.join(valid_actions)}") 

    def round_helper(self, card_1, card_2, river_card):
        """
        Returns: 1 if player 1 wins, 2 if player 2 wins, 0 if tie.
        """
        rank_order = {'King': 3, 'Queen': 2, 'Jack': 1}
        suit_order = {'Spades': 2, 'Hearts': 1}
        
        # Check if each player has a pair with the river card
        p1_has_pair = card_1.rank == river_card.rank
        p2_has_pair = card_2.rank == river_card.rank
        
        # If only one player has a pair, they win
        if p1_has_pair and not p2_has_pair:
            return 1
        elif p2_has_pair and not p1_has_pair:
            return 2
        # If both have pairs (same rank), compare by suit
        elif p1_has_pair and p2_has_pair:
            if suit_order[card_1.suit] > suit_order[card_2.suit]:
                return 1
            elif suit_order[card_2.suit] > suit_order[card_1.suit]:
                return 2
            else:
                return 0  # Tie
        # No pairs, compare high cards
        else:

            p1_best = card_1 if rank_order[card_1.rank] >= rank_order[river_card.rank] else river_card
            p2_best = card_2 if rank_order[card_2.rank] >= rank_order[river_card.rank] else river_card
            
            # Compare best cards by rank
            if rank_order[p1_best.rank] > rank_order[p2_best.rank]:
                return 1
            elif rank_order[p2_best.rank] > rank_order[p1_best.rank]:
                return 2
            else:
                # Same rank, compare by suit
                if suit_order[p1_best.suit] > suit_order[p2_best.suit]:
                    return 1
                else:
                    return 2
       
def train_cfr(agent, iterations=10000, deck=None, ranks=None):
    
    util = 0
    if deck is None:
        fallback_deck = Deck([]) 
        fallback_deck.generateDeck() # fallback deck
    for _ in range(iterations):
        cards = random.sample(deck.cards, 3)
        util += agent.cfr(cards, "", 1, 1, pot=2, ranks=ranks)

    print("Average game value:", util / iterations)

    for info_set in agent.node_map:
        print(info_set, agent.node_map[info_set].get_average_strategy())


def main():
    game = Game()
    player_1 = agent.Agent(strategy_table={})
    player_2 = agent.Agent(strategy_table={})
    print("Test: player 1 is an untrained agent, player 2 is a trained agent (1k instances).")
    deck = Deck([])
    deck.generateDeck()
    print("Test deck: " + str(deck.cards))
    train_cfr(player_2, iterations=1000, deck=deck, ranks=['Jack', 'Queen', 'King'])

    for i in range(5):
        winner = game.round(player_1, player_2, round_count=i)
        if winner:
            print(f"{winner} wins round {i + 1}!\n")
        else:
            print(f"Round {i + 1} ended in a tie.\n")

main()