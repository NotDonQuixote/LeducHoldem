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

cfr = CFR(actions=actions, node_class=Node)
class Agent:
    def __init__(self, strategy_table, card=None):
        self.q_table = {} #delete later
        self.round_count = 0 #Delete 
        self.csv_file = find_file("q_table_csv.csv", 'C://') #delete later if CRF works
        self.load_q_table() #delete later if CFR works
        self.card = card
        self.strategy_table = strategy_table
    
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

def find_file(filename, search_path):
   for root, dirs, files in os.walk(search_path):
       if filename in files:
           return os.path.join(root, filename)
   return None
# finds the file wherever it is in case the submission messes up the path.
def writecsv():
    #the cards will be a linear list of integers going up in rank and value
    '''
    1 - Jack of Hearts
    2 - Jack of Spades
    3 - Queen of Hearts
    4 - Queen of Spades
    5 - King of Hearts
    6 - King of Spades
    '''
    with open (find_file("q_table_csv.csv", 'C://'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([1, "State", "Action", "Reward"])
        writer.writerow([2, "State1", "Action1", "Reward1"])
        writer.writerow([3, "State2", "Action2", "Reward2"])

def printcsv():
    with open (find_file("q_table_csv.csv", 'C://'), 'r') as file:

        reader = csv.reader(file)
        for row in reader:
            print(row)
            #what am I doing wrong :<
        
#the decision maker will use CounterFactual regret minimization. 
#TODO: make a game tree and CFR algorithm then remove the Q-table approach


class DeleteLater:
    
    def load_q_table(self):
        if self.csv_file and os.path.exists(self.csv_file):
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3:
                        state, action, reward = row[0], row[1], row[2]
                        if state not in self.q_table:
                            self.q_table[state] = {}
                        self.q_table[state][action] = float(reward)
    
    def update_q_table(self, state, action, reward):
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = reward
        self.round_count += 1
        
        # Save to CSV every 200 rounds
        if self.round_count % 200 == 0:
            self.save_q_table()
    
    def save_q_table(self):
        if self.csv_file:
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["State", "Action", "Reward"])
                for state, actions in self.q_table.items():
                    for action, reward in actions.items():
                        writer.writerow([state, action, reward])
    
    def get_q_value(self, state, action):
        if state in self.q_table and action in self.q_table[state]:
            return self.q_table[state][action]
        return 0.0