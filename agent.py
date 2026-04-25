import csv
import os


def find_file(filename, search_path):
   for root, dirs, files in os.walk(search_path):
       if filename in files:
           return os.path.join(root, filename)
   return None
# finds the file wherever it is in case the submission messes up the path.

def writecsv():
    with open (find_file("q_table_csv.csv", 'C://'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["State", "Action", "Reward"])
        writer.writerow(["State1", "Action1", "Reward1"])
        writer.writerow(["State2", "Action2", "Reward2"])

def printcsv():
    with open (find_file("q_table_csv.csv", 'C://'), 'r') as file:

        reader = csv.reader(file)
        for row in reader:
            print(row)
            #what am I doing wrong :<
        
#the decision maker should be a Monte Carlo Tree that uses the q table as a heuristic

def evaluateHand(card):
    if card.rank == 'King':
        return("King lol")
    else:
        return ("I have a " + card.rank + ' of ' + card.suit)
def playHand(hand, q_table):
    pass
    
#evaluate hand should access the csv as a Q learning algoritm s