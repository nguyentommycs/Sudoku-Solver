import math
import pygame
pygame.font.init()

#constants to change look of the board
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
LINE_THICKNESS = 10
FONT_SIZE=50
font = pygame.font.SysFont('arial', FONT_SIZE)
showSteps= True
grid = [[0,2,0,0,0,4,3,0,0],
        [9,0,0,0,2,0,0,0,8],
        [0,0,0,6,0,9,0,5,0],
        [0,0,0,0,0,0,0,0,1],
        [0,7,2,5,0,3,6,8,0],
        [6,0,0,0,0,0,0,0,0],
        [0,8,0,2,0,5,0,0,0],
        [1,0,0,0,9,0,0,0,3],
        [0,0,9,8,0,0,0,6,0]]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku Solver')
clickedPos = (0,0)

#used to update the screen during the solve animation
def updateScreen():
    screen.fill((255, 255, 255))
    for i in range(8):
        surf = pygame.Surface((LINE_THICKNESS,SCREEN_HEIGHT))
        surf.fill((0,0,0))
        screen.blit(surf,((SCREEN_WIDTH//9)*(i+1)-LINE_THICKNESS//2,0))
    for i in range(8):
        surf = pygame.Surface((SCREEN_WIDTH,LINE_THICKNESS))
        surf.fill((0,0,0))
        screen.blit(surf,(0,(SCREEN_HEIGHT//9)*(i+1)-LINE_THICKNESS//2))
    
    #fill in numbers
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num!=0:
                text = font.render(str(num),True,(0,0,0))
                screen.blit(text,(round(SCREEN_WIDTH/9*(j+0.5)-FONT_SIZE/5),round(SCREEN_HEIGHT/9*(i+0.5))-FONT_SIZE//2))

    #this code prevents windows from thinking the program is unresponsive during the solve animation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    pygame.display.flip()
#inputs the number into the grid using clickedPos
def input(num):
    x = math.floor(clickedPos[0]/SCREEN_WIDTH*9)#find which square was clicked
    y = math.floor(clickedPos[1]/SCREEN_HEIGHT*9)
    grid[y][x]=num
#solves grid. returns true if there is a solution and false if there is no solution
def solve():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==0: #find the next point that isn't filled
                possible = findPossible(grid,i,j) #generate a list of possible numbers 
                    
                if len(possible)==0: #if there are no possible numbers, backtrack
                    return False
                for k in range(len(possible)): #try all possible numbers
                    grid[i][j]=possible[k]
                    if showSteps:
                        updateScreen()

                    if solve(): #repeat process with new grid
                        return True
                    grid[i][j]=0


                return False #if none of the possible numbers work, backtrack

    return checkSolved(grid)
 
#given an empty point, return all possible numbers based on col, row, and local square
def findPossible(grid,row,col):
    nonSol = set() #numbers that cannot be solutions
    solutions=[]
    for i in range(len(grid)): 
        nonSol.add(grid[i][col])
    for i in range(len(grid[row])):
        nonSol.add(grid[row][i])

    squareCol = col//3 * 3; 
    squareRow = row//3 * 3; #represents the top left corner of the square
    for i in range(3):
        for j in range(3):
            nonSol.add(grid[squareRow+i][squareCol+j])

    for i in range(len(grid)):
        if (i+1) not in nonSol:
            solutions+=[i+1]
    return solutions

#checks if a grid is solved and returns true/false
def checkSolved(grid):
    solutionSet = {1,2,3,4,5,6,7,8,9}
    #check each row
    for i in range(len(grid)):
        tempSet = set()
        for j in range(len(grid[i])):
            tempSet.add(grid[i][j])
        if len(tempSet.difference(solutionSet))!=0:
            return False
    #check each col
    for i in range(len(grid[0])):
        tempSet = set()
        for j in range(len(grid)):
            tempSet.add(grid[j][i])
        if len(tempSet.difference(solutionSet))!=0:
            return False
    #check each quadrant
    for squareRow in range(3):
        for squareCol in range(3):
            tempSet = set()
            for i in range(3):
                for j in range(3):
                    tempSet.add(grid[squareRow+i][squareCol+i])
            if len(tempSet.difference(solutionSet))!=0:
                return False
    return True
    
#prints grid in console, debugging tool
def printGrid(grid):
    output = ''
    for i in range(9):
        for j in range(9):
            output+=str(grid[i][j])+','
        output+='\n'
    print(output)


#game loop
running = True
while running:
    clock=pygame.time.Clock()
    clock.tick(144)

    screen.fill((255, 255, 255))
   
    #highlight square that is clicked
    coordX = math.floor(clickedPos[0]/SCREEN_WIDTH*9)*(SCREEN_WIDTH/9) #find top left corner of square clicked
    coordY = math.floor(clickedPos[1]/SCREEN_HEIGHT*9)*(SCREEN_HEIGHT/9)
    surf = pygame.Surface((SCREEN_WIDTH/9,SCREEN_HEIGHT/9))
    surf.fill((153,204,255))
    screen.blit(surf,(coordX,coordY))
    #draw gridlines
    for i in range(8):
        surf = pygame.Surface((LINE_THICKNESS,SCREEN_HEIGHT))
        surf.fill((0,0,0))
        screen.blit(surf,((SCREEN_WIDTH//9)*(i+1)-LINE_THICKNESS//2,0))
    for i in range(8):
        surf = pygame.Surface((SCREEN_WIDTH,LINE_THICKNESS))
        surf.fill((0,0,0))
        screen.blit(surf,(0,(SCREEN_HEIGHT//9)*(i+1)-LINE_THICKNESS//2))
    #fill in numbers
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num!=0:
                text = font.render(str(num),True,(0,0,0))
                screen.blit(text,(round(SCREEN_WIDTH/9*(j+0.5)-FONT_SIZE/5),round(SCREEN_HEIGHT/9*(i+0.5))-FONT_SIZE//2))
    #take user input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                showSteps=True
                solve()
            if event.key == pygame.K_RETURN:
                showSteps=False
                solve()
            if event.key == pygame.K_DELETE:
                input(0)
            if event.key == pygame.K_1:
                input(1)
            if event.key == pygame.K_2:
                input(2)
            if event.key == pygame.K_3:
                input(3)
            if event.key == pygame.K_4:
                input(4)
            if event.key == pygame.K_5:
                input(5)
            if event.key == pygame.K_6:
                input(6)
            if event.key == pygame.K_7:
                input(7)
            if event.key == pygame.K_8:
                input(8)
            if event.key == pygame.K_9:
                input(9)
            if event.key == pygame.K_KP1:
                input(1)
            if event.key == pygame.K_KP2:
                input(2)
            if event.key == pygame.K_KP3:
                input(3)
            if event.key == pygame.K_KP4:
                input(4)
            if event.key == pygame.K_KP5:
                input(5)
            if event.key == pygame.K_KP6:
                input(6)
            if event.key == pygame.K_KP7:
                input(7)
            if event.key == pygame.K_KP8:
                input(8)
            if event.key == pygame.K_KP9:
                input(9)
        elif event.type == pygame.MOUSEBUTTONDOWN:
             clickedPos = pygame.mouse.get_pos()
        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    pygame.display.flip()

    