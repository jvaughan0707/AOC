from shared.utils import getInput, directions, isOob, add, dot, getMinDist

lines = getInput(17)
minStraight = 4 # set to 1 for part 1
maxStraight = 10

adjacencyMatrix = {'s':{}, 'e': {}}

class Point:
    def __init__(self, pos, value):
        self.nodes = {}
        self.pos = pos
        self.value = value

        for d in directions.values():
            self.nodes[d] = []
            for l in range(0, maxStraight):
                key = getKey(self.pos, l, d)
                self.nodes[d].append(key)
                adjacencyMatrix[key] = {}

def getKey(pos, level, direction):
    return f'{pos}/{level}/{direction}'

width = len(lines[0])
height = len(lines)

def addNeighbour(source, target, dist):
    adjacencyMatrix[source][target] = dist

points = {}
for i in range(0, height):
    for j in range(0, width):
        points[(i,j)] = Point((i, j), int(lines[i][j]))

for i in range(0, height):
    for j in range(0, width):
        point = points[(i,j)]

        for d in directions.values():
            # connect each level to the one above (0 distance)
            for l in range(minStraight - 1, maxStraight):
                for l2 in range(l + 1, maxStraight):
                    addNeighbour(point.nodes[d][l], point.nodes[d][l2], 0)

            if not isOob(lines, add((i,j), d)):
                nextPoint = points[add((i, j), d)]
                # continuing in same direction
                for l in range(0, maxStraight - 1):
                    nextNode = nextPoint.nodes[d][l + 1]
                    addNeighbour(point.nodes[d][l], nextNode, nextPoint.value)

                # change in direction
                for d2 in directions.values():
                    if dot(d, d2) == 0:
                        for l in range(minStraight -1, maxStraight):
                            addNeighbour(point.nodes[d2][l], nextPoint.nodes[d][0], nextPoint.value)

addNeighbour('s', points[(0,1)].nodes[(0,1)][0], points[(0,1)].value)
addNeighbour('s', points[(1,0)].nodes[(1,0)][0], points[(1,0)].value)

endPoint = points[(height - 1, width - 1)]

for d in directions.values():
    for l in range(0, maxStraight):
        addNeighbour(endPoint.nodes[d][l], 'e', 0)

# distMap = getMinDist(adjacencyMatrix, 's', 'e')
#
# for i in range(0, height):
#     row = ''
#     for j in range(0, width):
#         point = points[(i,j)]
#         nodes = [x for y in point.nodes.values() for x in y ]
#
#         minDist = min(nodes, key=distMap.get)
#         row += f'{distMap[minDist]} '
#     print(row)
#
# for x in points[(1,1)].nodes.values():
#     for y in x:
#         print(y, distMap[y])

print(getMinDist(adjacencyMatrix, 's', 'e'))
