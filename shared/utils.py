from copy import deepcopy

def normalise(x):
    return 1 if x > 0 else 0 if x == 0 else -1

def expandWithPlaceholders(values, expandFunc, iterations, sizeFunc=None, addSizeFunc=None):
    # dictionary with keys which are possible item values. Dictionary values are arrays of sizes at increasing depths
    # First element in the array is the size of the item with no expansions, second is size after 1 expansion...
    expansionMap = {}

    # for a given item, what is the "size"?
    # Defaults to the length of the item, but other common use cases are returning 1 for all items when we only care about the count,
    # or returning something else entirely (e.g. frequency map)
    if sizeFunc is None:
        sizeFunc = lambda x: len(x)

    # for a current total "size" and a new item's "size", return the result of combining them
    if addSizeFunc is None:
        addSizeFunc = lambda current, new: current + new

    class Item:
        def __init__(self, value, parent=None):
            self.value = value
            self.parent = parent

        def __repr__(self):
            return str(self.value)

        def updateParents(self, depth=2):
            current = self.parent

            while current.parent:
                parent = current.parent
                if len(expansionMap[parent.value]) < depth + 1:
                    expansionMap[parent.value].append(0)
                expansionMap[parent.value][depth] = addSizeFunc(expansionMap[parent.value][depth], self.getSize())
                depth += 1
                current = parent

        def getSize(self):
            return sizeFunc(self.value)

    class Placeholder(Item):
        def __init__(self, value, parent, count):
            super().__init__(value, parent)
            self.count = count

        def __repr__(self):
            return f'({self.value})*{self.count}'

        def updateParents(self):
            super().updateParents(1 + self.count)

        def getSize(self):
            return expansionMap[self.value][self.count]

    items = []

    for v in values:
        items.append(Item(v))

    def recurse(currentItems, i=1):
        newItems = []
        totalLength = 0
        for item in currentItems:
            if type(item) is Placeholder:
                item.count += 1
                newItems.append(item)
            elif item.value in expansionMap:
                newItems.append(Placeholder(item.value, item, 1))
            else:
                expanded = expandFunc(item.value)
                expandedLength = 0
                for newItem in expanded:
                    newItems.append(Item(newItem, item))
                    expandedLength = addSizeFunc(expandedLength, sizeFunc(newItem))
                expansionMap[item.value] = [sizeFunc(item.value), expandedLength]

        for item in newItems:
            item.updateParents()
            totalLength = addSizeFunc(totalLength, item.getSize())

        # print('newItems:', newItems, 'length:', totalLength, 'map:', expansionMap)

        i += 1
        if i > iterations:
            return totalLength
        else:
            return recurse(newItems, i)

    return recurse(items)

def flipGrid(grid):
    newRows = []

    isStr = type(grid[0]) == str

    for j in range(len(grid[0])):
        newRow = []
        for i in range(len(grid)):
            newRow.append(grid[i][j])

        if isStr:
            newRows.append(''.join(newRow))
        else:
            newRows.append(newRow)
    return newRows

def sub(p1, p2):
    return tuple(p1[i] - p2[i] for i in range(len(p1)))

def add(p1, p2):
    return tuple(p1[i] + p2[i] for i in range(len(p1)))

def scale(p, s):
    return tuple(p[i] * s for i in range(len(p)))

def dot(p1, p2):
    return sum(p1[i] * p2[i] for i in range(len(p1)))

def isOob(grid, p):
    return not (0 <= p[0] < len(grid) and 0 <= p[1] < len(grid[0]))

def get(grid, p):
    if isOob(grid, p):
        return None
    return grid[p[0]][p[1]]

def isCollinear(p1, p2):
    return p1[1]*p2[2] == p1[2]*p2[1] and p1[0]*p2[2] == p1[2]*p2[0] and p1[0]*p2[1] == p1[1]*p2[0]

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
directions = {
    'u': up,
    'r': right,
    'd': down,
    'l': left,
}

compassDirections = {
    'N': up,
    'E': right,
    'S': down,
    'W': left,
}

arrowDirections = {
    '^': up,
    '>': right,
    '<': left,
    'v': down,
}

def getInput(day):
    with open(f'inputs/{day}') as f:
        return f.read().splitlines()


def getGridInput(day):
    lines = getInput(day)

    grid = []
    for line in lines:
        grid.append(list(line))

    return grid

