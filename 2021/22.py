from AOC.shared.utils import getInput, getNumbers, condense

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

    newPos = []
    newNeg = []

    if state:
        for c in positive:
            overlap = new.checkIntersection(c)
            if overlap:
                newNeg.append(overlap)
        for c in negative:
            overlap = new.checkIntersection(c)
            if overlap:
                newPos.append(overlap)
        newPos.append(new)
    else:
        for c in negative:
            overlap = new.checkIntersection(c)
            if overlap:
                newPos.append(overlap)
        for c in positive:
            overlap = new.checkIntersection(c)
            if overlap:
                newNeg.append(overlap)

    print(new, newPos, newNeg)
    positive.extend(newPos)
    negative.extend(newNeg)

    total = 0
    for c in positive:
        total += c.getArea()

    for c in negative:
        total -= c.getArea()

    print(total)

print(positive)
print(negative)

#[(10, 10)]
#[(11, 11), (11, 11), (10, 10)]