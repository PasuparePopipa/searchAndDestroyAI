import random
import math
import numpy as np
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
        self.man = 0
        

#Our agent, x and y tell us the agent's current position
#believe is our 2D array of probabilities
class Agent:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.belief = z
        self.flag = 0

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
                print("target is: (" + str(x) + ", " + str(y) + ")")
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

#The Agent Kai, 
#2 Things seperate improved agent from the Basics
#One is a simulated annealing like approach that lets the Agent make "mistakes", to alleviate the weakness of basic AI2
#Additional Heuristic, If at a good Cell, Search
def improvedAgent(board,agent):
    #Simulated Annealing Rate
    simAnn = 15
    rand = random.randint(0,100)
    if rand > simAnn:
        #Basic Agent 2 Rules
        targetx, targety = getCoordF(board,agent)
    elif rand <= simAnn:
        #Basic Agent 1 Rules
        targetx, targety = getCoordH(board,agent)
    
    #Travel towards target and search
    #If rate of finding cell is good, search the cell
    distance, searches , boole = improvedtravel(board,agent,targetx,targety)
    
    #If target found prematurely from heuristic, yay
    if boole == True:
        return True, distance, searches
    #search the Cell
    searches = searches + 1
    search = searchCell(board,targetx,targety)
    #If found, it's all over
    if search == True:
        #print('over')
        #print(searches)
        return True, distance, searches
    #If not found, update the network and return false
    elif search == False:
        #Update network
        #print('test')
        updateNetwork(agent,board,targetx,targety)
        #printBelief(agent.belief)
        return False, distance, searches


#agent travels to the targetted cell
#If Cell hits a certain heuristic, search
def improvedtravel(board,agent,targetx,targety):
    searches = 0
    #Set the heuristic for searching for Cells along the way
    heuris = improvedHeuristic(board,agent)
    distance = 0
    #Traveling to target
    while agent.x != targetx or agent.y != targety:
        if agent.x < targetx:
            agent.x = agent.x + 1
            distance = distance+1
            #If Chances of finding the cell is greater than heuristic, Search the cell
            if agent.belief[agent.x][agent.y] * (1-getRates(board[agent.x][agent.y].state)) > heuris:
                searches = searches + 1
                search = searchCell(board,agent.x,agent.y)
                if search == True:
                    return distance, searches, True
                elif search == False:
                    updateNetwork(agent,board,targetx,targety)
                    #printBelief(agent.belief)
        elif agent.x > targetx:
            agent.x = agent.x - 1
            distance = distance+1
            #If Chances of finding the cell is greater than heuristic, Search the cell
            if agent.belief[agent.x][agent.y] * (1-getRates(board[agent.x][agent.y].state)) > heuris:
                searches = searches + 1
                search = searchCell(board,agent.x,agent.y)
                if search == True:
                    return distance, searches, True
                elif search == False:
                    updateNetwork(agent,board,targetx,targety)
                    #printBelief(agent.belief)
        #If Chances of finding the cell is greater than heuristic, Search the cell
        elif agent.y > targety:
            agent.y = agent.y - 1
            distance = distance+1
            #If Chances of finding the cell is greater than heuristic, Search the cell
            if agent.belief[agent.x][agent.y] * (1-getRates(board[agent.x][agent.y].state)) > heuris:
                searches = searches + 1
                search = searchCell(board,agent.x,agent.y)
                if search == True:
                    return distance, searches, True
                elif search == False:
                    updateNetwork(agent,board,targetx,targety)
                    #printBelief(agent.belief)
        elif agent.y < targety:
            agent.y = agent.y + 1
            distance = distance+1
            #If Chances of finding the cell is greater than heuristic, Search the cell
            if agent.belief[agent.x][agent.y] * (1-getRates(board[agent.x][agent.y].state)) > heuris:
                searches = searches + 1
                search = searchCell(board,agent.x,agent.y)
                if search == True:
                    return distance, searches, True
                elif search == False:
                    updateNetwork(agent,board,targetx,targety)
                    #printBelief(agent.belief)
    return distance, searches, False

