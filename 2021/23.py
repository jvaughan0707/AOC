from copy import deepcopy

from shared.utils import getGridInput, getNetwork

initialGrid = getGridInput(23)

extraRows = ['  #D#C#B#A#', '  #D#B#A#C#']
initialGrid.insert(3, list(extraRows[0]))
initialGrid.insert(4, list(extraRows[1]))

height = len(initialGrid) - 2

graph = getNetwork(initialGrid, wallSymbols='# ')

targetColMap = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9,
}

costMap = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

cols = set([j for i,j in graph])

initialStacks = { x: [] for x in targetColMap.values() }
hallPositions = {}

stateHistory = {}

for i, j in sorted(graph.keys()):
    v = initialGrid[i][j]
    if v != '.':
        initialStacks[j].insert(0, v)

def isValidPath(starCol, endCol, halls):
    startCol, endCol = sorted([starCol, endCol])
    return not any(startCol < x < endCol for x in halls)

def getDist(startCol, sourceStack, targetCol, targetStack):
    dist = abs(targetCol - startCol)

    if sourceStack is not None:
        dist += height - len(sourceStack)

    if targetStack is not None:
        dist += height - len(targetStack) - 1

    return dist

globalMin = -1

def exploreOptions(stacks, halls, cost):
    global globalMin
    cacheKey = str(stacks) + str(halls)

    lowerBound = 0
    for col, stack in stacks.items():
        for item in stack:
            targetCol = targetColMap[item]
            targetStack = stacks[targetCol]
            if targetCol == col:
                continue
            lowerBound += costMap[item] * getDist(col, stack, targetCol, targetStack)

    for col, item in halls.items():
        targetCol = targetColMap[item]
        targetStack = stacks[targetCol]
        if targetCol == col:
            continue
        lowerBound += costMap[item] * getDist(col, None, targetCol, targetStack)

    if globalMin != -1 and cost + lowerBound > globalMin:
        return -1
    if cacheKey in stateHistory and stateHistory[cacheKey] <= cost:
        return -1
    stateHistory[cacheKey] = cost

    # check if any hall items can move to their targets. If there are any then no other moves will be considered
    for col, item in list(halls.items()):
        targetCol = targetColMap[item]
        stacksCopy = deepcopy(stacks)
        targetStack = stacksCopy[targetCol]
        if all(x == item for x in targetStack) and isValidPath(col, targetCol, halls):
            extraCost = getDist(col, None, targetCol, targetStack) * costMap[item]
            hallsCopy = deepcopy(halls)
            targetStack.append(item)
            del hallsCopy[col]
            return exploreOptions(stacksCopy, hallsCopy, cost + extraCost)

    minCost = -1

    # check if any item in a stack can move to its target stack. If so then no other moves will be considered
    lockedStacks = []
    for col, stack in stacks.items():
        if not stack:
            continue
        item = stack[-1]
        targetCol = targetColMap[item]
        if col == targetCol and (len(stack) == 1 or stack[0] == item):
            # item is in the correct stack and all other items (if any) are the same type. This stack cannot be removed from
            lockedStacks.append(stack)
            continue
        stacksCopy = deepcopy(stacks)
        stack = stacksCopy[col]
        targetStack = stacksCopy[targetCol]
        if all(x == item for x in targetStack) and isValidPath(col, targetCol, halls):
            extraCost = getDist(col, stack, targetCol, targetStack) * costMap[item]
            targetStack.append(item)
            stack.pop()
            return exploreOptions(stacksCopy, halls, cost + extraCost)

    if not halls and len(lockedStacks) == len(targetColMap.values()):
        if globalMin == -1 or cost < globalMin:
            globalMin = cost
        return cost

    # otherwise some item will have to move out of one stack and into the hall. Explore all possibilities
    for col, stack in stacks.items():
        if stack in lockedStacks or not stack:
            continue

        for targetCol in cols:
            if targetCol in targetColMap.values() or targetCol in halls:
                continue
            if not isValidPath(col, targetCol, halls):
                continue
            stacksCopy = deepcopy(stacks)
            stack = stacksCopy[col]
            hallsCopy = deepcopy(halls)

            item = stack[-1]
            extraCost = getDist(col, stack, targetCol, None) * costMap[item]
            stack.pop()
            hallsCopy[targetCol] = item
            newCost = exploreOptions(stacksCopy, hallsCopy, cost + extraCost)
            if newCost != -1 and (minCost == -1 or newCost < minCost):
                minCost = newCost

    return minCost

print(exploreOptions(initialStacks, hallPositions, 0))