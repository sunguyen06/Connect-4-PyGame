#Su Nguyen 751111   
#12/07/22
#ICS3U0-B
#This is a Connect 4 game in Python using PyGame

# Importing necessary modules
import pygame
import numpy as np
import random
import time
pygame.init()
pygame.mixer.init()

# Declaring constants/variables
ROWS, COLUMNS = 6, 7
WIDTH, HEIGHT = 860, 840
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (25, 25, 26)
BLUE = (0, 122, 204)
DARK_BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (254, 216, 177)
PIECE_SIZE = 100
pieceX = [70, 190, 310, 430, 550, 670, 790]
pieceY = [170, 290, 410, 530, 650, 770]
boardImage = pygame.image.load(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\Board.png")
instImage = pygame.image.load(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\Instructions.png")
blurImage = pygame.transform.scale(pygame.image.load(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\Blur.png"), (2500, 1625))
buttonSound = pygame.mixer.Sound(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\ButtonSound.wav")
buttonSound.set_volume(0.2)
pieceSound = pygame.mixer.Sound(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\pieceSound.wav")
errorSound = pygame.mixer.Sound(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\Invalid.wav")
font = pygame.font.Font(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\telegraphem.otf",  120)
font2 = pygame.font.Font(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\telegraphem.otf",  100)


# setting up pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# setting up bgm
#pygame.mixer.music.load(r"C:\Users\nguye\Old Projects\Connect-4-PyGame-main\connect4bgm.wav")
#pygame.mixer.music.set_volume(0.2)
#pygame.mixer.music.play()

# function resets/creates virtual board in console
def createBoard():
    resetBoard = np.zeros((ROWS,COLUMNS)) # uses numpy to create a 2d array filled of zeros with dimensions 6x7
    print(resetBoard)
    return resetBoard # returns the array as the value of the function

# animation function for the pieces
def animation(condition, colour, column, board):
    objectY = 50 # placeholder variable for the object's y coordinate
    skip = False # boolean variable for when they skip 
    
    while objectY < condition and skip == False:
        objectY += 10 # object will move 10 pixels every iteration of the loop causing a smooth fall
        pygame.draw.circle(screen, GRAY, (column, objectY-10), 50) # this is to cover up the objects previous iteration so the animation looks more smooth
        pygame.draw.circle(screen, colour, (column, objectY), 50) # this is the piece that is falling
        drawBoard(False, board) # constantly redrawing the board to not lose the layer consistency 
        for event in pygame.event.get(): # get list of events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if the event was another mouse click, skip the entire animation.
                pygame.draw.circle(screen, GRAY, (column, objectY), 50) # cleans up after skipping the animation
                drawBoard(False, board)
                skip = True # breaks the loop

    pieceSound.play()
    # this if statement is to tell whose turn it is and after the animation finishes, it will draw a circle for the next player's turn at the top.
    posX = pygame.mouse.get_pos()[0] # takes only the x-coordinate of the mouse
    if colour == RED: drawPiece(2, pieceX[checkCol(posX, pieceX)])
    else: drawPiece(1, pieceX[checkCol(posX, pieceX)])
    pygame.draw.circle(screen, colour, (column, condition), 50) # draws the piece that was played after the animation was skipped
    pygame.display.flip() # updates everything that has happened.

    
# function updates the board state according to the player and their move
def dropPiece(col, player, board):
    if board[0][col] == 0: # checks if the column is open
        for i in range(ROWS, 0, -1): # checks every row starting from bottom to top
            if board[i-1][col] == 0: # checks for open slots in that column
                board[i-1][col] = player # replaces the first open slot in that column as the player numbers' piece
                if player == 1: animation(pieceY[i-1], RED, pieceX[col], board, ) # player 1
                elif player == 2: animation(pieceY[i-1], YELLOW, pieceX[col], board, ) # player 2
                break
    else: # if the column is not full tell the user the move is invalid
        errorSound.set_volume(0.2)
        errorSound.play() # play a sound to indicate to the user the move is invalid
        return None # return None to allow conditional loop to replay the move

    print(board) # prints current board state

    win = checkWin(player, board) # boolean variable to check for wins
    if win == True: # if checkWin is true, return dropPiece as true
        time.sleep(1) # delay the screen from instantly changing to win screen
        return loadWin(player)
    else: # otherwise, dropPiece will be false
        return False

# Function that scans through the current board state and checks if any player has won
def checkWin(player, board): 
    for i in range(ROWS): # This for loop checks for horizontal wins
        for j in range(COLUMNS - 3):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True

    for i in range(ROWS - 3): # This for loop checks for vertical wins
        for j in range(COLUMNS):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True

    for i in range(3, ROWS): # This for loop checks for positive diagonal wins
        for j in range(COLUMNS - 3):
            if board[i][j] == player and board[i-1][j+1] == player and board[i-2][j+2] == player and board[i-3][j+3] == player:
                return True

    for i in range(3, ROWS): # This for loop checks for negative diagonal wins
        for j in range(3, COLUMNS):
            if board[i][j] == player and board[i-1][j-1] == player and board[i-2][j-2] == player and board[i-3][j-3] == player:
                return True

# Function that draws the board onto the screen using the board.png image
def drawBoard(paused, board):
    screen.blit(boardImage, (0, 0))
    if paused == True:
        for i in range(0, ROWS):
            for j in range(0, COLUMNS):
                if board[i][j] == 1:
                    pygame.draw.circle(screen, RED, (pieceX[j], pieceY[i]), 50)
                elif board[i][j] == 2:
                    pygame.draw.circle(screen, YELLOW, (pieceX[j], pieceY[i]), 50)
    pygame.display.flip()

# Function that draws the piece at the top of the screen which indicates what play the user is making.
def drawPiece(player, pos):
    if player == 1: # player 1's piece
        pygame.draw.circle(screen, RED, (pos, 50), 50)
    else: # player 2's piece
        pygame.draw.circle(screen, YELLOW, (pos, 50), 50)

# this check's each column for multiple purposes, 1: it will lock each piece in place making it so that a piece will never be outside of its necessary x position,
# 2: it tells us which column the piece is currently on respective to the mouse's position.
def checkCol(pos, restrictions):
    if pos > 0 and pos <= restrictions[0] + 70: return 0
    elif pos > restrictions[0] + 70 and pos <= restrictions[1] + 70: return 1
    elif pos > restrictions[1] + 70 and pos <= restrictions[2] + 70: return 2
    elif pos > restrictions[2] + 70 and pos <= restrictions[3] + 70: return 3
    elif pos > restrictions[3] + 70 and pos <= restrictions[4] + 70: return 4
    elif pos > restrictions[4] + 70 and pos <= restrictions[5] + 70: return 5
    elif (pos > restrictions[5] + 70 and pos <= restrictions[6] + 70) or (pos > restrictions[6] + 70): return 6
    else: return 0

# Function to center text creation
def centerText(text, colour, y):
    temp = font.render(text, True, colour)
    size = temp.get_width()
    screen.blit(temp, (((WIDTH - size)/2), y))
    pygame.display.flip()

# Function that changes the screen to a pause screen.
def pauseGame(player, board):
    # Creates the screen and the visuals
    screen.blit(blurImage, (0,0))
    centerText("PAUSED", BLACK, 0)
    centerText("RESUME", DARK_BLUE, 250)
    centerText("RESTART", YELLOW, 400)
    centerText("QUIT", RED, 550)

    paused = True # bool var for loop
    while paused:
        pygame.init() # initializing pygame in this loop to avoid error
        for event in pygame.event.get(): # getting list of events
            if event.type == pygame.QUIT: # if user quits from program, the program will quit
                paused = False
                return True

            if event.type == pygame.KEYDOWN: # if the user inputs esc key, the game will unpause and will reset the board back to normal.
                if event.key == pygame.K_ESCAPE:
                    buttonSound.play()
                    screen.fill(GRAY)
                    drawBoard(True, board)
                    posX = pygame.mouse.get_pos()[0] # takes only the x-coordinate of the mouse
                    if player == 1: drawPiece(1, pieceX[checkCol(posX, pieceX)])
                    else: drawPiece(2, pieceX[checkCol(posX, pieceX)])
                    paused = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # for mouse1 clicks. (left clicks)
                posX, posY = pygame.mouse.get_pos() # getting x and y coordinates of the mouse upon clicking.
                print(posX, posY)
                if (posX >= (WIDTH-420)/2 and posX <= (WIDTH-420)/2 + 420) and (posY >= 250 and posY <= 370): # Condition for clicking on Resume Text
                    buttonSound.play()
                    screen.fill(GRAY)
                    drawBoard(True, board)
                    if player == 1: drawPiece(1, pieceX[checkCol(posX, pieceX)])
                    else: drawPiece(2, pieceX[checkCol(posX, pieceX)])
                    paused = False

                elif (posX >= (WIDTH-488)/2 and posX <= (WIDTH-488)/2 + 488) and (posY >= 400 and posY <= 520): # Condition for clickling on Restart Text
                    buttonSound.play()
                    paused = False
                    return False
                    
                
                elif(posX >= (WIDTH-279)/2 and posX <= (WIDTH-279)/2 + 279) and (posY >= 550 and posY <= 770): # Condition for clicking on Quit Text
                    buttonSound.play()
                    return True

# Function to load all objects on the main menu screen
def loadMenu():
    pygame.init()
    screen.fill(DARK_BLUE)
    centerText("CONNECT 4", WHITE, 20)
    centerText("PLAY", YELLOW, 180)
    centerText("INSTRUCTIONS", ORANGE, 330)
    centerText("EXIT", RED, 480)
    pygame.display.flip()

# Function that transitions to the instruction screen
def showInstructions():
    # Visuals for the instruction screen
    screen.blit(instImage, (0,0))
    pygame.display.flip()
    instructions = True
    while instructions: # condition to keep it running and not interfere with other screens
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # allow the user to quit the program whenever necessary
                instructions = False
                return False
            
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # escape will bring you back to the main menu screen
                buttonSound.play()
                loadMenu()
                instructions = False
                return True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left clicking on the back button will bring you back to the main menu screen
                posX, posY = pygame.mouse.get_pos()
                if (posX >= 0 and posX <= 80) and (posY >= 0 and posY <= 80):
                    buttonSound.play()
                    loadMenu()
                    instructions = False
                    return True

# Function for the screen upon winning the game.
def loadWin(player):
    screen.blit(blurImage, (0,0))
    if player == 3: # draw condition
        winText = "It was a draw!"
    else:
        if player == 1:
            winText = "Red Wins!"
        else:
            winText = "Yellow Wins!"
    temp = font2.render(winText, True, BLACK)
    size = temp.get_width()
    screen.blit(temp, (((WIDTH - size)/2), 20))
    centerText("PLAY AGAIN?", YELLOW, 300) # play again button, resets board
    centerText("QUIT", RED, 450) # quit button, brings user back to main menu screen
    pygame.display.flip()
    winScreen = True

    while winScreen: # condition to keep it running and not interfere with other screens
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                winScreen = False
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                posX, posY = pygame.mouse.get_pos()
                if(posX >= (WIDTH - 774)/2 and posX <= (WIDTH - 774)/2 + 774) and (posY >= 300 and posY <= 420): # Clicking on Play again? text
                    buttonSound.play()
                    winScreen = False
                    return "restart"
                elif(posX >= (WIDTH - 279)/2 and posX <= (WIDTH - 279)/2 + 279) and (posY >= 450 and posY <= 570): # Clicking on Quit text
                    buttonSound.play()
                    winScreen = False
                    return True


# Function for main menu
def menu():
    loadMenu() # load all main menu visuals
    running = True

    while running: # condition to keep program running
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                posX, posY = pygame.mouse.get_pos()
                print(posX, posY)
                if (posX >= (WIDTH-282)/2 and posX <= (WIDTH-282)/2 + 282) and (posY >= 180 and posY <= 300): # play button
                    buttonSound.play()
                    running = playGame()

                elif (posX >= (WIDTH-840)/2 and posX <= (WIDTH-840/2) + 840) and (posY >= 330 and posY <= 450): # instructions button
                    buttonSound.play()
                    running = showInstructions()
                
                elif (posX >= (WIDTH-280)/2 and posX <= (WIDTH-280)/2 + 280) and (posY >= 480 and posY <= 600): # exit button
                    buttonSound.play()
                    running = False
    
    pygame.quit() # quit the program when the condition becomes false
             

# Function for the play screen.
def playGame():
    # All of this is to restart the game upon clicking play.
    board = createBoard() 
    player = random.randint(1,2)
    turns = 0
    gameOver = False
    screen.fill(GRAY)
    drawBoard(False, board)
    while not gameOver: # while the game is running
        pygame.init()
        for event in pygame.event.get(): # allows user to quit during the game
            if event.type == pygame.QUIT:
                gameOver = True
                return False
            
            if event.type == pygame.KEYDOWN: # if escape key is pressed, the game will pause
                if event.key == pygame.K_ESCAPE:
                    gameOver = pauseGame(player, board) # if pauseGame() returns false, the game will restart
                    if gameOver == False:
                        turns = 0
                        board = createBoard()
                        screen.fill(GRAY)
                        drawBoard(True, board)
                        posX = pygame.mouse.get_pos()[0] # takes only the x-coordinate of the mouse
                        if player == 1: drawPiece(1, pieceX[checkCol(posX, pieceX)])
                        else: drawPiece(2, pieceX[checkCol(posX, pieceX)])

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP: # when the mouse moves or after a mouse click is registered
                pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, PIECE_SIZE))
                posX = event.pos[0] # gets x position of the mouse cursor
                drawPiece(player, pieceX[checkCol(posX, pieceX)]) # the piece indicator at the top of the screen will redraw itself


            pygame.display.update() # update display

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # upon left clicking
                posX = event.pos[0] # track the x coordinate of the mouse
                col = checkCol(posX, pieceX) # checks which column the mouse is hovering over
                print(turns)
                
                if player == 1: # player 1's turn
                    gameOver = dropPiece(col, 1, board) # play their turn

                    if gameOver == None: # if turn is invalid, replay.
                        gameOver = dropPiece(col, 1, board)

                    elif gameOver == "restart": # If user clicks restart
                        gameOver = False
                        turns = 0
                        board = createBoard()
                        screen.fill(GRAY)
                        drawBoard(True, board)
                        posX = pygame.mouse.get_pos()[0] # takes only the x-coordinate of the mouse
                        if player == 1: drawPiece(1, pieceX[checkCol(posX, pieceX)])
                        else: drawPiece(2, pieceX[checkCol(posX, pieceX)])

                    else:# if turn ends up valid, next player's turn
                        turns += 1
                        player = 2
                        if turns == 42: # checks for draw
                            gameOver = loadWin(3)
                
                else: # player 2's turn
                    gameOver = dropPiece(col, 2, board)

                    if gameOver == None:
                        gameOver = dropPiece(col, 2, board)

                    elif gameOver == "restart":
                        gameOver = False
                        turns = 0
                        board = createBoard()
                        screen.fill(GRAY)
                        drawBoard(True, board)
                        posX = pygame.mouse.get_pos()[0]
                        if player == 1: drawPiece(1, pieceX[checkCol(posX, pieceX)])
                        else: drawPiece(2, pieceX[checkCol(posX, pieceX)])

                    else:
                        turns += 1
                        player = 1
                        if turns == 42:
                            gameOver = loadWin(3)
                        
    loadMenu()
    return True

menu()