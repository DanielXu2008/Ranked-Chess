rowToRank = [8, 7, 6, 5, 4, 3, 2, 1]
colToFile = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Board:
    def __init__(self):
        '''
        This functions intializes the board and chess game
        '''
        
        self.position = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]
        
        
        self.whiteTurn = True
        self.inCheck = False
        self.checkLog = [False]
        self.checkmate = False
        self.stalemate = False
        # binary representation of castling rights, for example:
        # whiteShort = True, whiteLong = False, blackShort = True, blackLong = False -> 0101 = 5
        self.castleRight = 0
        self.castleLog = [0]
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.color = 'w'
        self.engineTurn = False
        self.pieceCount = 32
        self.moveLog = []

    def makeMove(self, move):
        '''
        This functions makes a move on the board
        Parameters:
        - move, a class, that stores the information of the current move
        '''
        
        self.position[move.endRow][move.endCol] = self.position[move.startRow][move.startCol]
        self.position[move.startRow][move.startCol] = '--'

        # promotion
        if self.color == 'w' and move.endRow == 0 and move.pieceMoved == 'wp':
            self.position[move.endRow][move.endCol] = 'wq'
        elif self.color == 'b' and move.endRow == 7 and move.pieceMoved == 'bp':
            self.position[move.endRow][move.endCol] = 'bq'

        if move.pieceCaptured != '--':
            self.pieceCount -= 1

        # castling
        if move.pieceMoved == 'wk' and move.startRow == 7 and move.startCol == 4 and move.endRow == 7:
            if move.endCol == 6:
                self.position[7][5] = 'wr'
                self.position[7][7] = '--'
            elif move.endCol == 2:
                self.position[7][3] = 'wr'
                self.position[7][0] = '--' 
        elif move.pieceMoved == 'bk' and move.startRow == 0 and move.startCol == 4 and move.endRow == 0:
            if move.endCol == 6:
                self.position[0][5] = 'br'
                self.position[0][7] = '--'
            elif move.endCol == 2:
                self.position[0][3] = 'br'
                self.position[0][0] = '--'
                
        if move.pieceMoved == 'wk':
            self.whiteKingLocation = (move.endRow, move.endCol)
            self.castleRight |= 1 
            self.castleRight |= 2
        elif move.pieceMoved == 'bk':
            self.blackKingLocation = (move.endRow, move.endCol)
            self.castleRight |= 4
            self.castleRight |= 8
        elif move.pieceMoved == 'wr':
            if move.startRow == 7 and move.startCol == 7:
                self.castleRight |= 1
            elif move.startRow == 7 and move.startCol == 0:
                self.castleRight |= 2
        elif move.pieceMoved == 'br':
            if move.startRow == 0 and move.startCol == 7:
                self.castleRight |= 4
            elif move.startRow == 0 and move.startCol == 0:
                self.castleRight |= 8

        if self.position[7][7] != 'wr':
            self.castleRight |= 1
        if self.position[7][0] != 'wr':
            self.castleRight |= 2
        if self.position[0][7] != 'br':
            self.castleRight |= 4
        if self.position[0][0] != 'br':
            self.castleRight |= 8

        # append some information that is difficult to keep track of normally
        self.moveLog.append(move)
        self.checkLog.append(self.inCheck)
        self.castleLog.append(self.castleRight)

        # swap side to move 
        self.whiteTurn = not self.whiteTurn
        self.color = 'w' if self.whiteTurn else 'b'
        
        kingLocation = self.whiteKingLocation if self.whiteTurn else self.blackKingLocation

        # detect checks
        if len(self.findChecks(kingLocation)):
            self.inCheck = True
        else:
            self.inCheck = False
            
        legalMoves = self.getLegalMoves()
        
        # look for checkmate and stalemate
        if len(legalMoves) == 0 and self.inCheck:
            self.checkmate = True
        elif len(legalMoves) == 0 and not self.inCheck:
            self.stalemate = True
        
    def undoMove(self):
        '''
        This functions undos a move on the board
        '''
        
        if len(self.moveLog) != 0:
            # restore everything to the previous move
            move = self.moveLog.pop()
            self.checkLog.pop()
            self.castleLog.pop()
            
            self.checkmate = False
            self.stalemate = False

            self.inCheck = self.checkLog[-1]
            self.castleRight = self.castleLog[-1]

            self.position[move.startRow][move.startCol] = move.pieceMoved
            self.position[move.endRow][move.endCol] = move.pieceCaptured
            
            if move.pieceCaptured != '--':
                self.pieceCount += 1

            if move.pieceMoved == 'wk':
                self.whiteKingLocation = (move.startRow, move.startCol)

            elif move.pieceMoved == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)
                
            # castling
            if move.pieceMoved == 'wk' and move.startRow == 7 and move.startCol == 4 and move.endRow == 7 and move.endCol == 6:
                self.position[7][5] = '--'
                self.position[7][7] = 'wr'
            elif move.pieceMoved == 'wk' and move.startRow == 7 and move.startCol == 4 and move.endRow == 7 and move.endCol == 2:
                self.position[7][3] = '--'
                self.position[7][0] = 'wr'
            elif move.pieceMoved == 'bk' and move.startRow == 0 and move.startCol == 4 and move.endRow == 0 and move.endCol == 6:
                self.position[0][5] = '--'
                self.position[0][7] = 'br'
            elif move.pieceMoved == 'bk' and move.startRow == 0 and move.startCol == 4 and move.endRow == 0 and move.endCol == 2:
                self.position[0][3] = '--'
                self.position[0][0] = 'br'
                
            self.whiteTurn = not self.whiteTurn
            self.color = 'w' if self.whiteTurn else 'b'

    def findChecks(self, kingLocation):
        '''
        This functions finds possible checks for a specific location on the board
        Parameters:
        - kingLocation, a tuple, representing the square to be checked
        Return:
        - checks, a list of tuples, that contains the possible checks
        '''
        
        pins = []
        checks = []

        bishopDirections = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        rookDirections = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        knightDirections = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]

        # white pawn checks
        if self.color == 'w':
            endRow = kingLocation[0] - 1
            endCol = kingLocation[1] - 1
            
            if (0 <= endRow < 8) and (0 <= endCol < 8):     
                if self.position[endRow][endCol] == 'bp':
                    checks.append((endRow, endCol))

            endRow = kingLocation[0] - 1
            endCol = kingLocation[1] + 1
            
            if (0 <= endRow < 8) and (0 <= endCol < 8):     
                if self.position[endRow][endCol] == 'bp':
                    checks.append((endRow, endCol))
        # black pawn checks
        else:
            endRow = kingLocation[0] + 1
            endCol = kingLocation[1] - 1
            
            if (0 <= endRow < 8) and (0 <= endCol < 8):     
                if self.position[endRow][endCol] == 'wp':
                    checks.append((endRow, endCol))

            endRow = kingLocation[0] + 1
            endCol = kingLocation[1] + 1
            
            if (0 <= endRow < 8) and (0 <= endCol < 8):     
                if self.position[endRow][endCol] == 'wp':
                    checks.append((endRow, endCol))

        # bishop and queen checks
        for d in bishopDirections:
            blocked = False
            for distance in range(1, 8):
                endRow = kingLocation[0] + (d[0]*distance)
                endCol = kingLocation[1] + (d[1]*distance)
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if self.position[endRow][endCol] == '--':
                        continue  
                    if self.position[endRow][endCol][0] != self.color:
                        if self.position[endRow][endCol][1] == 'b' or self.position[endRow][endCol][1] == 'q' or (distance == 1 and self.position[endRow][endCol][1] == 'k'):
                            if not blocked:
                                checks.append((endRow, endCol))
                            else:
                                pins.append((endRow, endCol))
                    blocked = True
        
        # rook and queen checks
        for d in rookDirections:
            blocked = False
            for distance in range(1, 8):
                endRow = kingLocation[0] + (d[0]*distance)
                endCol = kingLocation[1] + (d[1]*distance)
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if self.position[endRow][endCol] == '--':
                        continue
                    if self.position[endRow][endCol][0] != self.color:
                        if self.position[endRow][endCol][1] == 'r' or self.position[endRow][endCol][1] == 'q' or (distance == 1 and self.position[endRow][endCol][1] == 'k'):
                            if not blocked:
                                checks.append((endRow, endCol))
                            else:
                                pins.append((endRow, endCol))
                    blocked = True

        # knight checks
        for d in knightDirections:
            endRow = kingLocation[0] + d[0]
            endCol = kingLocation[1] + d[1]
                                    
            if (0 <= endRow < 8) and (0 <= endCol < 8):
                if self.position[endRow][endCol][0] != self.color and self.position[endRow][endCol][1] == 'n':
                    checks.append((endRow, endCol))

        return checks
        
    def validMove(self, move):
        '''
        This functions filters out pseudo-legal moves for fully-legal moves
        Parameters:
        - move, a class, representing the move to be filtered
        Return:
        - valid, a boolean, if the move is legal or not
        '''
        
        valid = True
        kingLocation = self.whiteKingLocation if self.whiteTurn else self.blackKingLocation

        # is the move was a king move, remove king from board temporarily and search for checks on the king's new square
        if move.pieceMoved[1] == 'k':
            self.position[kingLocation[0]][kingLocation[1]] = '--'

            if move.pieceMoved[1] == 'k' and len(self.findChecks((move.endRow, move.endCol))):
                valid = False
            
            self.position[kingLocation[0]][kingLocation[1]] = self.color + 'k'
        # otherwise simulate the move and see if resulting position is legal
        else:
            occupied = self.position[move.endRow][move.endCol]
            self.position[move.endRow][move.endCol] = self.position[move.startRow][move.startCol]
            self.position[move.startRow][move.startCol] = '--'

            if len(self.findChecks((kingLocation))):
                valid = False

            self.position[move.startRow][move.startCol] = self.position[move.endRow][move.endCol] 
            self.position[move.endRow][move.endCol] = occupied

        return valid
    
    def getLegalMoves(self):
        '''
        This functions gets all fully-legal moves from the current position
        Returns:
        - legalMoves, a list, that contains all the legal moves
        '''
        
        possibleMoves = self.getPossibleMoves()
        legalMoves = [move for move in possibleMoves if self.validMove(move)]
        return legalMoves
    
    def getPossibleMoves(self):
        '''
        This functions generates all the pseudo-legal moves
        Returns:
        - possibleMoves, a list, that contains all the pseudo-legal moves
        '''
        
        moves = []
        
        # iterate through the chess board and generate moves for every piece that is the correct colour
        for r in range(8):
            for c in range(8):
                if (self.position[r][c][0] == 'w' and self.whiteTurn) or (self.position[r][c][0] == 'b' and not self.whiteTurn):
                    piece = self.position[r][c][1]
                    if piece == 'p':
                        self.pawnMoves(r, c, moves)
                    if piece == 'n':
                        self.knightMoves(r, c, moves)
                    elif piece == 'b':
                        self.bishopMoves(r, c, moves)
                    elif piece == 'r':
                        self.rookMoves(r, c, moves)
                    elif piece == 'q':
                        self.queenMoves(r, c, moves)
                    elif piece == 'k':
                        self.kingMoves(r, c, moves)
        
        return moves
                        
    def pawnMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal pawn moves
        Arguments:
        - r, an integer, the rank of the pawn
        - c, an integer, the column of the pawn
        - moves, the list of pseudo-legal moves that will be appened to
        '''
    
        if self.whiteTurn:
            if self.position[r-1][c] == '--':
                moves.append(Move(r, c, r-1, c, self.position))
                if r == 6 and self.position[r-2][c] == '--':
                    moves.append(Move(r, c, r-2, c, self.position))
            if (c+1 < 8) and self.position[r-1][c+1][0] == 'b':
                moves.append(Move(r, c, r-1, c+1, self.position))
            if (c-1 >= 0) and self.position[r-1][c-1][0] == 'b':
                moves.append(Move(r, c, r-1, c-1, self.position))
        else:
            if self.position[r+1][c] == '--':
                moves.append(Move(r, c, r+1, c, self.position))
                if r == 1 and self.position[r+2][c] == '--':
                    moves.append(Move(r, c, r+2, c, self.position))
            if (c+1 < 8) and self.position[r+1][c+1][0] == 'w':
                moves.append(Move(r, c, r+1, c+1, self.position))
            if (c-1 >= 0) and self.position[r+1][c-1][0] == 'w':
                moves.append(Move(r, c, r+1, c-1, self.position))
            
    def knightMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal knight moves
        Arguments:
        - r, an integer, the rank of the knight
        - c, an integer, the column of the knight
        - moves, the list of pseudo-legal moves that will be appened to
        '''
                
        directions = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if (0 <= endRow < 8) and (0 <= endCol < 8):
                if self.position[endRow][endCol][0] != self.color:
                    moves.append(Move(r, c, endRow, endCol, self.position))

                    
    def bishopMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal bishop moves
        Arguments:
        - r, an integer, the rank of the bishop
        - c, an integer, the column of the bishop
        - moves, the list of pseudo-legal moves that will be appened to
        '''
        
        directions = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

        for d in directions:
            for distance in range(1, 8):
                endRow = r + (d[0]*distance)
                endCol = c + (d[1]*distance)
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if self.position[endRow][endCol] == '--':
                        moves.append(Move(r, c, endRow, endCol, self.position))
                    elif self.position[endRow][endCol][0] != self.color:
                        moves.append(Move(r, c, endRow, endCol, self.position))
                        break
                    else:
                        break
                        
    def rookMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal rook moves
        Arguments:
        - r, an integer, the rank of the rook
        - c, an integer, the column of the rook
        - moves, the list of pseudo-legal moves that will be appened to
        '''
        
        directions = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        
        for d in directions:
            for distance in range(1, 8):
                endRow = r + (d[0]*distance)
                endCol = c + (d[1]*distance)
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if self.position[endRow][endCol] == '--':
                        moves.append(Move(r, c, endRow, endCol, self.position))
                    elif self.position[endRow][endCol][0] != self.color:
                        moves.append(Move(r, c, endRow, endCol, self.position))
                        break
                    else:
                        break
                    
    def queenMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal queen moves
        Arguments:
        - r, an integer, the rank of the queen
        - c, an integer, the column of the queen
        - moves, the list of pseudo-legal moves that will be appened to
        '''
        
        directions = [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [-1, 1], [-1, -1], [1, -1]]
        
        for d in directions:
            for distance in range(1, 8):
                endRow = r + (d[0]*distance)
                endCol = c + (d[1]*distance)
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if self.position[endRow][endCol] == '--':
                        moves.append(Move(r, c, endRow, endCol, self.position))
                    elif self.position[endRow][endCol][0] != self.color:
                        moves.append(Move(r, c, endRow, endCol, self.position))
                        break
                    else:
                        break
                    
    def kingMoves(self, r, c, moves):
        '''
        This functions generates all the possible pseudo-legal king moves
        Arguments:
        - r, an integer, the rank of the king
        - c, an integer, the column of the king
        - moves, the list of pseudo-legal moves that will be appened to
        '''
        
        directions = [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [-1, 1], [-1, -1], [1, -1]]
        
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if (0 <= endRow < 8) and (0 <= endCol < 8):
                if self.position[endRow][endCol][0] != self.color:
                    moves.append(Move(r, c, endRow, endCol, self.position))
        
        # castling
        if not self.inCheck:
            if self.whiteTurn:
                if not (self.castleRight & 1) and self.position[7][5] == '--' and self.position[7][6] == '--' and len(self.findChecks((7, 5))) == 0 and len(self.findChecks((7, 6))) == 0:
                    moves.append(Move(7, 4, 7, 6, self.position))
                if not (self.castleRight & 2) and self.position[7][1] == '--' and self.position[7][2] == '--' and self.position[7][3] == '--' and len(self.findChecks((7, 2))) == 0 and len(self.findChecks((7, 3))) == 0:
                    moves.append(Move(7, 4, 7, 2, self.position))
            else:
                if not (self.castleRight & 4) and self.position[0][5] == '--' and self.position[0][6] == '--' and len(self.findChecks((0, 5))) == 0 and len(self.findChecks((0, 6))) == 0:
                    moves.append(Move(0, 4, 0, 6, self.position))
                if not (self.castleRight & 8) and self.position[0][1] == '--' and self.position[0][2] == '--' and self.position[0][3] == '--' and len(self.findChecks((0, 2))) == 0 and len(self.findChecks((0, 3))) == 0:
                    moves.append(Move(0, 4, 0, 2, self.position))

class Move:
    def __init__(self, r1, c1, r2, c2, board):
        '''
        This functions intializes the move class, which will contain all the information for a single move
        '''
        self.startRow = r1
        self.startCol = c1
        self.endRow = r2
        self.endCol = c2
        self.pieceMoved = board[r1][c1]
        self.pieceCaptured = board[r2][c2]
        self.position = board
        
    def notation(self):
        '''
        A utily function that prints out the move in chess notation
        '''
        moveNotation = ''
        
        if self.pieceMoved[1] != 'p':
            moveNotation += self.pieceMoved[1].upper()
            
        moveNotation += (f'{colToFile[self.startCol]}{rowToRank[self.startRow]}-{colToFile[self.endCol]}{rowToRank[self.endRow]}')
        
        return moveNotation