import csv
import os
import random
from agent_CFR import CFR
from collections import defaultdict

actions = ['call', 'bet']
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

class Agent:
    def __init__(self, strategy_table, card=None):
        self.card = card
        self.strategy_table = strategy_table
        cfr = CFR(actions=actions, node_class=Node)
        self.cfr = cfr.cfr
    
    def new_card(self, card):
        self.card = card

    def get_strategy(self):
        table = {}
        for info_set, node in self.node_map.items():
            table[info_set] = node.get_average_strategy()
        return table

    def playHand(self, river_card, history):
        info = build_info(self, river_card, history)

        strategy = self.strategy_table.get(info)

        if strategy is None:
            return random.choice(['call', 'bet'])
        
        return self.action(self, strategy)
    
    def action(self, strategy):
        rand = random.random()
        cumulative_probability = 0.0
        for action, prob in strategy.items():
            cumulative_probability += prob
            if rand <= cumulative_probability:
                return action
        return 'call' #just in case


def build_info(agent_card, river_card, history):
    private_rank = agent_card.rank 
    river_rank = river_card.rank if river_card is not None else "None"
    return f"{private_rank}|{river_rank}|{history}"
