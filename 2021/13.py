from shared.utils import getSectionsInput, getNumbers

coordsList, foldLines = getSectionsInput(13)

points = [tuple(map(int, l.split(','))) for l in coordsList]
print(sorted(points))

for fold in foldLines:
    line = int(fold[13:])
    direction = fold[11]

    newPoints = set()

    for p in points:
        x,y = p
        if direction == 'x' and x > line:
            x = 2 * line - x
        elif direction == 'y' and y > line:
            y = 2 * line - y

        newPoints.add((x,y))

    points = newPoints

    print(len(points))

    print(sorted(points))

for y in range(0, max([j for (i, j) in points]) + 1):
    row = ''
    for x in range(0, max([i for (i, j) in points]) + 1):
        if (x, y) in points:
            row += '#'
        else:
            row += ' '

    print(row)