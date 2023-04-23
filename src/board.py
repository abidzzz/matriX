import pygame
import numpy
import os 
import json 

def openfile(file):
    with open(file) as f:
        data = json.load(f)
    return data

def savefile(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

class Board:

    def __init__(self):
        self.board = numpy.array([[0 for i in range(9)] for i in range(9)])
        self.rect = (200, 100, 540, 540)
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.score = 0
        self.consequtive = 0        


    
    def gameOver(self, pieces):
        av_sq = self.getAvailableSquares()
        num = 0

        for piece in pieces :
            for i in av_sq :
                if self.isValid(i, piece) :
                    break
            else:
                num += 1
                

        if num == len(pieces) and num != 0 :
            return True
        else :
            return False
            
    def getSurface(self, pos , surfaces):
        x, y = pos
        surface_x = 800
        sq_size = 45
        piece_surfaces = surfaces
        for piece, surface, surface_y in piece_surfaces:
            
            if surface_x <= x <= surface_x + surface.get_width() and surface_y <= y <= surface_y + surface.get_height():
                piece_x = (x - surface_x) // sq_size
                piece_y = (y - surface_y) // sq_size
                
                return True, piece, piece_x, piece_y
        return False, None, None, None 
        
                  
    def getPos(self,pos):
        self.sq_size = 60
        x = pos[0]
        y = pos[1]
        if self.rect[0] < x < self.rect[0] + self.rect[2]:
            if self.rect[1] < y < self.rect[1] + self.rect[3]:
                X = x - self.rect[0]
                Y = y - self.rect[1]
                i = int(X / (self.sq_size))
                j = int(Y / (self.sq_size))
                return i, j

        return None


    def getAvailableSquares(self):
        pos=[]
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    pos.append((i,j))
        return pos
    

    def makeSurface(self):
        new = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)

        sq_size = 60
        width = 2
        path = os.path.join('assets/images/block.png')
        img = pygame.image.load(path) 

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col]:
                    x , y = width + (col * sq_size) , width + (row * sq_size)
                    new.blit(img, (x, y))

        
        return new
    
    def clearTables(self, name, value, win):
        if name=="row":
            for col in range(len(self.board)):
                self.board[value][col] = 0

            self.score += 10 + (10 * self.consequtive)
                
        elif name=="col":
            for row in range(len(self.board)):
                self.board[row][value] = 0

            self.score += 10 + (10 * self.consequtive)

        else:
            for i in range(3):
                for j in range(3):
                    row = value[0] + i
                    col = value[1] + j
                    self.board[row][col] = 0

            self.score += 15 + (10 * self.consequtive)

        
        new = self.makeSurface()
        self.surface = new
        win.blit(self.surface , (200, 100, 540, 540) )
                    
                    
    def checkBoard(self, win):
        """Check all the rows , columns and 3x3 and clear if filled"""
        
        _3x3 = self.board.reshape(3,3,3,3).swapaxes(1,2).reshape(9,9)
        
        pos = [(i,j) for i in range(0,9,3) for j in range(0,9,3)]
        score = self.score 
        for i in range(len(self.board)):
            if sum(self.board[i]) == 9:
                self.clearTables('row',i,win)

            if sum(self.board[:,i]) == 9:
                self.clearTables('col',i, win)

            if sum(_3x3[i]) == 9:
                self.clearTables('3x3',pos[i],win)
        
        if self.score > score :
            self.consequtive += 1
            
        else :
            self.consequtive = 0

        data = openfile('score.json')
        high_score = data['high_score']
        # print(high_score,self.score)
        if self.score > high_score :
            data['high_score'] = int(self.score)
            savefile(data, 'score.json')

    
    def isValid(self, pos, piece):
       
        x, y = pos
        
        for i in range(len(piece)) :
            for j in range(len(piece[i])):
                
                try:
                    if piece[i][j] and self.board[y+i][x+j] :    
                        return False
                except:
                    return False

        return True 
            

    def placePiece(self, pos, piece, win):

        sq_size = 60
        width = 2
        path = os.path.join('assets/images/block.png')
        img = pygame.image.load(path)

        for i in range(len(piece)):
            for j in range(len(piece[0])):
                x , y = pos[0] + i , pos[1] + j

                if piece[i][j]:
                    self.board[pos[1]+i][pos[0]+j] = 1
                    x , y = width + ((pos[0] + j) * sq_size) , width + ((pos[1] + i) * sq_size)

                    self.surface.blit(img,(x, y))

        
        win.blit(self.surface, self.rect)
        self.score += numpy.sum(piece)
        self.checkBoard(win)

    def animate(self, win):
        for i in range(18):
            self.reset(win)
            z=i+1
            if i>=9:
                z=8-(i-9)

            bruh=8

            for x in range(z):
                
                if i>8:
                    y=i-8+x
                    self.placePiece((y,bruh),[[1]],win)
                    bruh-=1
                else:
                    self.placePiece((x, i),[[1]],win)
                    i-=1
            pygame.display.update()
            pygame.time.wait(20)
        self.reset(win)
        
    def reset(self, win):
        self.score = 0
        self.board = numpy.array([[0 for i in range(9)] for i in range(9)])
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        
        win.fill((173, 216, 230))

        x , y = 200,100
        path = os.path.join('assets/images/board.png')
        img = pygame.image.load(path)
        win.blit(img, (x,y))
        


        
        
        