from shared.utils import getGridInput, getNetwork, visualiseGraph

grid = getGridInput(23)

width = len(grid[0])
height = len(grid)

entrancePoint = (0, grid[0].index('.'))
exitPoint = (height - 1, grid[-1].index('.'))

# def getLongestPath():
def adjFunc(current, _, direction):
    if current == '.':
        return True
    m = {
        '^': 'u',
        'v': 'd',
        '<': 'l',
        '>': 'r'
    }
    if current in m and m[current] == direction:
        return True
    return False

# network = getNetwork(grid, adjFunc)
network = getNetwork(grid)
reducedNetwork = {entrancePoint: []}

visitedPoints = set()
def getNodes(start):
    current = start
    for firstPoint in network[current]:
        if firstPoint in visitedPoints:
            continue
        currentSegment = [start, firstPoint]
        current = firstPoint
        visitedPoints.add(current)
        while len(network[current]) <= 2:
            nextPoints = network[current]
            current = None
            for nextPoint in nextPoints:
                if nextPoint not in currentSegment:
                    current = nextPoint
                    break

            if current:
                currentSegment.append(current)
                visitedPoints.add(current)
            else:
                break

        end = currentSegment[-1]
        if end in reducedNetwork:
            reducedNetwork[end].append((start, len(currentSegment) - 1))
        else:
            reducedNetwork[end] = [(start, len(currentSegment) - 1)]
            getNodes(end)

        reducedNetwork[start].append((end, len(currentSegment) - 1))

getNodes(entrancePoint)

# visualiseGraph(reducedNetwork, False, weighted=True, name = 'graph2')

distCache = {}

def getCacheKey(path, reachableNodes):
    l = list(map(str, reachableNodes))
    l.sort()
    return str(path[-1]) + ''.join(l)

def getReachableNodes(excludedNodes, reachableNodes = None, currentNode = exitPoint):
    if reachableNodes is None:
        reachableNodes = [exitPoint]
    for neighbor, dist in reducedNetwork[currentNode]:
        if neighbor in excludedNodes or neighbor in reachableNodes:
            continue
        reachableNodes.append(neighbor)
        getReachableNodes(excludedNodes, reachableNodes, neighbor)
    return reachableNodes

def getUpperBound(remainingNodes):
    upperBound = 0
    exploredNodes = set()
    for node in remainingNodes:
        exploredNodes.add(node)
        upperBound += max(0 if n in exploredNodes else d for (n, d) in reducedNetwork[node])

    return upperBound

maxFound = 0

# returns maximum remaining distance
def getMaxDist(path, currentLength):
    reachableNodes = getReachableNodes(path)

    cacheKey = getCacheKey(path, reachableNodes)
    if cacheKey in distCache:
        return distCache[cacheKey]

    upperBound = getUpperBound(reachableNodes)

    if currentLength + upperBound < maxFound:
        print('pruned', path, upperBound)
        return 0

    end = path[-1]
    maxDist = 0
    for neighbour, dist in reducedNetwork[end]:
        if neighbour in path or neighbour not in reachableNodes:
            continue
        if neighbour == exitPoint:
            maxDist = max(maxDist, dist)
        neighbourDist = getMaxDist(path + [neighbour], currentLength + dist)
        maxDist = max(maxDist, neighbourDist + dist)

    distCache[cacheKey] = maxDist
    return maxDist

print(getMaxDist([entrancePoint], 0))