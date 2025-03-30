import random

# define constants 
CHECKMATE = 99999
STALEMATE = 0
PIECESCORE = {'k': 0, 'q': 1000, 'r': 400, 'b': 200, 'n': 200, 'p': 50}

# piece square tables, values used in evaluation that customize the bot 
queenPSQT = [[-40, -40,-40,-40,-40,-40, -40,-40],
            [-30, -20,-20,-20,-20,-20, -20,-30],
            [20, 20, 20, 20, 20, 20, 20, 20],
            [40, 40, 40, 40, 40, 40, 40, 40],
            [20, -40, 40, 40, 40, 40, 40, 20],  
            [-10, -40, 40, 40, 40,40, 40,-10],
            [-30, -20,-20,-20,-20,-20, -20,-30],
            [-40, -40,-40,-40,-40,-40, -40,-40]]
knightPSQT = [[-10, -20,-20,-20,-20,-20, -20,-10],
            [-40,-20,  0,  0,  0,  0,-20, -40],
            [-30,  0, 10, 15, 15, 10,  0, -30],
            [-30,  5, 15, 20, 20, 15,  5, -30],
            [-30,  0, 15, 20, 20, 15,  0, -30],  
            [-30,  5, 10, 15, 15, 10,  5, -30],
            [-40,-20,  0,  5,  5,  0,-20, -40],
            [-50, -20,-20,-20,-20,-20, -20, -50]]
bishopPSQT = [[-10, -10, -10, -10, -10, -10, -10, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10, -10, -20, -10, -10, -20, -10, -10]]
pawnPSQT = [[0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]]

def findBestMove(board, legalMoves):
    '''
    This functions finds the 'best' move in a position
    Arguments:
    - board, a class, the current game position 
    - legalMoves, the legal moves in the position
    Returns:
    - bestMove, a move, the best move that was found    
    '''
    
    random.shuffle(legalMoves)
    bestMove = random.choice(legalMoves)
    maxScore = (-1) * CHECKMATE

    # loop through all the moves and evalute each one to find the best 
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
            # loop through all the opponent moves and evalute each one to find the best counter
            for opponentMove in opponentMoves:
                board.makeMove(opponentMove)
                
                if board.stalemate:
                    currentOpponentMaxScore = STALEMATE
                elif board.checkmate:
                    currentOpponentMaxScore = CHECKMATE
                else:
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

    return bestMove

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
            elif board.position[r][c] == 'wq':
                score += queenPSQT[r][c]
            elif board.position[r][c] == 'wp':
                score += pawnPSQT[r][c]
            elif board.position[r][c] == 'wb':
                score += bishopPSQT[r][c]
            elif board.position[r][c] == 'bn':
                score -= knightPSQT[7-r][7-c]
            elif board.position[r][c] == 'bq':
                score -= queenPSQT[7-r][7-c]
            elif board.position[r][c] == 'bp':
                score -= pawnPSQT[7-r][7-c]
            elif board.position[r][c] == 'bb':
                score -= bishopPSQT[7-r][7-c]

    return score