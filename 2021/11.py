from shared.utils import getNumbersGridInput, getGridPoints

grid = getNumbersGridInput(11)

points = getGridPoints(grid, True)


flashCount = 0

class Octopus:
    def __init__(self, point):
        self.point = point
        self.position = point.position
        self.value = point.value
        self.neighbours = []

    def increment(self):
        if self.value > 9:
            return

        self.value += 1

        if self.value > 9:
            self.doFlash()

    def doFlash(self):
        global flashCount
        flashCount += 1
        for n in self.neighbours:
            n.increment()

    def reset(self):
        if self.value > 9:
            self.value = 0

    def __repr__(self):
        return str(self.point)

octopi = { p: Octopus(points[p]) for p in points}

for o1 in octopi.values():
    o1.neighbours = [octopi[n.position] for n in o1.point.neighbours.values()]


for t in range(1950):
    for o in octopi.values():
        o.increment()

    for o in octopi.values():
        o.reset()

    total = sum([o.value for o in octopi.values()])

    print('time:', t+1, 'count:', flashCount, 'grid:')
    for i in range(len(grid)):
        row = ''
        for j in range(len(grid[0])):
            row += str(octopi[(i,j)].value)

        print(row)

    if total == 0:
        break
