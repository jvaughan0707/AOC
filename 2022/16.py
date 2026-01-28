from shared.utils import getInput, getMinDist, visualiseGraph
import re
lines = getInput(16)

class Valve:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.neighbours = []

valves = {}
nonZeroValves = set()
for line in lines:
    matches = re.search(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
    name, value, neighbours = matches.groups()

    v = Valve(name, int(value))
    for n in neighbours.split(', '):
        v.neighbours.append(n)

    valves[name] = v

    if int(value) > 0:
        nonZeroValves.add(v.name)

adjMap = { n.name: n.neighbours for n in valves.values()}

print(adjMap)

start = 'AA'

def getReducedMap():
    reducedMap = {n: {} for n in nonZeroValves}
    reducedMap[start] = {}

    for n1 in nonZeroValves:
        for n2 in nonZeroValves:
            if n1 <= n2:
                continue
            # amount of time to get from current node and turn on the target (+1)
            d = getMinDist(adjMap, n1, n2, False) + 1

            reducedMap[n1][n2] = d
            reducedMap[n2][n1] = d

        dStart = getMinDist(adjMap, n1, 'AA', False) + 1
        reducedMap[n1][start] = dStart
        reducedMap[start][n1] = dStart

    return reducedMap

reducedMap = getReducedMap()
print(reducedMap)

# visualiseGraph(adjMap, colorMap=lambda x: 'red' if x in nonZeroValves else 'blue')

def getMaxScore(activeValves, currentPosition, remainingTime):
    # print(activeValves, currentPosition, remainingTime)
    currentNeighbours = reducedMap[currentPosition]
    if remainingTime <= 0:
        return 0

    maxScore = 0
    for neighbour, dist in currentNeighbours.items():
        if neighbour in activeValves:
            continue
        if dist > remainingTime:
            continue
        maxScore = max(maxScore, valves[neighbour].value * (remainingTime - dist) + getMaxScore(activeValves + [neighbour], neighbour, remainingTime - dist))
    return maxScore

# print(getMaxScore([start], start, 30))

globalMaxScore = 0
def getMaxScore2(activeValves, aPos, bPos, aTime, bTime, currentScore = 0):
    global globalMaxScore
    aNeighbours = reducedMap[aPos]
    bNeighbours = reducedMap[bPos]
    if aTime <= 0 and bTime <= 0:
        return 0

    upperBound = 0
    for r in nonZeroValves:
        if r in activeValves:
            continue
        rScore = valves[r].value
        upperBound += rScore * max(0, aTime - aNeighbours[r], bTime - bNeighbours[r])

    if currentScore + upperBound < globalMaxScore:
        return 0

    maxScore = currentScore
    for aNeighbour, aDist in aNeighbours.items():
        if aNeighbour in activeValves or aDist > aTime:
            continue

        for bNeighbour, bDist in bNeighbours.items():
            if bNeighbour in activeValves or bDist > bTime or bNeighbour == aNeighbour:
                continue
            if bPos == start and bNeighbour < aNeighbour:
                continue

            maxScore = max(maxScore,
                           getMaxScore2(activeValves + [aNeighbour, bNeighbour], aNeighbour, bNeighbour, aTime - aDist, bTime - bDist,
                                        currentScore + valves[aNeighbour].value * (aTime - aDist) + valves[bNeighbour].value * (bTime - bDist)))

        if bTime < 10:
            maxScore = max(maxScore,
                           getMaxScore2(activeValves + [aNeighbour], aNeighbour, bPos, aTime - aDist,0,
                                        currentScore + valves[aNeighbour].value * (aTime - aDist)))

    if aTime < 10:
        for bNeighbour, bDist in bNeighbours.items():
            if bNeighbour in activeValves or bDist > bTime:
                continue

            maxScore = max(maxScore,
                           getMaxScore2(activeValves + [bNeighbour], aPos, bNeighbour, 0, bTime - bDist,
                                        currentScore + valves[bNeighbour].value * (bTime - bDist)))
    globalMaxScore = max(globalMaxScore, maxScore)
    return maxScore

print(getMaxScore2([start], start, start, 26, 26))
