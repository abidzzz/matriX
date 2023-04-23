import numpy
import random

piece_small = [
    
        [[1]]
    ,
    
        [[1, 1]]
    ,
    
        [[1, 0],
        [1, 1]]
    ,
    
        [[1, 0],
         [0, 1]]
    
]

piece_medium = [
    
        [[1, 1, 1]]
    ,
    
        [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]
    ,
    
        [[1, 1, 1],
         [0, 0, 1] ,
         [0, 0, 1]]
    ,
    
        [[1, 1, 1],
         [1, 0, 1]]
    ,
    
        [[0, 1, 1],
         [1, 1, 0]]
    ,
        [[0, 1, 1],
         [1, 1, 0]]
    ,
    
    
        [[1, 0, 0],
         [1, 1, 1]]
    ,
    
        [[1, 1],
         [1, 1]]
    ,
    
        [[0, 1, 0],
         [1, 1, 1] ,
         [0, 1, 0]]
]

piece_large = [
    
        [[1, 1, 1, 1]]
    ,
    
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]
    ,
    
        [[1, 1, 1, 1, 1]]
    ,
    
        [[1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1]]
    
]


all_pieces = [piece_small, piece_medium, piece_large]

class Piece:

    def __init__(self):
        self.rect = (800, 100, 300, 540) 
        self.piece_sizes = {"small": 10, "medium": 15, "large": 3}
        

    def get_piece_probabilities(self):
        total_pieces = sum(self.piece_sizes.values())

        if total_pieces == 0:
            return [35, 40 , 25]
        
        piece_probabilities = [
            round(self.piece_sizes["small"] / total_pieces, 2) * 100,
            round(self.piece_sizes["medium"] / total_pieces, 2)* 100,
            round(self.piece_sizes["large"] / total_pieces, 2)* 100
        ]

        return piece_probabilities

            
  
    def getPieceProbablilty(self):

        s = len(all_pieces[0])
        m = len(all_pieces[1])
        l= len(all_pieces[2])
        total = s+m+l
        p = [(s / total) * 100, (m / total) * 100, (l / total) * 100]
        if self.piece_sizes["small"]:
            p[0] = ((s - self.piece_sizes["small"]) / (total - 3)) * 100
        if self.piece_sizes["medium"]:
            p[1] = ((m - self.piece_sizes["medium"]) / (total - 3)) * 100
        if self.piece_sizes["large"]:
            p[2] = ((l - self.piece_sizes["large"]) / (total - 3)) * 100

        
        return p

    def rotate(self, piece):
        num=random.randint(0,2)
        piece=numpy.array(piece)
    
        if num==0:
            return numpy.fliplr(piece)
        elif num==1:
            return numpy.flipud(piece)
        elif num==2:
            return piece.T

    def getRandomPiece(self):
        p = []
        piece_probabilities = self.get_piece_probabilities()
        # print(piece_probabilities)
        for i in range(3):
            choice = random.choices(all_pieces, weights=piece_probabilities)

            randomPiece = random.choice(choice[0])


            x = self.rotate(randomPiece)
            if x.tolist() in p:
                randomPiece = random.choice(choice[0])
            p.append(x.tolist())
            
            if randomPiece in piece_small:
                self.piece_sizes["small"] += 1
            elif randomPiece in piece_medium:
                self.piece_sizes["medium"] += 1
            elif randomPiece in piece_large:
                self.piece_sizes["large"] += 1
        return p