#The Agent Kai, 
#2 Things seperate improved agent from the Basics while accounting for a moving topic
#One is a simulated annealing like approach that lets the Agent make "mistakes", to alleviate the weakness of basic AI2
#Additional Heuristic, If at a good Cell, Search
def improvedAgentmov(board,agent):

    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y

    print("coords are: (" + str(tx) + ", " + str(ty) + ")")
    #switch to tracking in manhatan distance search
    if agent.flag == 0:            
        #Simulated Annealing Rate
        simAnn = 15
        rand = random.randint(0,100)
        if rand > simAnn:
            #Basic Agent 2 Rules
            targetx, targety = getCoordF(board,agent)
        elif rand <= simAnn:
            #Basic Agent 1 Rules
            targetx, targety = getCoordH(board,agent)
    
        #Travel towards target and search
        #If rate of finding cell is good, search the cell
        distance, searches , boole = improvedtravel(board,agent,targetx,targety)
        print(coorManDistCalc(tx, ty, agent))
        if coorManDistCalc(tx, ty, agent) <= 5:

            agent.flag = 1
            print("i got you in my sights")
    else:
        #Simulated Annealing Rate
        simAnn = 15
        rand = random.randint(0,100)
        if rand > simAnn:
            #Basic Agent 2 Rules
            targetx, targety = getCoordFAlt(board,agent)
        elif rand <= simAnn:
            #Basic Agent 1 Rules
            targetx, targety = getCoordHAlt(board,agent)
    
        #Travel towards target and search
        #If rate of finding cell is good, search the cell
        distance, searches , boole = improvedtravel(board,agent,targetx,targety)


    #If target found prematurely from heuristic, yay
    if boole == True:
        return True, distance, searches
    #search the Cell
    searches = searches + 1
    search = searchCell(board,targetx,targety)
    #If found, it's all over
    if search == True:
        #print('over')
        #print(searches)
        return True, distance, searches
    #If not found, update the network and return false
    elif search == False:
        #Update network
        #print('test')
        updateNetwork(agent,board,targetx,targety)
        board = newTarget(board)
        #printBelief(agent.belief)
        return False, distance, searches
  
#Set Heuristic for searching for a Cell along the way
#Heurisitc is currently set to be higher than the 95th percentile
def improvedHeuristic(board,agent):
    tmpList = []
    #print('test')
    for row in board:
        for cell in row:
            tmpList.append(agent.belief[cell.x][cell.y] * (1-getRates(cell.state)))
    percen = np.percentile(tmpList,95)
    return percen
    

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


    #Getts the coordinates of a cell with the highest probability of finding a target
#Used for Basic Agent 2 while withing manhatan distance of 5 from target
def getCoordFAlt(board,agent):
    greatestProb = 0
    counter = 0
    targetx = None
    targety = None
    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y
    #Find the greatest current probabiity, and number of Cells that have that probabiliy
    for row in board:
        for cell in row:
            if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
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
                if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
                    if agent.belief[cell.x][cell.y]  * (1-getRates(cell.state)) == greatestProb:
                        if abs(cell.x - agent.x) + abs(cell.y-agent.y) < shortDist:
                            shortDist = abs(cell.x - agent.x) + abs(cell.y-agent.y) 
        for row in board:
            for cell in row:
                if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
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

#Get Data for Basic Agent 1
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

#Get Data for Basic Agent 1
def getDatam(x):
    for i in range(x):
        searches = 0
        totalDistance = 0
        tmp = generateBoard(50)
        bob, tmp = startAgent(tmp)
        res = False
        while res == False:
            res, dist = movBasicAI(tmp,bob)
            totalDistance = totalDistance + dist
            searches = searches + 1
        print(totalDistance)
        print(searches)

#Get Data for Basic Agent 2
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
#Get Data for Improved Agent
def getData3(x):
    for i in range(x):
        totalDistance = 0
        totalSearches = 0
        tmp = generateBoard(50)
        bob, tmp = startAgent(tmp)
        res = False
        while res == False:
            res, dist , searches = improvedAgentmov(tmp,bob)
            totalDistance = totalDistance + dist
            totalSearches = totalSearches + searches
        print(totalDistance)
        print(totalSearches)
        print('sep')

def genManBoard(board):
    mBoard = []
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                mBoard[x][y].state = 2
            else:
                mBoard[x][y].state = 0
    return mBoard
            
def updateManBoard(mBoard, cur):
    mBoard = []
    d = len()
    for x in range(d):
        for y in range(d):
            if mBoard[x][y].state < 2 and manDistCalc(mBoard[x][y], cur) <= 5:
                 mBoard[x][y].state = 1
                 return mBoard

def manDistCalc(c, cur):
    return abs(c.x - cur.x) + abs(c.y - cur.y)

def coorManDistCalc(x, y, cur):
    return abs(x - cur.x) + abs(y - cur.y)

def bothCoorManDistCalc(x, y, bx, by):
    return abs(x - bx) + abs(y - by)

