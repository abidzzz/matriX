import pygame
from pygame.locals import *
import threading

from board import Board
from piece import Piece
from ui import Ui

class Game:   

    def __init__(self) :

        
        self.WIN = pygame.display.set_mode((1130, 700))
        self._import()  
        pygame.init()
        pygame.display.set_caption('matriX')

        self.run = True
        
        self.clock = pygame.time.Clock()
        
        
    def _import(self):
        self.piece = Piece()
        self.pieces = self.piece.getRandomPiece()
        # print(self.pieces)
        
        self.ui = Ui()
        self.surfaces = self.ui.getSurfaces(self.pieces)

        self.board = Board()
        self.boardSurface = self.board.surface

        self.game_over = False
        self.dragger = self.ui.dragger
        

    
    def draw(self):
        win = self.WIN
        self.ui.show_board(win, self.boardSurface)
        self.ui.display_score(self.board.score, win)
        

        try:
            self.ui.hover(win)  
        except:
            pass

        updated_win = self.board.makeSurface()
        self.board.surface = updated_win
        
        win.blit(self.board.surface , (200, 100, 540, 540) )

        self.ui.show_pieces(win, self.pieces)

        if self.dragger.dragging:
            self.dragger.updatePieceSurface(win)

        if self.game_over : 
            self.ui.show_menu(win, "Game Over! ")

   
        
    def update_pieces(self):
        if len(self.pieces) == 0:
            self.pieces = self.piece.getRandomPiece()
            self.surfaces = self.ui.getSurfaces(self.pieces)
        
    def restart(self, win):
        self.board.reset(win)
        self.pieces = []
        self.draw()
        self.board.animate(self.WIN)
        self.game_over = False       

        
    def loop(self):
        self.draw()
        self.board.animate(self.WIN)
        while self.run:
            self.game_over = self.board.gameOver(self.pieces)
            self.update_pieces()
            self.draw()
            self.handle_events()
            self.clock.tick()
            pygame.display.update()
            
    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False 
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                surf, piece, x, y = self.board.getSurface(event.pos, self.surfaces)
                
                if surf:
                    self.dragger.drag_piece(piece)                    
                    self.dragger.updatePos(event.pos)
                    self.dragger.save_initial((x,y))
                    
                    
                   
            elif event.type == pygame.MOUSEMOTION:
                if self.dragger.dragging :
                    
                    self.dragger.updatePos(event.pos)

                    pos = self.board.getPos(event.pos)

                    if pos :
                        if self.board.isValid(pos, self.dragger.piece) : 
                            self.ui.hoverPos = pos
                            self.draw()
                    
                else:
                    self.ui.hoverPos = None

                
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragger.dragging:
                    self.dragger.updatePos(event.pos)
                    pos = self.board.getPos(event.pos)
                    
                    if pos:

                        if self.board.isValid(pos, self.dragger.piece) :
                            self.draw()
                            
                            self.board.placePiece(pos, self.dragger.piece, self.WIN)
                            
                            self.pieces.remove(self.dragger.piece)
                            
                            self.surfaces = self.ui.getSurfaces(self.pieces)
                    
                self.dragger.undrag_piece()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.run = False
                
                elif event.key == pygame.K_r:
                    self.restart(self.WIN)


                   
if __name__ == '__main__':
    game=Game()
    game.loop()
