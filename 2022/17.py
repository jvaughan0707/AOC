from shared.utils import getInput, up, down, left, right, add

directions = getInput(17)[0]

shapes = [
    [(0, i) for i in range(4)], #-
    [(1,0),(0,1),(1,1),(2,1),(1,2)], #+
    [(0,0),(0,1),(0,2),(1,2),(2,2)], # _|
    [(j,0) for j in range(4)], # |
    [(0,0),(0,1),(1,0),(1,1)], # ::
]

directionIndex = 0
shapeIndex = 0
width = 7
rocks = []
lockedPoints = {}
maxHeight = 0

shapePosCache = { }

class Rock:
    def __init__(self):
        global shapeIndex

        self.shape = shapes[shapeIndex]
        self.shapeIndex = shapeIndex
        self.height = max([y for y, x in self.shape]) + 1
        if len(rocks) > 0:
            self.pos = (maxHeight + 3, 2)
        else:
            self.pos = (3, 2)
        shapeIndex += 1
        shapeIndex %= len(shapes)

    def move(self, direction):
        newPos = add(self.pos, direction)

        for point in self.shape:
            pointPos = add(newPos, point)
            if pointPos in lockedPoints:
                return False
            if pointPos[0] < 0 or pointPos[1] < 0 or pointPos[1] >= width:
                return False
        self.pos = newPos
        return True

    def lock(self):
        global maxHeight
        for point in self.shape:
            pointPos = add(self.pos, point)
            lockedPoints[pointPos] = self.shapeIndex
            maxHeight = max(maxHeight, pointPos[0] + 1)

startCount = startHeight = endCount = endHeight = 0

def getHeight(numRocks):
    print('numRocks', numRocks)
    cycleLength = endCount - startCount
    cycleHeight = endHeight - startHeight
    print('cycleLength, cycleHeight', cycleLength, cycleHeight)

    cycles = (numRocks - startCount) // cycleLength
    remainder = (numRocks - startCount) % cycleLength

    print('cycles, remainder', cycles, remainder)

    print(shapePosCache.values())

    if remainder == 0:
        remainderHeight = 0
    else:
        remainderHeight = [x[1] for x in shapePosCache.values() if x[0] == remainder + startCount][0] - startHeight

    print('remainderHeight', remainderHeight)

    return startHeight + cycles * cycleHeight + remainderHeight

matchCounter = 0

while len(rocks) < 3000:
    rock = Rock()
    rocks.append(rock)

    while True:
        direction = left if directions[directionIndex] == '<' else right

        rock.move(direction)
        directionIndex += 1
        directionIndex %= len(directions)

        if not rock.move(up):
            rock.lock()
            break

    if (rock.pos[1], directionIndex, rock.shapeIndex) in shapePosCache:
        matchCounter += 1
        if matchCounter > 5:
            startCount, startHeight = shapePosCache[(rock.pos[1], directionIndex, rock.shapeIndex)]
            print('repeat')
            print('startCount, startHeight', startCount, startHeight)
            print('shapeIndex', rock.shapeIndex)
            print('rock pos', rock.pos)
            endCount = len(rocks)
            endHeight = maxHeight
            print('endCount, endHeight', endCount, endHeight)
            break
    else:
        shapePosCache[(rock.pos[1], directionIndex, rock.shapeIndex)] = (len(rocks), maxHeight)
        matchCounter = 0
        print('count, height', len(rocks), maxHeight)

# for i in reversed(range(2862, 2885)):
#     row = ''
#     for j in range(7):
#         if (i,j) in lockedPoints:
#             row += str(lockedPoints[(i,j)])
#         else:
#             row += '.'
#     print(row)
#
# print()

# for i in reversed(range(182, 205)):
#     row = ''
#     for j in range(7):
#         if (i,j) in lockedPoints:
#             row += str(lockedPoints[(i,j)])
#         else:
#             row += '.'
#     print(row)
print(getHeight(1000000000000))

