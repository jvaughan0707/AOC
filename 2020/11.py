from shared.utils import getGridInput, getGridPoints

grid = getGridInput(11, __file__)

points = getGridPoints(grid, True)
def iterate(abandonThreshold):
    newValues = {}
    for pos, point in points.items():
        if point.value == 'L':
            if not list(filter(lambda n: n.value == '#', point.neighbours.values())):
                newValues[pos] = '#'
        elif point.value == '#':
            if sum([1 for _ in filter(lambda n: n.value == '#', point.neighbours.values())]) >= abandonThreshold:
                newValues[pos] = 'L'
                
    for (i,j), v in newValues.items():
        points[(i,j)].value = v
        grid[i][j] = v

    return newValues

def getFirstSeat(point, dir):
    current = point.neighbours[dir]
    while current.value == '.':
        if dir in current.neighbours:
            current = current.neighbours[dir]
        else:
            return None
        
    return current

def reduceNeighbours():
    for point in points.values():
        for dir in list(point.neighbours):
            newNeighbour = getFirstSeat(point, dir)
            if newNeighbour:
                point.neighbours[dir] = newNeighbour
            else:
                del point.neighbours[dir]

# remove for part 1            
reduceNeighbours()
while iterate(5):
    pass

print(sum([''.join(row).count('#') for row in grid]))
