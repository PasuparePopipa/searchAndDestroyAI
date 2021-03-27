import random
import math
import numpy
from copy import copy, deepcopy
from itertools import combinations

#Cell properties
#x and y represent the coordinates, X is vertical, Y is horizontal
#z represents the state, flat, hill, forest, or cave
#target tells us if that cell is the target or not
class Cell:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.state = z
        self.target = False
#Our agent, x and y tell us the agent's current position
#believe is our 2D array of probabilities
class Agent:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.belief = z

#Generate the search and destroy board,
#1/4 chance of each cell being flat, hilly, forested, and cave
def generateBoard(d):
    board = []
    #Create Board of x and y
    for x in range(d):
        board2 = []
        for y in range(d):
            rand = random.randint(1,4)
            if rand == 1:
                board2.append(Cell(x,y,'flat'))
            elif rand == 2:
                board2.append(Cell(x,y,'hill'))
            elif rand == 3:
                board2.append(Cell(x,y,'forest'))
            elif rand == 4:
                board2.append(Cell(x,y,'cave'))
        board.append(board2)
    #total Cells
    #Set a random target in a cell
    totalCells = d*d
    rand = random.randint(1,totalCells)
    counter = 1
    for x in range(d):
        for y in range(d):
            if counter == rand:
                board[x][y].target = True
            counter = counter + 1
    return board

#Generates the initial state of Agents belief about the board 
#P(Target in Celli) = 1 / # of Cells
def generateInitialBelief(z):
    board = []
    #Create Board of x and y
    for x in range(len(z)):
        board2 = []
        for y in range(len(z)):
            p = 1/(len(z)*len(z))
            board2.append(p)
        board.append(board2)
    #total Cells
    return board

#Print out current board based on state
def printBoard(board):
    for row in board:
        for cell in row:
            print(cell.state)
#Print out current board of beliefs
def printBelief(board):
    for row in board:
        for cell in row:
            print(cell)

def startAgent():
    tmp = generateBoard(20)
    belief = generateInitialBelief(tmp) 
    startLocationX = random.randint(0,len(tmp))
    startLocationY = random.randint(0,len(tmp))
    bob = Agent(startLocationX,startLocationY,belief)
    return bob, tmp

#Iteratively travel to the cell with the highest probability of containing the target, search
#that cell. Repeat until target is found.
def basicAI1(board,agent):
    
    #Travel to Cell with Highest probability of containing target, keep track of distance

    #search

    #Update network



    print('over')
    
#Iteratively travel to the cell with the highest probability of finding the target within that
#cell, search that cell. Repeat until the target is found.
def basicAI2(board,agent):
    belief = generateInitialBelief(board) 

bob, tmp = startAgent()
basicAI1(tmp, bob)

