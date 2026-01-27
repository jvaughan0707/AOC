from AOC.shared.utils import getInput

lines = getInput(12)

adjMap = {}

for line in lines:
    left, right = line.split('-')

    if left not in adjMap:
        adjMap[left] = []
    adjMap[left].append(right)
    if right not in adjMap:
        adjMap[right] = []
    adjMap[right].append(left)

def isSmall(c):
    return c.lower() == c

def findAllPaths(currentPath, end):
    currentNode = currentPath[-1]

    paths = []

    for neighbour in adjMap[currentNode]:
        if neighbour == end:
            paths.append(currentPath + [neighbour])
            continue
        if isSmall(neighbour) and neighbour in currentPath:
            continue

        paths.extend(findAllPaths(currentPath + [neighbour], end))

    return paths


def findAllPaths2(currentPath, end, repeatedSmall=False):
    currentNode = currentPath[-1]

    paths = []

    for neighbour in adjMap[currentNode]:
        if neighbour == 'start':
            continue
        if neighbour == end:
            paths.append(currentPath + [neighbour])
            continue
        if isSmall(neighbour) and neighbour in currentPath:
            if repeatedSmall:
                continue

            paths.extend(findAllPaths2(currentPath + [neighbour], end, True))
            continue

        paths.extend(findAllPaths2(currentPath + [neighbour], end, repeatedSmall))

    return paths


allPaths = findAllPaths2(['start'], 'end')
print(len(allPaths))
