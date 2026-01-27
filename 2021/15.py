from AOC.shared.utils import getNumbersGridInput, getGridPoints, getMinDist

grid = getNumbersGridInput(15)

height = len(grid)
width = len(grid[0])

for i in range(height):
    newRow = grid[i].copy()
    for x in range(4):
        newRow.extend([(v + x) % 9 + 1 for v in grid[i]])

    grid[i] = newRow

for x in range(4):
    for i in range(height):
        grid.append([(v + x) % 9  + 1 for v in grid[i]])

height = len(grid)
width = len(grid[0])

print(grid)
points = getGridPoints(grid)

adjMap = { p.position: {n.position: n.value for n in p.neighbours.values()} for p in points.values() }

# print(adjMap)

minDist = getMinDist(adjMap, (0,0), (height - 1, width - 1))

print(minDist)