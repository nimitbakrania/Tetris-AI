from board import Direction, Rotation, Block, Shape
from random import Random
import random

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        countHoles(self, board)
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])
                    
numInColumn = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
maxColumnHeights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def findMaxColumnHeights(self, board):
    for x in range(0, board.width):
        for y in range(board.height, 0, -1):
            if (x, y) in board.cells:
                maxColumnHeights[x] = board.height - y

def findMaxInThisColumn(self, board, column):
    return maxColumnHeights[column - 1]

aggregateHeight = 0
def calculateAggregateHeight(self, board):
    global aggregateHeight
    findMaxColumnHeights(self, board)
    aggregateHeight = 0
    for eachMax in maxColumnHeights:
        aggregateHeight += eachMax
    #print("Aggregate height: " + str(aggregateHeight))

prevScore = 0

def changeInScore(self, board):
    global prevScore
    newScore = board.score
    changeInScore.scoreChange = newScore - prevScore
    #print("Previous score: " + str(prevScore))
    #print("New score: " + str(newScore))
    #print("Change in score: " + str(changeInScore.scoreChange))

def resetPrevScore(self, board):
    global prevScore
    prevScore = board.score

bumpiness = 0
def calculateBumpiness(self, board):
    global bumpiness
    bumpiness = 0
    findMaxColumnHeights(self, board)
    #print(maxColumnHeights)
    count = 0
    for eachValue in range(0, 9):
        bumpiness += abs(maxColumnHeights[count] - maxColumnHeights [count + 1])
        count += 1
    #print("Bumpiness: " + str(bumpiness))

aiScore = 0
holeCountWeight = -0.6382#0 - random.uniform(0, 1)
bumpinessWeight = -0.2632#0 - random.uniform(0, 1)
aggregateHeightWeight = -0.7383#0 - random.uniform(0, 1)
scoreDiffWeight = 0.1192#random.uniform(0, 1)
def getDecisionScore(self, holeCount, bumpiness, aggregateHeight, scoreDiff):
    global aiScore, holeCountWeight, bumpinessWeight, aggregateHeightWeight, scoreDiffWeight
    #print("\n\nHole weight = " + str(holeCountWeight) + "\nBumpiness Weight = " + str(bumpinessWeight) + "\nAggregate Weight = " + str(aggregateHeightWeight) + "\nScore Weight = " + str(scoreDiffWeight))
    aiScore = (holeCount * holeCountWeight) + (bumpiness * bumpinessWeight) + (aggregateHeight * aggregateHeightWeight) + (scoreDiff * scoreDiffWeight)
    return aiScore

holes = 0
def countHoles(self, board):
    global holes
    holes = 0
    for each in board.cells:
        keepGoing = 1
        count = 1
        while keepGoing == 1:
            if ((each[0], each[1] + count) in board.cells) or (count + each[1] == 24):
                keepGoing = 0
            else:
                holes += 1
                count += 1
    #print("Holes: " + str(holes))

class Attempt3(Player):
    global holes
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.rot = 0

    def choose_action(self, board):
        print("calling choose action")
        bestScore = -9999999
        resetPrevScore(self, board)
        for i in range(-5, 15):
            for j in range(0, 4):
                #print("\npos = " + str(i) + " and rot = " + str(j))
                sandbox = board.clone()
                for k in range(0, j):
                    try:
                        sandbox.rotate(Rotation.Clockwise)
                    except:
                        pass
                left = board.falling.left
                while left != i:
                    if i < left:
                        left -= 1
                        try:
                            sandbox.move(Direction.Left)
                        except:
                            pass
                    elif i > left:
                        left += 1
                        try:
                            sandbox.move(Direction.Right)
                        except:
                            print("passed right")
                            pass
                try:
                    sandbox.move(Direction.Drop)
                except:
                    pass

                countHoles(self, sandbox)
                calculateBumpiness(self, sandbox)
                calculateAggregateHeight(self, sandbox)
                changeInScore(self, sandbox)
                getDecisionScore(self, holes, bumpiness, aggregateHeight, changeInScore.scoreChange)
                #print("Decision score: " + str(aiScore))
                
                if aiScore > bestScore:
                    #print(str(aiScore) + " is greater than " + str(bestScore))
                    #print("best ai score is now " + str(aiScore))
                    bestScore = aiScore
                    bestRotation = j
                    bestPosition = i

        #print("Best pos: " + str(bestPosition) + " and Best rot: " + str(bestRotation) + " with aiScore = " + str(bestScore))
        returnList = []
        for a in range(0, bestRotation):
            returnList.append(Rotation.Clockwise)
        
        left = board.falling.left
        #print("BOARDFALLINGKEFT" + str(board.falling.left))
        while left != bestPosition:
            #print("LEFT = " + str(board.falling.left) + " AND BEST POSITION = " + str(bestPosition))
            if bestPosition < left:
                left -= 1
                print("left")
                returnList.append(Direction.Left)
            elif bestPosition > left:
                left += 1
                print("right")
                returnList.append(Direction.Right)
        
        returnList.append(Direction.Drop)
        return returnList

SelectedPlayer = Attempt3
