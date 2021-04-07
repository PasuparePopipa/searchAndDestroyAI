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

#Gets the rate of failure given a current state
def getRates(state):
    if state == 'flat':
        return 0.1
    elif state == 'hill':
        return 0.3
    elif state == 'forest':
        return 0.7
    elif state == 'cave':
        return 0.9

#Print out current board based on state
def printBoard(board):
    for row in board:
        for cell in row:
            print(cell.target)
#Print out current board of beliefs
def printBelief(board):
    for row in board:
        for cell in row:
            print(cell)

#Starts up the AI, Partially for UI Purposes
def startAgent(tmp):
    #tmp = generateBoard(20)
    belief = generateInitialBelief(tmp) 
    startLocationX = random.randint(0,len(tmp)-1)
    startLocationY = random.randint(0,len(tmp)-1)
    bob = Agent(startLocationX,startLocationY,belief)
    return bob, tmp

#Iteratively travel to the cell with the highest probability of containing the target, search
#that cell. Repeat until target is found.
def basicAI1(board,agent):
    #Travel to Cell with Highest probability of containing target, keep track of distance
    targetx, targety = getCoordH(board,agent)
    distance = travel(board,agent,targetx,targety)
    #search the Cell
    search = searchCell(board,targetx,targety)
    #If found, it's all over
    if search == True:
        #print('over')
        return True, distance
    #If not found, update the network and return false
    elif search == False:
        #Update network
        #print('test')
        updateNetwork(agent,board,targetx,targety)
        #printBelief(agent.belief)
        return False, distance

#Iteratively travel to the cell with the highest probability of finding the target within that
#cell, search that cell. Repeat until the target is found.
#So Basic AI1 rate * the rate of finding it
def basicAI2(board,agent):
    #Travel to Cell with Highest probability of containing target, keep track of distance
    targetx, targety = getCoordF(board,agent)
    distance = travel(board,agent,targetx,targety)
    #search the Cell
    search = searchCell(board,targetx,targety)
    #If found, it's all over
    if search == True:
        #print('over')
        return True, distance
    #If not found, update the network and return false
    elif search == False:
        #Update network
        #print('test')
        updateNetwork(agent,board,targetx,targety)
        #printBelief(agent.belief)
        return False, distance


#Updates the Network of the agent,
#Change the beliefs based on the last false
def updateNetwork(agent,board,targetx,targety):
    d = len(agent.belief)
    agent2 = deepcopy(agent)
    for i in range(d):
        for j in range(d):
            #Prob(target in Cell given obs + fail)
            #P(A) = In Current Cell
            #P(B) = Failed in Specific Cell
            #Bayes P(A|B) = P(A)P(B|A)/P(B)
            # 
            #P(B) = P(A)P(B/A) + P(notA)P(B/notA)


            #Bayes Therom, A is target is in current Cell, B is failure in searched Cell?
            #Bayes P(A|B) = P(A)P(B|A)/P(B)
            #P(B) = P(A)P(B/A) + P(notA)P(B/notA)
            #P(B) = 
            #(1-getRates(board[targetx][targety])) 
            if i == targetx and j == targety: #If we are in the Cell that we searched
                #P(B) changes to failure in this Cell
                pb = agent2.belief[i][j] * (getRates(board[targetx][targety].state)) + (1-agent2.belief[i][j]) * 1
                newBelief = agent2.belief[i][j] * getRates(board[targetx][targety].state)  / pb
                agent.belief[i][j] = newBelief
            else: #Belief State of other cells
                pb = agent2.belief[i][j] * (getRates(board[targetx][targety].state)) + (1-agent2.belief[i][j]) * 1
                newBelief = agent2.belief[i][j] * 1 / pb
                #print(agent.belief[i][j])

                agent.belief[i][j] = newBelief
            #print('update')