def getNumbersGridInput(day):
    grid = getGridInput(day)

    return [list(map(int, row)) for row in grid]

def getSectionsInput(day):
    with open(f'inputs/{day}') as f:
        sections = f.read().split('\n\n')

        return list(map(lambda x: x.split('\n'), sections))

def getFirstInGrid(grid, char):
    width = len(grid[0])
    height = len(grid)

    for i in range(height):
        for j in range(width):
            if grid[i][j] == char:
                return i, j


def getMinDist(adjacencyMatrix, start, end, weighted=True, distMap = None):
    if distMap is None:
        distMap = {x: float('inf') for x in adjacencyMatrix}
    else:
        for x in adjacencyMatrix:
            distMap[x] = float('inf')

    exploredNodes = set()
    explorableNodes = {start}
    distMap[start] = 0

    while True:
        minUnexploredNode = min(explorableNodes, key=distMap.get)

        if minUnexploredNode == end:
            break
        dist = distMap[minUnexploredNode]
        explorableNodes.remove(minUnexploredNode)
        exploredNodes.add(minUnexploredNode)

        neighbours = adjacencyMatrix[minUnexploredNode]
        for neighbour in neighbours:
            nDist = neighbours[neighbour] if weighted else 1
            if neighbour in exploredNodes:
                continue

            distMap[neighbour] = min(dist + nDist, distMap[neighbour])

            # if nDist > 0:
            explorableNodes.add(neighbour)

    # print(distMap)
    return distMap[end]

def getMinDistDynamic(adjacencyMatrix, start, end, weightFunc):
    distMap = {x: float('inf') for x in adjacencyMatrix}

    exploredNodes = set()
    explorableNodes = {start}
    distMap[start] = 0

    while True:
        minUnexploredNode = min(explorableNodes, key=distMap.get)

        if minUnexploredNode == end:
            break
        dist = distMap[minUnexploredNode]
        explorableNodes.remove(minUnexploredNode)
        exploredNodes.add(minUnexploredNode)

        neighbours = adjacencyMatrix[minUnexploredNode]
        for neighbour in neighbours:
            if neighbour in exploredNodes:
                continue
            nDist = weightFunc(minUnexploredNode, neighbour, dist)
            distMap[neighbour] = min(dist + nDist, distMap[neighbour])
            explorableNodes.add(neighbour)
            print(distMap)

    print(distMap)
    return distMap[end]

def visualiseGraph(adjacencyMatrix, directed=False, weighted=False, colorMap=None, name='graph'):
    from pyvis.network import Network
    import os
    import webbrowser

    net = Network('1500px', '1500px', directed=directed)

    for k in adjacencyMatrix.keys():
        color = 'black'
        if colorMap:
            color = colorMap(k)
        net.add_node(str(k), color=color)

    for source, targets in adjacencyMatrix.items():
        for target in targets:
            if weighted:
                net.add_edge(str(source), str(target[0]), color='black', label=str(target[1]))
            else:
                net.add_edge(str(source), str(target), color='black')

    net.show_buttons(filter_=['physics'])
    name = name + '.html'
    net.show(name, notebook=False)
    webbrowser.open('file://' + os.path.realpath(name))

def getNetwork(grid, adjFunc=None, wallSymbols='#'):
    nodes = {}
    height = len(grid)
    for i in range(height):
        for j in range(len(grid[i])):
            current = grid[i][j]
            if current in wallSymbols:
                continue
            nodes[(i, j)] = []
            for direction in directions:
                neighbourPoint = add((i, j), directions[direction])
                neighbourSymbol = get(grid, neighbourPoint)
                if not neighbourSymbol or neighbourSymbol in wallSymbols:
                    continue
                if not adjFunc or adjFunc(current, neighbourSymbol, direction):
                    nodes[(i, j)].append(neighbourPoint)
    return nodes

def getPathDfs(adjMap, start, end, currentPath=None):
    if currentPath is None:
        currentPath = [start]
    if end in adjMap[start]:
        currentPath.append(end)
        return currentPath
    for neighbour in adjMap[start]:
        if neighbour not in currentPath:
            path = getPathDfs(adjMap, neighbour, end, currentPath + [neighbour])

            if path:
                return path

    return None