#Gets the Coordinates of a Cell with highest Probability of containing target within manhatan distance
#If tie, random among
#Used for Basic Agent 1
# stays withing manhatan distance of 5 from target
def getCoordHAlt(board,agent):
    greatestProb = 0
    counter = 0
    targetx = None
    targety = None
    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y
    #Find the greatest current probabiity, and number of Cells that have that probabiliy
    for row in board:
        for cell in row:
            if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
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
                if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
                    if agent.belief[cell.x][cell.y] == greatestProb:
                        if abs(cell.x - agent.x) + abs(cell.y-agent.y) < shortDist:
                            shortDist = abs(cell.x - agent.x) + abs(cell.y-agent.y) 
        for row in board:
            for cell in row:
                if bothCoorManDistCalc(cell.x, cell.y, tx, ty) <= 5:
                    if agent.belief[cell.x][cell.y] == greatestProb and abs(cell.x - agent.x) + abs(cell.y-agent.y) == shortDist:
                        targetx = cell.x
                        targety = cell.y
                        return targetx,targety
    print('reached')
    

#Iteratively travel to the cell with the highest probability of containing the target, search
#that cell while within manhatan distance of 5. Repeat until target is found.
def movBasicAI1(board,agent):
    
    #Travel to Cell with Highest probability of containing target, keep track of distance
    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y

    print("coords are: (" + str(tx) + ", " + str(ty) + ")")
    if agent.flag == 0:
        targetx, targety = getCoordH(board,agent)
        distance = travel(board,agent,targetx,targety)
        print(coorManDistCalc(tx, ty, agent))
        if coorManDistCalc(tx, ty, agent) <= 5:

            agent.flag = 1
            print("i got you in my sights")
    else:
        print(coorManDistCalc(tx, ty, agent))
        targetx, targety = getCoordHAlt(board,agent)
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
        board = newTarget(board)
        #printBelief(agent.belief)
        return False, distance

#Iteratively travel to the cell with the highest probability of containing the target, search
#that cell while within manhatan distance of 5. Repeat until target is found.
def movBasicAI2(board,agent):
    
    #Travel to Cell with Highest probability of containing target, keep track of distance
    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y

    print("coords are: (" + str(tx) + ", " + str(ty) + ")")
    if agent.flag == 0:
        targetx, targety = getCoordF(board,agent)
        distance = travel(board,agent,targetx,targety)
        print(coorManDistCalc(tx, ty, agent))
        if coorManDistCalc(tx, ty, agent) <= 5:

            agent.flag = 1
            print("i got you in my sights")
    else:
        print(coorManDistCalc(tx, ty, agent))
        targetx, targety = getCoordFAlt(board,agent)
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
        board = newTarget(board)
        #printBelief(agent.belief)
        return False, distance


#finds a new home for target within adjacent spaces
def newTarget(board):
    d = len(board)
    for x in range(d):
        for y in range(d):
            if board[x][y].target == True:
                tx = x
                ty = y
    br = len(board) - 1
    if tx == 0 and ty == 0:
        rand = random.randint(1,2)
        if rand == 1:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
            print()
        elif rand == 2:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif tx == br and ty == 0:
        rand = random.randint(1,2)
        if rand == 1:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif tx == 0 and ty == br:
        rand = random.randint(1,2)
        if rand == 1:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif tx == br and ty == br:
        rand = random.randint(1,2)
        if rand == 1:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif ty == 0:
        rand = random.randint(1,3)
        if rand == 1:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 3:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif ty == br:
        rand = random.randint(1,3)
        if rand == 1:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 3:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif tx == 0:
        rand = random.randint(1,3)
        if rand == 1:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 3:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    elif tx == br:
        rand = random.randint(1,3)
        if rand == 1:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 3:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    else:
        rand = random.randint(1,4)
        if rand == 1:
            board[tx - 1][ty].target = True
            board[tx - 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 2:
            board[tx + 1][ty].target = True
            board[tx + 1][ty].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 3:
            board[tx][ty + 1].target = True
            board[tx][ty + 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
        elif rand == 4:
            board[tx][ty - 1].target = True
            board[tx][ty - 1].man = 2
            board[tx][ty].target = False
            board[tx][ty].man = 1
    return board
    
#getData3(10)
#print('sep')
#getData2(1)
#getData3(5)



'''

tmp = generateBoard(5)
bob, tmp2 = startAgent(tmp)
printBelief(bob.belief)


updateNetwork(bob,tmp,1,1)
printBelief(bob.belief)
'''