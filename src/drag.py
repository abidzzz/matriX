
import pygame
import os

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.X = 0
        self.Y = 0
        

    def updatePieceSurface(self, win):
        x , y = self.X, self.Y

        piece = self.piece
        sq_size = 48
        sq_size_ = sq_size + 3
        surface = pygame.Surface((len(piece[0]) * sq_size_ , len(piece) * sq_size_), pygame.SRCALPHA)
            
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                    pos = j * sq_size_ ,  (i * sq_size_)
                    if piece[i][j]:
                            path = os.path.join('assets/images/block.png')
                            img = pygame.image.load(path)
                            img = pygame.transform.smoothscale(img,(sq_size,sq_size))

                            surface.blit(img , (pos[0],pos[1]))
                        
        img=img.get_rect(center=(x,y))
        win.blit(surface, img)
        
    def updatePos(self, pos):
        self.X, self.Y = pos 

    def save_initial(self, pos):
        self.row = pos[1] 
        self.col = pos[0] 

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True


    def undrag_piece(self):
        self.piece = None
        self.dragging = False
