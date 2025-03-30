"""
Ranked Chess
A chess program featuring computer opponents 
ICS3U
Daniel Xu
Program History:
April 23 - program creation
"""

import pygame, engine, martinAI, nelsonAI, polgarAI

# define screen properties
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 512

# intialize pygame 
pygame.init()
pygame.display.set_caption("Ranked Chess")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# get fonts
pygame.font.init()
header = pygame.font.Font('fonts/lora.ttf', 65)
body = pygame.font.Font('fonts/lora.ttf', 40)

# load images
chessboard = pygame.image.load('images/Chessboard.png')
background = pygame.image.load('images/Background.jpg')
instructions = pygame.image.load('images/Instructions.png')

backButton = pygame.image.load('images/Back.png')
playButton = pygame.image.load('images/Play.png')
helpButton = pygame.image.load('images/Help.png')

martinImage = pygame.image.load('images/Martin.png')
nelsonImage = pygame.image.load('images/Nelson.png')
polgarImage = pygame.image.load('images/Polgar.png')

playerMove = pygame.image.load('images/PlayerMove.png')
engineMove = pygame.image.load('images/EngineMove.png')

gameOver = pygame.image.load('images/GameOver.png')
winImage = pygame.image.load('images/Win.png')
drawImage = pygame.image.load('images/Draw.png')
loseImage = pygame.image.load('images/Lose.png')

# for ease of refering to the different chess pieces
pDict = {}
pList = ['wp', 'wn', 'wb', 'wr', 'wq', 'wk', 'bp', 'bn', 'bb', 'br', 'bq', 'bk']

# load the piece images
for piece in pList:
    pDict[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + ".png"), (64, 64))

def drawPosition():
    '''
    This functions blits the chessboard and the pieces onto the screen
    '''
    
    # draw chessboard
    screen.blit(chessboard, (0, 0))
    
    # highlight the currently selected piece
    if clicks:
        pygame.draw.rect(screen, (255, 0, 0), (clicks[1]*64, clicks[0]*64, 64, 64))
        
    # highlight legal moves
    for mv in displayMoves:
        pygame.draw.rect(screen, (250, 0, 0), (mv[1]*64, mv[0]*64, 64, 64))
        
    # draw the pieces
    for r in range(8):
        for c in range(8):
            piece = board.position[r][c]
            if piece != '--':
                screen.blit(pDict[piece], pygame.Rect(c*64, r*64, 64, 64))

def clickToMove():
    '''
    This function handles the user interaction with the chess pieces and making moves
    Returns:
    - currentClick, a tuple, that represents the square of the selected piece
    '''
    
    # get the current selected piece
    currentClick = clicks
    
    # get clicked square from mouse position
    pos = pygame.mouse.get_pos()
    col = pos[0]//64    
    row = pos[1]//64

    # if no piece selected, assign the current square
    if not clicks and board.position[row][col][0] == board.color:
        currentClick = (row, col)
        # get legal moves for the piece the user selected
        for mv in legalMoves:
            if mv.startRow == row and mv.startCol == col:
                displayMoves.append((mv.endRow, mv.endCol))
    # if a piece is selected, see if the user clicked on a legal square for the piece to move
    elif clicks:
        currentClick = None
        # check if the user makes a legal move
        if (row, col) in displayMoves and clicks != (row, col):
            move = engine.Move(clicks[0], clicks[1], row, col, board.position)
            board.makeMove(move)
            board.engineTurn = True
        displayMoves.clear()

    return currentClick

def rankPlayer(ELO):
    '''
    This function returns a rank from a rating
    Parameters:
    - ELO, an integer, the user's rating 
    Returns:
    - rank, a string, the user's rank
    '''
    
    rank = 'Starter'
    
    if ELO > 2000:
        rank = 'Master'
    elif ELO > 1800:
        rank = 'Expert'
    elif ELO > 1500:
        rank = 'Intermediate'
    elif ELO > 1200:
        rank = 'Casual'
    elif ELO > 800:
        rank = 'Beginner'

    return rank


# initialize variables
clicks = None
legalMoves = []
displayMoves = []

# load the player data from save
fin = open("save.txt", "r")
try:
    playerELO = int(fin.read())
except:
    playerELO = 600
    
newPlayerELO = playerELO
playerRanking = rankPlayer(playerELO)
fin.close()

