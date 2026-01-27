from AOC.shared.utils import getInput, add

lines = getInput(14)

grid = set()
maxY = 0
minX = 500
maxX = 500

for line in lines:
    coords = line.split(' -> ')

    previous = None
    for coord in coords:
        x = int(coord.split(',')[0])
        y = int(coord.split(',')[1])
        maxY = max(maxY, y)
        grid.add((x, y))
        if previous is not None:
            px, py = previous
            xFixed = px == x

            if xFixed:
                for j in range(min(py, y) + 1, max(py, y)):
                    grid.add((x, j))
            else:
                for j in range(min(px, x) + 1, max(px, x)):
                    grid.add((j, y))
        previous = (x, y)

wallGrid = grid.copy()

def addSand():
    global maxY, minX, maxX
    pos = (500, 0)

    while pos[1] < maxY + 1:
        down = add(pos, (0, 1))
        if add(pos, (0, 1)) not in grid:
            pos = down
            continue
        dl = add(pos, (-1, 1))
        if dl not in grid:
            pos = dl
            continue
        dr = add(pos, (1, 1))
        if dr not in grid:
            pos = dr
            continue

        break
    grid.add(pos)
    minX = min(minX, pos[0])
    maxX = max(maxX, pos[0])
    return pos

t = 0
while True:
    # if addSand()[1] >= maxY:
    #     break

    if addSand()[1] == 0:
        t += 1
        break
    t += 1

print(t)

def printGrid():
    for i in range(maxY + 4):
        row = ''
        for j in range(minX, maxX + 1):
            if (j, i) in grid:
                if (j, i) in wallGrid:
                    row += '#'
                else:
                    row += 'o'
            else:
                row += '.'
        print(row)


