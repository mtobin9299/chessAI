import chip
import cfLogic

from chip import *

allWinningLocations = [[0 for c in range(7)] for r in range(6)]

for i in range(100000):

    cf = cfLogic.ConnectFour()

    #cf.printBoard()
    cf.getPossibleMoves()

    flag = True
    gameOver = False

    winningSpots = []
    winningSpots.clear()
    while not gameOver:
        while(flag):
            #print("Red Turn")
            slot = cfLogic.chooseRandSlot(cf,'R')
            if slot == -1: #board is full
                gameOver = True
                winningSpots = []
                break
            inserted = Chip('R')
            if(cf.addPiece(inserted,slot)):
                #cf.printBoard()
                flag = False
                tup = cf.checkForWin(inserted)
                if(tup[0]):
                    winningSpots = tup[1]
                    gameOver = True
            #else:
                #print("filled, pick another")
        
        flag = True
        while(flag and not gameOver):
            #print("Yellow Turn")
            slot = cfLogic.chooseRandSlot(cf,'Y')
            if slot == -1: #board is full
                gameOver = True
                winningSpots = []
                break
            inserted = Chip('Y')
            if(cf.addPiece(inserted,slot)):            
                #cf.printBoard()
                flag = False
                tup = cf.checkForWin(inserted)
                if(tup[0]):
                    winningSpots = tup[1]
                    gameOver = True
            #else:
                #print("filled, pick another")
        flag = True
#     cf.printBoard()
#     print()
#     printSpotLocations(winningSpots)
    for spot in winningSpots:
        allWinningLocations[spot.row][spot.col] += 1
    if i % 10000 == 0:
        print(i/1000)

for x in range(len(allWinningLocations)):
        print('|',end=' ')
        for y in range(len(allWinningLocations[x])):
            print(allWinningLocations[x][y], end=' | ')
        print('','\n')