mode = 'title'
bot = 'martin'

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            
            if mode == 'title':
                if pygame.Rect(100, 370, 176, 88).collidepoint(pygame.mouse.get_pos()):
                    mode = 'menu'
                if pygame.Rect(400, 370, 177, 88).collidepoint(pygame.mouse.get_pos()):
                    mode = 'help'

            elif mode == 'help':
                if pygame.Rect(270, 430, 150, 76).collidepoint(pygame.mouse.get_pos()):
                    mode = 'title'
            
            elif mode == 'menu':
                if pygame.Rect(270, 430, 150, 76).collidepoint(pygame.mouse.get_pos()):
                    mode = 'title'
                # opponent 1                    
                if pygame.Rect(25, 100, 200, 200).collidepoint(pygame.mouse.get_pos()):
                    bot = 'martin'
                    board = engine.Board()
                    mode = 'play'
                # opponent 2
                elif pygame.Rect(250, 100, 200, 200).collidepoint(pygame.mouse.get_pos()):
                    bot = 'nelson'
                    board = engine.Board()
                    mode = 'play'
                # opponent 3
                elif pygame.Rect(475, 100, 200, 200).collidepoint(pygame.mouse.get_pos()):
                    bot = 'polgar'
                    board = engine.Board()
                    mode = 'play'

            elif mode == 'play':
                if pygame.mouse.get_pos()[0] < 512:
                    clicks = clickToMove()
            
            elif mode == 'end':
                if pygame.Rect(530, 430, 150, 76).collidepoint(pygame.mouse.get_pos()):
                    fout = open("save.txt", "w")
                    playerELO = newPlayerELO
                    fout.write(str(playerELO))
                    fout.close()
                    mode = 'title'
        
        # undo move feature (hidden/cheat code)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                clicks = None
                displayMoves.clear()
                board.undoMove()
                board.undoMove()
            
    # title screen
    if mode == 'title':
        screen.blit(background, (0, 0))
        screen.blit(playButton, (100, 370))
        screen.blit(helpButton, (400, 370))
        screen.blit(header.render('Ranked Chess!', False, (255, 255, 255)), (150, 50))
    # instructions menu
    elif mode == 'help':
        screen.fill((255, 255, 255))
        screen.blit(instructions, (0, 0))
        screen.blit(backButton, (270, 430))
    # bot select screen
    elif mode == 'menu':
        screen.fill((0, 0, 0))
        # show the player's current rating and rank
        playerRating = body.render('Your current ELO: ' + str(playerELO), False, (255, 255, 255))
        playerRanking = body.render('Your current rank: ' + rankPlayer(playerELO), False, (255, 255, 255))
        
        screen.blit(playerRating, (60, 300))
        screen.blit(playerRanking, (60, 350))
        screen.blit(body.render('Who would you like to play?', False, (255, 255, 255)), (60, 25))
        screen.blit(backButton, (270, 430))
        
        # display the different computer opponents
        screen.blit(martinImage, (25, 100))
        screen.blit(nelsonImage, (250, 100))
        screen.blit(polgarImage, (475, 100))
    # chess game
    elif mode == 'play':
        # get legal moves that the user can make
        legalMoves = board.getLegalMoves()
        
        screen.fill((0, 0, 0))
        drawPosition()
        
        # check if game ends 
        if board.checkmate or board.stalemate:
            mode = 'end'
        else:
            # indicate to the user whose move it is
            if not board.engineTurn:
                screen.blit(playerMove, (525, 400))
            elif board.engineTurn:
                screen.blit(engineMove, (512, 0))
                
            # update display early as the engine will take a long time to finish thinking
            pygame.display.update()

            if board.engineTurn == True:     
                # choose accordingly to which opponent the user chose
                if bot == 'martin':
                     board.makeMove(martinAI.findBestMove(board, legalMoves))
                elif bot == 'nelson':
                     board.makeMove(nelsonAI.findBestMove(board, legalMoves))
                elif bot == 'polgar':
                    board.makeMove(polgarAI.findBestMove(board, legalMoves, 0))
                    
                board.engineTurn = False
    # ending screen  
    elif mode == 'end':
        screen.blit(gameOver, (512, 150))
        screen.blit(backButton, (530, 430))
        
        if board.color == 'b' and board.checkmate:
            screen.blit(winImage, (512, 250))
            result = 1
        elif board.color == 'w' and board.checkmate:
            screen.blit(loseImage, (512, 250))
            result = 0
        else:
            screen.blit(drawImage, (512, 250))
            result = 0.5
        
        if bot == 'martin':
            botELO = 500
        elif bot == 'nelson':
            botELO = 1200
        elif bot == 'polgar':
            botELO = 2000
            
        expected = 1 / (1 + 10**((botELO - playerELO)/400))
        newPlayerELO = round(playerELO + 100*(result-expected))
        
    pygame.display.update()
    clock.tick(30)
            
pygame.quit()