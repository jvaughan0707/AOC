import math
from shared.utils import getInput, getNumbers

targetInput = getInput(17)[0]

xMin, xMax, yMin, yMax = getNumbers(targetInput)
yDiff = yMax - yMin
xDiff = xMax - xMin

validVelocities = set()
for x in range(xMin, xMax +1):
    for y in range(yMin, yMax +1):
        validVelocities.add((x, y))

def checkTrajectory(vx, vy):
    px = py = 0

    while px < xMin or py > yMax:
        px += vx
        py += vy
        if vx > 0:
            vx -= 1
        vy -= 1

    return xMin <= px <= xMax and yMin <= py <= yMax

def inverseTriangle(n):
    return math.ceil((math.sqrt(1 + 8 * n) - 1) / 2)

# min/max velocities ignoring trivial cases
maxVY = -yMin -1
minVY = math.ceil( (1+yMin) / 2)
maxVX = (xMax + 1) // 2
minVX = inverseTriangle(xMin)

print('max height:', maxVY * (maxVY + 1) // 2)

for x in range(minVX, maxVX + 1):
    for y in range(minVY, maxVY + 1):
        if checkTrajectory(x, y):
            validVelocities.add((x, y))

print(len(validVelocities))
