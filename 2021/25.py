from shared.utils import getGridInput

grid = getGridInput(25, __file__)

allItems = set()
rightItems = set()
downItems = set()

rightMap = {}
downMap = {}

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '>':
            rightItems.add((i,j))
            allItems.add((i,j))
        elif grid[i][j] == 'v':
            downItems.add((i,j))
            allItems.add((i,j))

        rightMap[(i,j)] = (i, (j + 1) % len(grid[i]))
        downMap[(i,j)] = ((i + 1) % len(grid), j)

step = 0

while step < 10000:
    step += 1
    rightMovers = []
    for item in rightItems:
        if rightMap[item] not in allItems:
            rightMovers.append(item)

    for item in rightMovers:
        allItems.remove(item)
        allItems.add(rightMap[item])

        rightItems.remove(item)
        rightItems.add(rightMap[item])

    downMovers = []
    for item in downItems:
        if downMap[item] not in allItems:
            downMovers.append(item)

    for item in downMovers:
        allItems.remove(item)
        allItems.add(downMap[item])
        
        downItems.remove(item)
        downItems.add(downMap[item])


    if not rightMovers and not downMovers:
        break

print(step)