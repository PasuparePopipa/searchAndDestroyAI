import pygame, sys
import searchdestroyai
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (102, 0, 102)
YELLOW = (255,255,0)
CYAN = (0,255,255)
BLUE = (0, 0, 255)

pygame.init()

font = pygame.font.SysFont("Arial",30)
font2 = pygame.font.SysFont("Arial",20)
FPS = 30
fpsClock = pygame.time.Clock()

# This sets the margin between each cell
MARGIN = 5
scale = (720,480)
screen = pygame.display.set_mode(scale,RESIZABLE)
pygame.display.set_caption('Search And Destroy!')


#Set dimensions for the board and create board 
dimen = 5

WIDTH = int((480-(dimen*MARGIN))/dimen)
HEIGHT = int((480-(dimen*MARGIN))/dimen)

tmpboard = searchdestroyai.generateBoard(dimen)



def gamestart():
    #Initialize Stuff
    text0 = font.render("Search and Destroy!",1,RED)
    #text1 = font2.render("Target:",1,BLACK)
    text2 = font2.render("Start the AI",1,BLACK)
    text3 = font2.render("Basic AI 1",1,BLACK)
    text4 = font2.render("Basic AI 2",1,BLACK)
    text5 = font2.render("Da Ai",1,BLACK)


    agentAsset = pygame.image.load('assets/agent.png').convert_alpha()
    agentAsset = pygame.transform.scale(agentAsset, (WIDTH, HEIGHT))

    aiStart = False
    result = False

    
    

    #Event Starto
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            #If you want to play without the AI, minesweeper works from clicking!
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #activateCell(tmpboard,dimen,mouse)
                #STart AI
                if 525 <= mouse[0] <= 525+140 and 120 <= mouse[1] <= 120+40:
                    bob, tmp = searchdestroyai.startAgent(tmpboard)
                    aiStart = True
                    print('clicked')
                #Run Basic AI
                if 525 <= mouse[0] <= 525+140 and 170 <= mouse[1] <= 170+40:
                    result = searchdestroyai.basicAI1(tmpboard,bob)
                    print(result)
                    print('clicked')
                if 525 <= mouse[0] <= 525+140 and 220 <= mouse[1] <= 220+40:
                    result = searchdestroyai.basicAI2(tmpboard,bob)
                    print(result)
                    print('clicked')
                if 525 <= mouse[0] <= 525+140 and 270 <= mouse[1] <= 270+40:
                    #minesweepai.improvedAIGlobal(tmpboard,90)
                    minesweepai.improvedAIBetter(tmpboard)
                    flagMine, rip = checkWin(tmpboard,dimen)
                    print('clicked')

        screen.fill(BLACK)
        #Generate the board on UI based on board generated
        genBoard(tmpboard,dimen)

        #Blit the Agent
        if aiStart == True:
            #print(bob.x)
            screen.blit(agentAsset,[(MARGIN + WIDTH) * bob.x + MARGIN,(MARGIN + HEIGHT) * bob.y + MARGIN,WIDTH,HEIGHT])

        if result == False:
            text1 = font2.render("Target:Not Found",1,RED)
        elif result == True:
            text1 = font2.render("Target:Found!",1,RED)
        #Draw Buttons
        pygame.draw.rect(screen,(170,170,170),[525,70,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,120,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,170,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,220,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,270,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,320,140,40])
        pygame.draw.rect(screen,(170,170,170),[525,370,140,40])
        #Add title
        screen.blit(text0,(495,5))
        #Add label to the buttons
        screen.blit(text1, (530,80))
        screen.blit(text2, (530,130))
        screen.blit(text3, (530,180))
        screen.blit(text4, (530,230))
        screen.blit(text5, (530,280))
        #screen.blit(text6, (530,330))




        #Leaving if for coordinates of possible future buttons
        '''
        #Add text to Buttons
        screen.blit(text1, (530,80))
        screen.blit(text2, (530,130))
        screen.blit(text3, (530,180))
        screen.blit(text4, (530,230))
        screen.blit(text5, (530,280))
        screen.blit(text6, (530,330))
        screen.blit(text35, (530,380))
        '''


        #update screen
        pygame.display.update()
        fpsClock.tick(10)



#Generate the initial maze based on board generated
#Draws everything onto Pygames
def genBoard(board,x):
    #print(x)
    WIDTH = int((480-(x*MARGIN))/x)
    HEIGHT = int((480-(x*MARGIN))/x)
    #Get all the assets

    caveCell = pygame.image.load('assets/cave.jpg').convert_alpha()
    caveCell = pygame.transform.scale(caveCell, (WIDTH, HEIGHT))
    forestCell = pygame.image.load('assets/forest.png').convert_alpha()
    forestCell = pygame.transform.scale(forestCell, (WIDTH, HEIGHT))
    flatCell = pygame.image.load('assets/flat.jpg').convert_alpha()
    flatCell = pygame.transform.scale(flatCell, (WIDTH, HEIGHT))
    hillCell = pygame.image.load('assets/hill.jpg').convert_alpha()
    hillCell = pygame.transform.scale(hillCell, (WIDTH, HEIGHT))

    #Blitz the assets based on the state of the Cell
    for row in range(x):
        for column in range(x):
            cell = None
            if board[row][column].state == 'flat':
                cell = flatCell
            if board[row][column].state == 'hill':
                cell = hillCell
            if board[row][column].state == 'forest':
                cell = forestCell
            if board[row][column].state == 'cave':
                cell = caveCell

            screen.blit(cell,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])








#Game Starto
gamestart()
