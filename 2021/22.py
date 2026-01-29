from shared.utils import getInput, getNumbers, condense

lines = getInput(22)

instructionsRestricted = []
instructions = []
values = [
    [],[],[]
]

class Cuboid:
    def __init__(self, xRange, yRange, zRange):
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange

    def checkIntersection(self, other):
        xMin = max(self.xRange[0], other.xRange[0])
        xMax = min(self.xRange[1], other.xRange[1])
        yMin = max(self.yRange[0], other.yRange[0])
        yMax = min(self.yRange[1], other.yRange[1])
        zMin = max(self.zRange[0], other.zRange[0])
        zMax = min(self.zRange[1], other.zRange[1])

        if xMin > xMax or yMin > yMax or zMin > zMax:
            return None

        return Cuboid((xMin, xMax), (yMin, yMax), (zMin, zMax))

    def getArea(self):
        return (self.xRange[1] - self.xRange[0] + 1) * (self.yRange[1] - self.yRange[0] + 1) * (self.zRange[1] - self.zRange[0] + 1)

    def __repr__(self):
        return f'{self.xRange}'

    def __eq__(self, other):
        return self.xRange == other.xRange and self.yRange == other.yRange and self.zRange == other.zRange

for line in lines:
    state = line.startswith('on')
    xMin, xMax, yMin, yMax, zMin, zMax = getNumbers(line)

    instructions.append((state, xMin, xMax, yMin, yMax, zMin, zMax))
    if min(xMax, yMax, zMax) >= -50 and max(xMin, yMin, zMin) <= 50:
        instructionsRestricted.append((state, xMin, xMax, yMin, yMax, zMin, zMax))
    values[0].extend([xMin, xMax])
    values[1].extend([yMin, yMax])
    values[2].extend([zMin, zMax])

# coordMap, widthMap = condense(values, False)

# print(coordMap)
# print(widthMap)

positive = []
negative = []

def addPositive(cuboid):
    if cuboid in negative:
        negative.remove(cuboid)
    else:
        positive.append(cuboid)

def addNegative(cuboid):
    if cuboid in positive:
        positive.remove(cuboid)
    else:
        negative.append(cuboid)

for instruction in instructions:
    state, xMin, xMax, yMin, yMax, zMin, zMax = instruction
    #
    # xMin = coordMap[0][xMin]
    # xMax = coordMap[0][xMax]
    # yMin = coordMap[1][yMin]
    # yMax = coordMap[1][yMax]
    # zMin = coordMap[2][zMin]
    # zMax = coordMap[2][zMax]

    new = Cuboid((xMin, xMax), (yMin, yMax), (zMin, zMax))

    currentPos = positive.copy()
    currentNeg = negative.copy()

    if state:
        for c in currentPos:
            overlap = new.checkIntersection(c)
            if overlap:
                addNegative(overlap)
        for c in currentNeg:
            overlap = new.checkIntersection(c)
            if overlap:
                addPositive(overlap)
        addPositive(new)
    else:
        for c in currentNeg:
            overlap = new.checkIntersection(c)
            if overlap:
                addPositive(overlap)
        for c in currentPos:
            overlap = new.checkIntersection(c)
            if overlap:
                addNegative(overlap)

total = 0
for c in positive:
    total += c.getArea()

for c in negative:
    total -= c.getArea()

print(total)