#Gets the Coordinates of a Cell with highest Probability of containing target
#If tie, random among
#Used for Basic Agent 1
def getCoordH(board,agent):
    greatestProb = 0
    counter = 0
    targetx = None
    targety = None
    #Find the greatest current probabiity, and number of Cells that have that probabiliy
    for row in board:
        for cell in row:
            if agent.belief[cell.x][cell.y] > greatestProb:
                greatestProb = agent.belief[cell.x][cell.y]
                counter = 1
                targetx = cell.x
                targety = cell.y
            elif agent.belief[cell.x][cell.y] == greatestProb:
                counter = counter + 1
    #If Counter is one, return the coordinates, otherwise, coordinates with shortest distance
    if counter == 1:
        return targetx, targety
    else:
        shortDist = 999999
        counter = 0
        for row in board:
            for cell in row:
                if agent.belief[cell.x][cell.y] == greatestProb:
                    if abs(cell.x - agent.x) + abs(cell.y-agent.y) < shortDist:
                        shortDist = abs(cell.x - agent.x) + abs(cell.y-agent.y) 
        for row in board:
            for cell in row:
                if agent.belief[cell.x][cell.y] == greatestProb and abs(cell.x - agent.x) + abs(cell.y-agent.y) == shortDist:
                    targetx = cell.x
                    targety = cell.y
                    return targetx,targety
    print('reached')


#Getts the coordinates of a cell with the highest probability of finding a target
#Used for Basic Agent 2
def getCoordF(board,agent):
    greatestProb = 0
    counter = 0
    targetx = None
    targety = None
    #Find the greatest current probabiity, and number of Cells that have that probabiliy
    for row in board:
        for cell in row:
            if agent.belief[cell.x][cell.y] * (1-getRates(cell.state)) > greatestProb:
                greatestProb = agent.belief[cell.x][cell.y]
                counter = 1
                targetx = cell.x
                targety = cell.y
            elif agent.belief[cell.x][cell.y] * (1-getRates(cell.state))== greatestProb:
                counter = counter + 1
    #If Counter is one, return the coordinates, otherwise, return a coordinate with shortest distance
    if counter == 1:
        return targetx, targety
    else:
        shortDist = 999999
        counter = 0
        for row in board:
            for cell in row:
                if agent.belief[cell.x][cell.y]  * (1-getRates(cell.state)) == greatestProb:
                    if abs(cell.x - agent.x) + abs(cell.y-agent.y) < shortDist:
                        shortDist = abs(cell.x - agent.x) + abs(cell.y-agent.y) 
        for row in board:
            for cell in row:
                if agent.belief[cell.x][cell.y]  * (1-getRates(cell.state)) == greatestProb and abs(cell.x - agent.x) + abs(cell.y-agent.y) == shortDist:
                    targetx = cell.x
                    targety = cell.y
                    return targetx,targety
    print('reached')

#Searches the Cell based on a given x and y coordinate, 
#Return true if found, false if not found
def searchCell(board,targetx,targety):
    if board[targetx][targety].target == False:
        return False
    elif board[targetx][targety].target == True:
        rand = random.randint(1,100)
        if board[targetx][targety].state == 'flat':
            if rand < 10:
                return False
        elif board[targetx][targety].state == 'hill':
            if rand < 30:
                return False
        elif board[targetx][targety].state == 'forest':
            if rand < 70:
                return False
        elif board[targetx][targety].state == 'cave':
            if rand < 90:
                return False
        return True

#agent travels to the targetted cell
def travel(board,agent,targetx,targety):
    distance = 0
    while agent.x != targetx or agent.y != targety:
        if agent.x < targetx:
            agent.x = agent.x + 1
            distance = distance+1
        elif agent.x > targetx:
            agent.x = agent.x - 1
            distance = distance+1
        elif agent.y > targety:
            agent.y = agent.y - 1
            distance = distance+1
        elif agent.y < targety:
            agent.y = agent.y + 1
            distance = distance+1
    return distance
    print('over')
    
def getData(x):
    for i in range(x):
        searches = 0
        totalDistance = 0
        tmp = generateBoard(50)
        bob, tmp = startAgent(tmp)
        res = False
        while res == False:
            res, dist = basicAI1(tmp,bob)
            totalDistance = totalDistance + dist
            searches = searches + 1
        print(totalDistance)
        print(searches)


def getData2(x):
    for i in range(x):
        searches = 0
        totalDistance = 0
        tmp = generateBoard(50)
        bob, tmp = startAgent(tmp)
        res = False
        while res == False:
            res, dist = basicAI2(tmp,bob)
            totalDistance = totalDistance + dist
            searches = searches + 1
        print(totalDistance)
        print(searches)




getData(1)
print('sep')
getData2(1)



'''

tmp = generateBoard(5)
bob, tmp2 = startAgent(tmp)
printBelief(bob.belief)


updateNetwork(bob,tmp,1,1)
printBelief(bob.belief)
'''