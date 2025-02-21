import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = theme.bg.dark 
                else:
                    color = theme.bg.light
                
                # if(row + col) % 2 == 0:
                #     color = (234, 235, 200)
                # else:
                #     color = (119, 154, 88)

                rect = (col * SQSIZE, row *SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

                # if col == 0:
                #     # color
                #     color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                #     # label
                #     lbl = self.config.font.render(str(ROWS-row), 1, color)
                #     lbl_pos = (5, 5 + row * SQSIZE)
                #     # blit
                #     surface.blit(lbl, lbl_pos)

                # # col coordinates
                # if row == 7:
                #     # color
                #     color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                #     # label
                #     lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                #     lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                #     # blit
                #     surface.blit(lbl, lbl_pos)
                    #print(lbl, lbl_pos)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range (COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                if(move.final.row + move.final.col) % 2 == 0 :
                    color = theme.moves.light
                else:
                    color = theme.moves.dark

                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # print(piece,color)

                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark

                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180) #if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)

            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        if (self.next_player == "black"):
            self.next_player = "white"
        else:
            self.next_player = "black"

    def set_hover(self, row, col):
        # print(self)
        # print(self.board.squares)
        if col < 8 and row < 8:
            # print(row)
            # print(col)
            self.hovered_sqr = self.board.squares[row][col]
        

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()