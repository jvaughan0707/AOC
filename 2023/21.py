from copy import deepcopy

from shared.utils import getGridInput, getFirstInGrid, directions, isOob, get, add

og = getGridInput(21)
width = len(og[0])
height = len(og)
sPos = getFirstInGrid(og, 'S')
og[sPos[0]][sPos[1]] = '.'


def getCount(steps, start):
    grid = deepcopy(og)
    grid[start[0]][start[1]] = 'O'

    for x in range(steps):
        newGrid = deepcopy(grid)
        for i in range(height):
            for j in range(width):
                p = (i, j)
                if grid[i][j] == '#':
                    continue
                if grid[i][j] == 'O':
                    newGrid[i][j] = '.'
                for d in directions.values():
                    if get(grid, add(p, d)) == 'O':
                        newGrid[i][j] = 'O'
        grid = newGrid

    # for row in grid:
    #     print(' '.join(row))

    return sum(row.count('O') for row in grid)

half = int((width - 1) / 2)

totalSteps = 26501365

n = totalSteps // width # n is even, center block will be odd parity
fullyCompletedBlocks =  [n ** 2, (n - 1) ** 2] # even, odd

smallCornersCount = n # even parity
largeCornersCount = n - 1 # odd parity

smallCorners = {
    'tl': getCount(half - 1, (0,0)),
    'tr': getCount(half - 1, (0,width-1)),
    'bl': getCount(half - 1, (height- 1,0)),
    'br': getCount(half - 1, (height-1,width-1)),
}

largeCorners = {
    'tl': getCount(width + half - 1, (height-1,width-1)),
    'tr': getCount(width + half - 1, (height-1,0)),
    'bl': getCount(width + half - 1, (0,width-1)),
    'br': getCount(width + half - 1, (0,0)),
}

tips = {
    'u': getCount(height - 1, (height-1,half)),
    'd': getCount(height - 1, (0,half)),
    'l': getCount(height - 1, (half,width-1)),
    'r': getCount(height - 1, (half, 0)),
}

fullEven = getCount(height - 1, (half, half))
fullOdd = getCount(height, (half, half))

total = (fullyCompletedBlocks[0] * fullEven +
    fullyCompletedBlocks[1] * fullOdd +
    sum(tips.values()) +
    smallCornersCount * sum(smallCorners.values()) +
    largeCornersCount * sum(largeCorners.values()))

print(total)