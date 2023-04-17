from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.casteling(initial, final):
                diff = initial.col - final.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True

        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self,piece,final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def casteling(self,initial,final):
        return abs(initial.col - final.col) == 2
    
    def in_check(self,piece,move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].hasRivalPiece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.cals_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def cals_moves(self, piece, row, col, bool = True):
        #calculate all valid moves of a specific piece on specific position

        def pawn_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isEmpty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                    else: break
                else: break

            possible_move_row = row + piece.dir
            possible_move_col = [col-1, col+1]
            for possible_move_cols in possible_move_col:
                if Square.in_range(possible_move_row, possible_move_cols):
                    if self.squares[possible_move_row][possible_move_cols].hasRivalPiece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_cols].piece
                        final = Square(possible_move_row, possible_move_cols, final_piece)
                        move = Move(initial,final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

        def knight_moves():
            possible_moves = [
                (row-2,col+1),
                (row-1,col+2),
                (row+1,col+2),
                (row+2,col+1),
                (row+2,col-1),
                (row+1,col-2),
                (row-1,col-2),
                (row-2,col-1),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isEmptyOrRival(piece.color):
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                            else: 
                                break
                        else:
                            piece.add_moves(move)        

        def straigtline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row,possible_move_col):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isEmpty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                        elif self.squares[possible_move_row][possible_move_col].hasRivalPiece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].hasTeamPiece(piece.color):
                            break

                    else: break
                        
                    possible_move_row, possible_move_col = possible_move_row + row_incr, possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0),
                (row-1, col+1),
                (row+0, col+1),
                (row+1, col+1),
                (row+1, col+0),
                (row+1, col-1),
                (row+0, col-1),
                (row-1, col-1),
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isEmptyOrRival(piece.color):
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                            else: 
                                break
                        else:
                            piece.add_moves(move)

            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                initial = Square(row,0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                left_rook.add_moves(moveR)

                                initial = Square(row,col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_moves(moveR)
                                        piece.add_moves(moveK)
                                else:
                                    left_rook.add_moves(moveR)
                                    piece.add_moves(moveK)
            
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(row,7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                initial = Square(row,col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_moves(moveR)
                                        piece.add_moves(moveK)
                                else:
                                    right_rook.add_moves(moveR)
                                    piece.add_moves(moveK)

        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop): straigtline_moves([
                (-1,1),
                (-1,-1),
                (1,1),
                (1,-1)
        ])
        elif isinstance(piece, Rook): straigtline_moves([
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
        ])
        elif isinstance(piece, Queen): straigtline_moves([
                (-1,1),
                (-1,-1),
                (1,1),
                (1,-1),
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
        ])
        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)

    def _add_pieces(self,color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        self.squares[row_other][4] = Square(row_other, 4, King(color))