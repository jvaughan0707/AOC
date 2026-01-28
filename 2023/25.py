from shared.utils import getInput, getGlobalMinCuts, getConnectedPoints
import sys
sys.setrecursionlimit(150000)

lines = getInput(25)

adjMap = {}

def createOrGet(node):
    if node not in adjMap:
        adjMap[node] = []
    return adjMap[node]

for line in lines:
    source, targets = line.split(': ')

    createOrGet(source).extend(targets.split())

    for target in targets.split():
        createOrGet(target).append(source)


# cuts = ldl-fpg, dfk-nxk, hcf-lhn

minCutEdges = getGlobalMinCuts(adjMap, 3)
print(minCutEdges)

for e in minCutEdges:
    adjMap[e[0]].remove(e[1])
    adjMap[e[1]].remove(e[0])

start = list(adjMap)[0]

size = len(getConnectedPoints(adjMap, start))

print(size)
print(len(adjMap) - size)

print(size * (len(adjMap) - size))
