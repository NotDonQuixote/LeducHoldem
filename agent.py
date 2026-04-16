import csv

#with open ('q_table_csv.csv') as file:
    #q_table = file.read()

def printcsv():
    with open ('q_table_csv.csv') as file:
        q_table = file.read()
        for line in q_table:
            print(line)
            #what am I doing wrong :<


def evaluateHand(card):
    if card.rank == 'King':
        return("King lol")
    else:
        return ("I have a " + card.rank + ' of ' + card.suit)

