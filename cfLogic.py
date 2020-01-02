import chip
from chip import *
from random import randrange
class ConnectFour:

    def __init__(self):
        self.board = [[Chip('.') for c in range(7)] for r in range(6)]

    #determines if coordinates are within the board
    def isValid(self,row,col):
        if(row>=0 and col>=0):
            if(row<6 and col<7):
                return True
        return False

    def addPiece(self, chip, slot):
        for i in range(len(self.board)):
            row = len(self.board)-i-1
            if(self.board[row][slot].team=='.'):
                self.board[row][slot] = chip
                chip.row = row
                chip.col = slot
                return True
        return False

    def printBoard(self):
        for x in range(len(self.board)):
            print('|',end=' ')
            for y in range(len(self.board[x])):
                print(self.board[x][y], end=' | ')
            print('','\n')

    def getPossibleMoves(self):
        lst = []
        for slot in range(len(self.board[0])):
            if(self.board[0][slot].team=='.'):
                lst.append(slot)
        return lst

    #checks most recent placement of a chip to see if it won the game
    #returns a tuple of (True,spots) if a team won and (False,[]) if not
    def checkForWin(self,chip):    
        t = chip.team      
        
        spots = []
        spots.append(chip)

        #checking top & bottom  
        r = chip.row
        c = chip.col      
        count = 1
        while(self.isValid(r+1,c) and self.board[r+1][c].team == t):
            count += 1
            r = r + 1
            c = c
            spots.append(self.board[r][c])   
        r = chip.row
        c = chip.col
        while(self.isValid(r-1,c) and self.board[r-1][c].team == t):
            count += 1
            r = r - 1
            c = c
            spots.append(self.board[r][c])

        if(count>=4):
            return (True,spots)

        #checking left & right
        count = 1
        del spots[1:]
        r = chip.row
        c = chip.col
        while(self.isValid(r,c+1) and self.board[r][c+1].team == t):
            count += 1
            r = r
            c = c + 1
            spots.append(self.board[r][c])
        r = chip.row
        c = chip.col
        while(self.isValid(r,c-1) and self.board[r][c-1].team == t):
            count += 1
            r = r
            c = c - 1
            spots.append(self.board[r][c])

        if(count>=4):
            return (True,spots)
        

        #checking TopLeft & BotRight
        count = 1
        del spots[1:]
        r = chip.row
        c = chip.col
        while(self.isValid(r-1,c-1) and self.board[r-1][c-1].team == t):
            count += 1
            r = r - 1
            c = c - 1
            spots.append(self.board[r][c])
        r = chip.row
        c = chip.col
        while(self.isValid(r+1,c+1) and self.board[r+1][c+1].team == t):
            count += 1
            r = r + 1
            c = c + 1
            spots.append(self.board[r][c])

        if(count>=4):
            return (True,spots)

        #checking TopRight & BotLeft
        count = 1
        del spots[1:]
        r = chip.row
        c = chip.col
        while(self.isValid(r+1,c-1) and self.board[r+1][c-1].team == t):
            count += 1
            r = r + 1
            c = c - 1
            spots.append(self.board[r][c])
        r = chip.row
        c = chip.col
        while(self.isValid(r-1,c+1) and self.board[r-1][c+1].team == t):
            count += 1
            r = r - 1
            c = c + 1
            spots.append(self.board[r][c])

        if(count>=4):
            return (True,spots)
        
        return (False,[])

#generates a random slot from 0-6 accounting for filled slots
#returns -1 if the whole board is filled
def chooseRandSlot(cf,team):
    lst = cf.getPossibleMoves()
    if len(lst)==0:
        return -1
    return lst[randrange(len(lst))]


def printSpotPositions(spots):
    for spot in spots:
        print("(%d,%d)" % (spot.row,spot.col), end=' ')
    print()
    