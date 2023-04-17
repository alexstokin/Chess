import pygame
from square import Square
from board import Board
from const import *
from drag import Drag
from config import Config

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hover_sqr = None
        self.board = Board()
        self.drag = Drag()
        self.config = Config()
        

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(row+col) % 2 == 0:
                    color = (234,235,200)
                else:
                    color = (119,154,88)
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE,SQSIZE)

                pygame.draw.rect(surface, color, rect)
                if col == 0:
                    color = (0,0,0) if row % 2 == 0 else (0,0,0)
                    lbl = self.config.font.render(str(ROWS-row),1,color)
                    lbl_pos = (5,5 + row * SQSIZE)
                    surface.blit(lbl,lbl_pos)

                if row == 7:
                    color = (0,0,0) if (row+col)% 2 == 0 else (0,0,0)
                    lbl = self.config.font.render(Square.get_alphacol(col),1,color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 30)
                    surface.blit(lbl,lbl_pos)

    def show_piece(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.drag.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    def show_moves(self,surface):
        if self.drag.dragging:
            piece = self.drag.piece

            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C86464'

                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244,247,116) if (pos.row + pos.col) % 2 == 0 else (172,195,51)
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_hover(self,surface):
        if self.hover_sqr:
            color = (180,180,180)
            rect = (self.hover_sqr.col * SQSIZE, self.hover_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface,color,rect, width=3)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self,row,col):
        self.hover_sqr = self.board.squares[row][col]

    def sound_effect(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()