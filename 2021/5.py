from AOC.shared.utils import getInput, getNumbers, sub, add

inputLines = getInput(5)

lines = []

for l in inputLines:
    x1,y1,x2,y2 = getNumbers(l)
    # if x1 == x2 or y1 == y2:
    lines.append(((x1,y1),(x2,y2)))

points = set()
duplicatePoints = set()
for line in lines:
    dx, dy = sub(line[1], line[0])
    scale = max(abs(dx), abs(dy))

    dx //= scale
    dy //= scale

    p = line[0]

    while p != line[1]:
        if p in points:
            duplicatePoints.add(p)
        points.add(p)
        p = add(p, (dx,dy))

    if p in points:
        duplicatePoints.add(p)
    points.add(p)

print(points)
print(duplicatePoints)
print(len(duplicatePoints))