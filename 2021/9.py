from AOC.shared.utils import getNumbersGridInput, getGridPoints, formatText

grid = getNumbersGridInput(9)

points = getGridPoints(grid)
lowPoints = set()
total = 0
for point in points.values():
    if point.value < min([n.value for n in point.neighbours.values()]):
        lowPoints.add(point)
        total += point.value + 1

print(total)

def expandBasin(basin, point):
    for nextPoint in point.neighbours.values():
        if nextPoint in basin:
            continue

        if nextPoint.value == 9:
            continue
        valid = True
        for neighbour in nextPoint.neighbours.values():
            if neighbour not in basin and neighbour.value < nextPoint.value:
                valid = False
            # print(nextPoint, nextPoint.value, neighbour, neighbour.value, valid)

        if valid:
            basin.add(nextPoint)
            expandBasin(basin, nextPoint)

basins = []
for lowPoint in lowPoints:
    basin = { lowPoint }
    expandBasin(basin, lowPoint)

    basins.append(basin)

allBasinPoints = set()
for b in basins:
    print(len(b), sorted(list([p.position for p in b])))
    print()
    for p in b:
        allBasinPoints.add(p)

lengths = [len(basin) for basin in basins]
lengths.sort(reverse=True)

total = 1
for i in range(3):
    total *= lengths[i]

print(total)

for i in range(len(grid)):
    row = ''
    for j in range(len(grid[0])):
        point = points[(i,j)]
        valueStr = str(point.value)
        if point in lowPoints:
            row += formatText(valueStr, 'blue', 'b')
        elif point in allBasinPoints:
            row += formatText(valueStr, 'red', 'b')
        else:
            row += valueStr

    print(row)