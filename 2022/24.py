import math

from AOC.shared.utils import getGridInput, arrowDirections, add, getNetwork, getMinDistDynamic

grid = getGridInput(24)

height = len(grid)
width = len(grid[0])

innerGrid = [r[1:-1] for r in grid[1:-1]]

innerWidth = width - 2
innerHeight = height - 2

class Blizzard:
    def __init__(self, startingPos, direction):
        self.pos = startingPos
        self.direction = direction

    def move(self):
        self.pos = add(self.pos, self.direction)
        self.pos = (self.pos[0] % innerHeight, self.pos[1] % innerWidth)

def getBlizzards():
    output = []
    for i in range(innerHeight):
        for j in range(innerWidth):
            symbol = innerGrid[i][j]
            if symbol == '.':
                continue
            output.append(Blizzard((i, j), arrowDirections[symbol]))

    return output

lcm = math.lcm(innerHeight, innerWidth)
blizzards = getBlizzards()
posAvailabilityMap = {(i,j): {} for i in range(innerHeight) for j in range(innerWidth)}

def getAvailabilityMap():
    for t in range(lcm):
        unavailablePoints = set()
        for b in blizzards:
            unavailablePoints.add(b.pos)

        for i in range(innerHeight):
            for j in range(innerWidth):
                posAvailabilityMap[(i, j)][t] = (i,j) not in unavailablePoints

        for b in blizzards:
            b.move()

getAvailabilityMap()

adjMap = getNetwork(innerGrid)

adjMap['s'] = [(0,0)]
adjMap[(0,0)].append('s')
adjMap[(innerHeight - 1, innerWidth - 1)].append('e')
adjMap['e'] = [(innerHeight - 1, innerWidth - 1)]


def getMinDist(start, end, startTime):
    distMap = { startTime: {start}}

    t = startTime
    while True:
        distMap[t + 1] = set()

        for n1 in distMap[t]:
            for n2 in adjMap[n1] + [n1]:
                if n2 == end:
                    return t + 1
                if n2 not in posAvailabilityMap or posAvailabilityMap[n2][(t + 1)%lcm]:
                    distMap[t + 1].add(n2)

        t += 1

d1 = getMinDist('s', 'e', 0)
d2 = getMinDist('e', 's', d1)
d3 = getMinDist('s', 'e', d2)

print(d3)