def getPathBfs(adjMap, start, end):
    nodeDists = { 0: [start]}
    visited = {start}
    while True:
        maxDist = max(nodeDists.keys())
        nodeDists[maxDist + 1] = []

        if end in nodeDists[maxDist]:
            break
        for node in nodeDists[maxDist]:
            for neighbour in adjMap[node]:
                if neighbour not in visited:
                    nodeDists[maxDist + 1].append(neighbour)
                    visited.add(neighbour)

        if not nodeDists[maxDist + 1]:
            return None

    dist = maxDist - 1
    current = end
    path = [end]

    while dist >= 0:
        for neighbour in nodeDists[dist]:
            if current in adjMap[neighbour]:
                path.append(neighbour)
                current = neighbour
                dist -= 1
                break

    path.reverse()
    return path

def getConnectedPoints(adjMap, start, currentSet = None):
    if currentSet is None:
        currentSet = set()
    for neighbour in adjMap[start]:
        if neighbour not in currentSet:
            currentSet.add(neighbour)
            getConnectedPoints(adjMap, neighbour, currentSet)

    return currentSet

def getMinCuts(adjMap, s, t, upperLimit):
    cuts = 0

    adjMapCopy = deepcopy(adjMap)

    while cuts <= upperLimit:
        path = getPathBfs(adjMapCopy, s, t)

        if not path:
            break

        cuts += 1

        for i in range(len(path) - 1):
            n1 = path[i]
            n2 = path[i + 1]
            adjMapCopy[n1].remove(n2)

    if cuts > upperLimit:
        return None

    S = getConnectedPoints(adjMapCopy, s)

    cutEdges = []

    for x in adjMap:
        for y in adjMap[x]:
            if x in S and y not in S:
                cutEdges.append((x, y))

    return cutEdges

def getGlobalMinCuts(adjMap, upperLimit):
    for n1 in adjMap:
        for n2 in adjMap:
            if n1 == n2:
                continue

            if n1 in adjMap[n2]:
                continue

            minCuts = getMinCuts(adjMap, n1, n2, upperLimit)

            if minCuts:
                return minCuts

    return None

def getNumbers(text):
    import re
    m = re.findall(r'-?\d+', text)

    return list(map(int, m))

class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.neighbours = {}

    def addNeighbour(self, neighbour, direction):
        self.neighbours[direction] = neighbour

    def __repr__(self):
        return str(self.position)

def getGridPoints(grid, diagonal = False):
    points = {}
    height = len(grid)
    width = len(grid[0])
    for i in range(height):
        for j in range(width):
            value = grid[i][j]
            points[(i,j)] = Point((i, j), value)

    for i in range(height):
        for j in range(width):
            p1 = points[(i,j)]
            for d in directions:
                p2 = add((i, j), directions[d])
                if not isOob(grid, p2):
                    p1.addNeighbour(points[p2], d)

            if diagonal:
                for d in directions:
                    i2, j2 = directions[d]
                    i2, j2 = i2 + j2, j2 - i2
                    p2 = add((i, j), (i2, j2))
                    if not isOob(grid, p2):
                        p1.addNeighbour(points[p2], d + '+')

    return points

def formatText(text, colour = '', style = ''):
    colourMap = {
        'pink': '\033[95m' ,
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'green': '\033[92m',
        'orange': '\033[93m',
        'red': '\033[91m'
    }

    styleMap = {
        'b': '\033[1m',
        'u': '\033[4m'
    }

    endSequence = '\033[0m'
    output = text
    if colour:
        output = colourMap[colour] + output + endSequence

    if style:
        output = styleMap[style] + output + endSequence

    return output

def triangle(n):
    return n * (n + 1) // 2

def condense(coordValues, includeMiddles = True):
    dimensions = len(coordValues)

    coordMap = [
        {} for i in range(dimensions)
    ]

    widthMap = [
        {} for i in range(dimensions)
    ]

    for values in coordValues:
        values.sort()

    for d in range(dimensions):
        m = widthMap[d]

        current = 0

        for i, v in enumerate(coordValues[d]):
            coordMap[d][v] = current
            m[current] = 1

            current += 1
            if includeMiddles:

                if i > 0 and coordValues[d][i - 1] < v - 1:
                    m[current] =  v - coordValues[d][i - 1] - 1
                    current += 1
            elif i > 0:
                m[current] = v - coordValues[d][i - 1]

    return coordMap, widthMap