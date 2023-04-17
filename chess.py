import pygame
import sys

from square import Square
from const import *
from game import Game
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game= Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        drag = self.game.drag

        while True:
            game.show_bg(self.screen)
            game.show_last_move(self.screen)
            game.show_moves(self.screen)
            game.show_piece(self.screen)

            game.show_hover(self.screen)

            if drag.dragging:
                drag.update_blit(self.screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag.update_mouse(event.pos)
                    clicked_row = drag.mouseY // SQSIZE
                    clicked_col = drag.mouseX // SQSIZE
                    
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.cals_moves(piece, clicked_row, clicked_col, bool=True)
                            drag.save_initial(event.pos)
                            drag.drag_piece(piece)

                            game.show_bg(self.screen)
                            game.show_moves(self.screen)
                            game.show_piece(self.screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if drag.dragging:
                        drag.update_mouse(event.pos)
                        game.show_bg(self.screen)
                        game.show_last_move(self.screen)
                        game.show_moves(self.screen)
                        game.show_piece(self.screen)
                        game.show_hover(self.screen)
                        drag.update_blit(self.screen)
                    
                elif event.type == pygame.MOUSEBUTTONUP:

                    if drag.dragging:
                        drag.update_mouse(event.pos)

                        released_row = drag.mouseY // SQSIZE
                        released_col = drag.mouseX // SQSIZE

                        initial = Square(drag.initial_row, drag.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial,final)

                        if board.valid_move(drag.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            game.sound_effect(captured)
                            board.move(drag.piece, move)
                            game.show_bg(self.screen)
                            game.show_last_move(self.screen)
                            game.show_piece(self.screen)
                            game.next_turn()

                    drag.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        drag = self.game.drag

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()