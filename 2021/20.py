from shared.utils import getSectionsInput

sections = getSectionsInput(20)

algoStr = sections[0][0]


def symbolsToBin(string):
    return string.replace('#', '1').replace('.', '0')

algoStr = symbolsToBin(algoStr)

initialGrid = [symbolsToBin(row) for row in sections[1]]

def extend(grid, symbol = None):
    if not symbol:
        symbol = grid[0][0]
    height = len(grid)
    for i in range(height):
        grid[i] = symbol + grid[i] + symbol

    width = len(grid[0])
    grid.insert(0, symbol * width)
    grid.append(symbol * width)

extend(initialGrid, '0')

def getNeighbours(grid, point):
    result = ''
    for di in range(-1, 2):
        for dj in range(-1, 2):
            result += grid[point[0]+di][point[1]+dj]

    return result

def printGrid(grid):
    for row in grid:
        print(row.replace('1', '#').replace('0', '.'))

    print()

def enhance(grid, times = 1):
    extend(grid)

    width = len(grid[0])
    height = len(grid)
    newGrid = []

    for i in range(1, height - 1):
        newRow = ''
        for j in range(1, width - 1):
            neighbours = getNeighbours(grid, (i,j))
            algoIndex = int(neighbours, 2)
            newRow += algoStr[algoIndex]
        newGrid.append(newRow)

    extend(newGrid)
    if times > 1:
        return enhance(newGrid, times - 1)
    return newGrid

printGrid(initialGrid)
enhanced = enhance(initialGrid, 50)
printGrid(enhanced)

print(sum(row.count('1') for row in enhanced))

# < 5776