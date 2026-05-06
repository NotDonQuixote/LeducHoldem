import random
from collections import defaultdict
# CFR class for integration with agent.py
class CFR:
    def __init__(self, actions=None, node_class=None):
        # Use actions from agent.py if provided, else default
        self.actions = actions if actions is not None else ['call', 'bet', 'fold']
        # Use Node from agent.py if provided, else fallback
        self.Node = node_class if node_class is not None else self._default_node_class()
        self.node_map = {}

    def _default_node_class(self):
        actions = self.actions
        class Node:
            def __init__(self, info_set):
                self.info_set = info_set
                self.regret_sum = defaultdict(float)
                self.strategy = {a: 0.0 for a in actions}
                self.strategy_sum = defaultdict(float)

            def get_strategy(self, realization_weight, iteration=None, delay =0):
                normalizing_sum = 0
                for a in actions:
                    self.strategy[a] = max(self.regret_sum[a], 0)
                    normalizing_sum += self.strategy[a]

                for a in actions:
                    if normalizing_sum > 0:
                        self.strategy[a] /= normalizing_sum
                    else:
                        self.strategy[a] = 1 / len(actions)
                    if iteration is None or iteration > delay:
                        self.strategy_sum[a] += realization_weight * self.strategy[a]

                return self.strategy
            def update_regret(self, action, regret):
                self.regret_sum[action] = max(0.0, self.regret_sum[action] + regret)
            def get_average_strategy(self):
                avg_strategy = {}
                normalizing_sum = sum(self.strategy_sum.values())
                for a in actions:
                    if normalizing_sum > 0:
                        avg_strategy[a] = self.strategy_sum[a] / normalizing_sum
                    else:
                        avg_strategy[a] = 1.0 / len(actions)
                return avg_strategy
        return Node

    def is_terminal(self, history, max_length=10):
        # Terminal
        if history.endswith("f"):
            return True
        # Terminal if there have been two bets
        if history.count('b') >= 2:
            return True
        # Terminal: showdown
        if len(history) >= 2 and history[-2:] == "cc":
            return True
        # Safeguard:
        if len(history) >= max_length: 
            return True
        return False

    def payoff(self, cards, history, pot, ranks=None):
        # folding case
        if history.endswith("f"):
            player = len(history) % 2
            return pot if player == 1 else -pot

        # showdown
        p1, p2, public = cards
        def hand_strength(card, public):
            if card.rank is None:
                # fallback: treat card as int
                return 10 + card if card == public else card
            if card == public:
                #print("for debugging: card is " + str(card) + " and public is " + str(public))
                #print('\n')
                #print("ranks list is " + str(ranks))
                return 10 + ranks.index(card)
            #print("for debugging: card is " + str(card) + " and public is " + str(public))
            #print('\n')
            #print("ranks list is " + str(ranks))

            return ranks.index(card.rank) #now a card object

        s1 = hand_strength(p1, public)
        s2 = hand_strength(p2, public)

        if s1 > s2:
            return pot
        elif s2 > s1:
            return -pot
        return 0

    def get_info_set(self, player, card, public, history):
        return f"{card}|{public}|{history}"

    def cfr(self, cards, history, p0, p1, pot, ranks=None):
        player = len(history) % 2

        if self.is_terminal(history):
            #print("Function: is_terminal, returning payoff for cards"+ str(cards))
            #print("test: cards using value function to call from deck: " + str())
            return self.payoff(cards, history, pot, ranks)

        card = cards[player]
        public = cards[2] if len(history) > 2 else None
        info_set = self.get_info_set(player, card, public, history)

        if info_set not in self.node_map:
            self.node_map[info_set] = self.Node(info_set)

        node = self.node_map[info_set]
        strategy = node.get_strategy(p0 if player == 0 else p1)

        util = {}
        node_util = 0

        for a in self.actions:
            next_history = history + a
            next_pot = pot + (1 if a == 'b' else 0)

            if player == 0:
                util[a] = -self.cfr(cards, next_history, p0 * strategy[a], p1, next_pot, ranks)
            else:
                util[a] = -self.cfr(cards, next_history, p0, p1 * strategy[a], next_pot, ranks)

            node_util += strategy[a] * util[a]

        for a in self.actions:
            regret = util[a] - node_util
            if player == 0:
                node.regret_sum[a] = max(0, node.regret_sum[a]+ regret)
            else:
                node.regret_sum[a] += max(0, node.regret_sum[a]+ regret)

        return node_util

    # Training is now handled by train_cfr in cards.py