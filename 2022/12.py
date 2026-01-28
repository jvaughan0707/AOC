from shared.utils import getGridInput, getNetwork, getFirstInGrid, getMinDist, get

grid = getGridInput(12)

def getHeight(x):
    if x == 'S':
        return ord('a')
    elif x == 'E':
        return ord('z')
    else:
        return ord(x)

# calculating reverse path from end to start so adj func is flipped
def isAdj(a, b, _):
    x = getHeight(a)
    y = getHeight(b)

    return x <= y + 1

network = getNetwork(grid, isAdj)

start = getFirstInGrid(grid, 'S')
end = getFirstInGrid(grid, 'E')

distMap = {}
startEndDist = getMinDist(network, end, start, False, distMap)
print(startEndDist)

globalMinDist = startEndDist

for p, d in distMap.items():
    if d < globalMinDist and get(grid, p) == 'a':
        globalMinDist = d

print(globalMinDist)