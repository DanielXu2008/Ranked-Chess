import random

# define constants
CHECKMATE = 99999
STALEMATE = 0
ENDGAME_START = 24
MAX_DEPTH = 1
PIECESCORE = {'k': 0, 'q': 900, 'r': 500, 'b': 300, 'n': 300, 'p': 100}

# piee# piece square tables, values used in evaluation that customize the bot 
knightPSQT = [[-10, -20,-20,-20,-20,-20, -20,-10],
            [-40,-20,  0,  0,  0,  0,-20, -40],
            [-30,  0, 10, 15, 15, 10,  0, -30],
            [-30,  5, 15, 20, 20, 15,  5, -30],
            [-30,  0, 15, 20, 20, 15,  0, -30],  
            [-30,  5, 10, 15, 15, 10,  5, -30],
            [-40,-20,  0,  5,  5,  0,-20, -40],
            [-50, -20,-20,-20,-20,-20, -20, -50]]
pawnPSQT = [[0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]]
kingPSQT = [[-40, -40, -40, -40, -40, -40, -40, -40],
            [-40, -40, -40, -40, -40, -40, -40, -40],
            [-40, -40, -40, -40, -40, -40, -40, -40],
            [-40, -40, -40, -40, -40, -40, -40, -40],
            [-40, -40, -40, -40, -40, -40, -40, -40],
            [-40, -40, -40, -40, -40, -40, -40, -40],
            [-20, -20, -20, -20, -20, -20, -20, -20],
            [0,  40,  20, 0,  -20, 40,  40,  20]]
bishopPSQT = [[-10, -10, -10, -10, -10, -10, -10, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10, -10, -20, -10, -10, -20, -10, -10]]
endgameKingPSQT =  [[30, 20, 20, 20, 20, 20, 25, 30],
                    [25, 10, 10, 5, 5, 10, 10, 25],
                    [20, 10, -5, -5, -5, -5, 10, 20],
                    [20, 10, -5, -20, -20, -5, 5, 20],
                    [20, 10, -5, -20, -20, -5, 5, 20],  
                    [20, 10, -5, -5, -5, 0, 10, 20],
                    [25, 10, 10, 5, 5, 10, 10, 25],
                    [30, 25, 20, 20, 20, 20, 25, 30]]

def findBestMove(board, legalMoves, depth):
    '''
    This functions finds the 'best' move in a position
    Arguments:
    - board, a class, the current game position 
    - legalMoves, the legal moves in the position
    - depth, the how far the engine is currently searching at
    Returns:
    - bestMove, a move, the best move that was found
    - maxScore, an integer, the highest scoring evaluation of a move that was found
    '''
    
    random.shuffle(legalMoves)
    bestMove = random.choice(legalMoves)
    maxScore = (-1) * CHECKMATE

    for move in legalMoves:
        board.makeMove(move)
        currentMaxScore = (-1) * CHECKMATE
    
        if board.stalemate:
            currentMaxScore = STALEMATE
        elif board.checkmate:
            currentMaxScore = CHECKMATE
        else:
            opponentMaxScore = (-1) * CHECKMATE
            currentOpponentMaxScore = (-1) * CHECKMATE
            opponentMoves = board.getLegalMoves()
            
            for opponentMove in opponentMoves:
                board.makeMove(opponentMove)
                
                if board.stalemate:
                    currentOpponentMaxScore = STALEMATE
                elif board.checkmate:
                    currentOpponentMaxScore = CHECKMATE
                elif depth < MAX_DEPTH and opponentMove.pieceCaptured != '--':
                    # recursive function call when max depth is not reached
                    currentOpponentMaxScore = findBestMove(board, board.getLegalMoves(), depth+1)
                else:
                    # evaluation when maximum depth is reached
                    currentOpponentMaxScore = evaluate(board)

                if currentOpponentMaxScore > opponentMaxScore:
                    opponentMaxScore = currentOpponentMaxScore
                    
                board.undoMove()
                
                if (-1) * opponentMaxScore < maxScore:
                    break

            currentMaxScore = (-1) * opponentMaxScore
                
        if currentMaxScore > maxScore:
            maxScore = currentMaxScore
            bestMove = move
        
        board.undoMove()

    if depth == 0:
        return bestMove
    else:
        return -maxScore

def evaluate(board):
    '''
    This functions evaluates a position
    Arguments:
    - board, a class, the current game position 
    Returns:
    - evaluation, an integer, the evaluation    
    '''
    
    evaluation = 0
    
    evaluation += countMaterial(board)
    evaluation += pieceSquareTable(board)

    return evaluation

def countMaterial(board):
    '''
    This functions counts the material in a position to evaluate it
    Arguments:
    - board, a class, the current game position 
    Returns:
    - score, an integer, the evaluation    
    '''
    
    score = 0

    for r in range(8):
        for c in range(8):
            if board.position[r][c][0] == 'w':
                score += PIECESCORE[board.position[r][c][1]]
            elif board.position[r][c][0] == 'b':
                score -= PIECESCORE[board.position[r][c][1]]
    
    return score

def pieceSquareTable(board):
    '''
    This functions uses the valeus in the piece square tables to refine the evaluation of the position
    Arguments:
    - board, a class, the current game position 
    Returns:
    - score, an integer, the evaluation    
    '''
    
    score = 0

    for r in range(8):
        for c in range(8):
            if board.position[r][c] == 'wn':
                score += knightPSQT[r][c]
            elif board.position[r][c] == 'wp':
                score += pawnPSQT[r][c]
            elif board.position[r][c] == 'wk':
                if board.pieceCount < ENDGAME_START:
                    score -= endgameKingPSQT[r][c]
                else:
                    score += kingPSQT[r][c]
            elif board.position[r][c] == 'wb':
                score += bishopPSQT[r][c]
            elif board.position[r][c] == 'bn':
                score -= knightPSQT[7-r][7-c]
            elif board.position[r][c] == 'bp':
                score -= pawnPSQT[7-r][7-c]
            elif board.position[r][c] == 'bk':
                if board.pieceCount < ENDGAME_START:
                    score += endgameKingPSQT[r][c]
                else:
                    score -= kingPSQT[7-r][7-c]
            elif board.position[r][c] == 'bb':
                score -= bishopPSQT[7-r][7-c]

    return score