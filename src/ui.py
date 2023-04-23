
import pygame
import os
import json
from drag import Dragger


def openfile(file):
    with open(file) as f:
        data = json.load(f)
    return data

def savefile(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

class Ui:

    def __init__(self):              
        self.dragger = Dragger()
        
        self.hoverPos = None

    def show_board(self , win, boardSurface):
        
        win.fill((173, 216, 230))
        x , y = 200,100
        path = os.path.join('assets/images/board.png')
        img = pygame.image.load(path)
        
        win.blit(img, (x,y))
        
        win.blit(boardSurface , (200, 100, 540, 540) )



    def drawPiece(self, surface , pos, size=None ):
        path = os.path.join('assets/images/block.png')
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.smoothscale(img,(size,size))

        surface.blit(img , (pos[0], pos[1]))


    def getSurfaces(self, pieces):
        s = []
        sq_size = 35
        y =  100 + sq_size
        for p in range(len(pieces)):
            
            surface = pygame.Surface((len(pieces[p][0]) * sq_size , len(pieces[p]) * sq_size), pygame.SRCALPHA)
            
            s.append((pieces[p], surface, y))
            y += (sq_size) + (sq_size * len(pieces[p]))
            

        return s

        

    def show_pieces(self, win, pieces):
        

        sq_size = 35
        x , y = 800 , 135
        dragger = self.dragger
        
        sq_size_ = sq_size + 3

        for piece in pieces :
            try :
                if dragger.piece == piece:
                    y += (sq_size) + (sq_size * len(piece))
                    continue
            except :
                pass
            
            surface = pygame.Surface((len(piece[0]) * sq_size_ + 2 ,  2 + len(piece) * sq_size_), pygame.SRCALPHA)
            
            for i in range(len(piece)):
                for j in range(len(piece[0])):
                    
                    p_x, p_y = (j * sq_size_ ), (i * sq_size_)
                    if piece[i][j]:
                        self.drawPiece(surface , (p_x,p_y), sq_size)
                        
            win.blit(surface, (x,y))
            y += (sq_size) + (sq_size_ * len(piece))

    def hover(self, win):
        if self.hoverPos == None :
            return
        
        surface = pygame.Surface((540,540), pygame.SRCALPHA)
        
        pos = self.hoverPos
        piece = self.dragger.piece
        sq_size = 60
        color = 'cadetblue4'
        width = 2
        
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] :
                    x , y = width + ((pos[0] + j) * sq_size) , width + ((pos[1] + i) * sq_size)
                    rect = (x, y, sq_size - 2, sq_size - 2)
                    pygame.draw.rect(surface, color, rect)
        win.blit(surface, (200, 100))


    def display_score(self, score, win):
        x = 640
        gap = 16
        x -= gap * len(str(score))
        pos = (x, 60)
        font = pygame.font.SysFont("Urban Defender Semi-Italic", 35)
        text = f"Score : {score}"
        text = font.render(text, True, "#676668")
        win.blit(text, pos)

        data = openfile('score.json')
        high_score = data['high_score']
        x = 610
        gap = 16
        x -= gap * len(str(high_score))
        pos = (x, 30)
        font = pygame.font.SysFont("Urban Defender Semi-Italic", 28)
        text = f"High Score : {high_score}"
        text = font.render(text, True, "#595563")
        win.blit(text, pos)
        


    def show_menu(self, win, text = "Menu"):
        surface = pygame.Surface((1130, 700), pygame.SRCALPHA)

        gray_color = "#676668"
        surface.fill(gray_color)

        alpha = 135
        surface.set_alpha(alpha)

        font = pygame.font.SysFont("Urban Defender Semi-Italic", 45)
        f = pygame.font.SysFont("Urban Defender Semi-Italic", 60)

        text = f.render(text, True, (245, 0, 0))
        pos = text.get_rect()
        pos.center = (565, 250)

        win.blit(text, pos)
        
        info_text =  "Enter `esc` to quit the game"
        info_text = font.render(info_text, True, "#FFFFFF")
        info_pos = info_text.get_rect()
        info_pos.center = (565, 350)
        win.blit(info_text, info_pos)

        info_text_1 =  "Enter `r` to restart the game"
        info_text_1 = font.render(info_text_1, True, "#FFFFFF")
        info_pos_1 = info_text_1.get_rect()
        info_pos_1.center = (565, 450)

        win.blit(info_text_1, info_pos_1)
        win.blit(surface, (0, 0))
    

