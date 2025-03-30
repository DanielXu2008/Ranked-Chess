import random

# define constants
CHECKMATE = 99999
STALEMATE = 0
PIECESCORE = {'k': 0, 'q': 900, 'r': 500, 'b': 300, 'n': 300, 'p': 100}

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
        # make the move 
        board.makeMove(move)
        
        if board.stalemate:
            score = STALEMATE
        elif board.checkmate:
            score = CHECKMATE
        else:
            # evaluate
            score = (-1) * countMaterial(board)

        if score > maxScore:
            bestMove = move
            maxScore = score
        
        # backtrack
        board.undoMove()
        
    return bestMove

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