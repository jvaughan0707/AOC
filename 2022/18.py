from shared.utils import getInput, add, sub

lines = getInput(18)

points = set()

for line in lines:
    x,y,z = line.split(',')
    points.add((int(x), int(y), int(z)))

print(points)

X = (1, 0, 0)
Y = (0, 1, 0)
Z = (0, 0, 1)
X_ = (-1, 0, 0)
Y_ = (0, -1, 0)
Z_ = (0, 0, -1)

total = 0

def isAdj(p1, p2):
    diff = sub(p1, p2)
    return diff in [X, Y, Z, X_, Y_, Z_]

for point in points:
    for d in [X,Y,Z]:
        if add(point, d) not in points:
            total += 1
        if sub(point, d) not in points:
            total += 1

print(total)

xLines = {}
yLines = {}
zLines = {}

def addLinePoint(k, v, l):
    if k not in l:
        l[k] = [v, v]
    else:
        current = l[k]
        l[k] = [min(current[0], v), max(current[1], v)]

for point in points:
    x,y,z = point
    addLinePoint((y,z), x, xLines)
    addLinePoint((x,z), y, yLines)
    addLinePoint((x,y), z, zLines)

interiorPoints = set()
exteriorPoints = set()

def checkExteriorPoint(p):
    if p in points or p in exteriorPoints:
        return
    x,y,z = p

    if (y,z) not in xLines or (x,z) not in yLines or (x,y) not in zLines:
        return

    minX, maxX = xLines[(y,z)]
    minY, maxY = yLines[(x,z)]
    minZ, maxZ = zLines[(x,y)]

    if x < minX or x > maxX or y < minY or y > maxY or z < minZ or z > maxZ:
        exteriorPoints.add(p)
    else:
        interiorPoints.add(p)

for point in points:
    for d in [X,Y,Z]:
        checkExteriorPoint(add(point, d))
        checkExteriorPoint(sub(point, d))

def expand(exteriorPoint):
    removedPoints = []
    for d in [X,Y,Z]:
        p1 = add(exteriorPoint, d)
        p2 = sub(exteriorPoint, d)
        if p1 in interiorPoints:
            interiorPoints.remove(p1)
            removedPoints.append(p1)
        if p2 in interiorPoints:
            interiorPoints.remove(p2)
            removedPoints.append(p2)

    for p in removedPoints:
        expand(p)

for point in exteriorPoints:
    expand(point)

total = 0

for point in points:
    for d in [X,Y,Z]:
        p1 = add(point, d)
        if p1 not in points and p1 not in interiorPoints:
            total += 1
        p2 = sub(point, d)
        if p2 not in points and p2 not in interiorPoints:
            total += 1

print(total)