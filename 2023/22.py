from shared.utils import getInput, sub, add

lines = getInput(22)

bricks = []

baseGrid = {}
names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

class Brick:
    def __init__(self, start, end):
        self.supportingBricks = []
        self.supportedBricks = []
        self.start = tuple(map(int, start.split(',')))
        self.end =  tuple(map(int, end.split(',')))
        # self.name = names[len(bricks)]
        self.name = str(len(bricks))

        if self.start[0] != self.end[0]:
            self.orientation = 0
        elif self.start[1] != self.end[1]:
            self.orientation = 1
        else:
            self.orientation = 2

        self.baseHeight = min(self.start[2], self.end[2])
        self.topHeight = max(self.start[2], self.end[2])

        self.length = self.end[self.orientation] + 1 - self.start[self.orientation]

        if self.length <= 0:
            print(self, self.start, self.end, self.length)
        self.direction = tuple(1 if t > 0 else 0 for t in sub(self.end, self.start))

        self.overlappingProjections = set()

        cube = self.start
        for i in range(self.length):
            projection = (cube[0], cube[1])
            if projection not in baseGrid:
                baseGrid[projection] = []
            for p in baseGrid[projection]:
                if p.baseHeight < self.baseHeight:
                    self.overlappingProjections.add(p)
                else:
                    p.overlappingProjections.add(self)

            baseGrid[projection].append(self)

            if self.orientation == 2:
                break
            cube = add(cube, self.direction)

    def __repr__(self):
        # return str(self.start) + '-' + str(self.end)
        return self.name

for line in lines:
    brick = Brick(*line.split('~'))
    bricks.append(brick)

bricks.sort(key=lambda b: b.baseHeight)

supportingBricks = set()
for brick in bricks:
    newHeight = 1
    if brick.overlappingProjections:
        maxHeight = max(brick.overlappingProjections, key=lambda b: b.topHeight).topHeight
        brick.supportingBricks.extend(filter(lambda p : p.topHeight == maxHeight, brick.overlappingProjections))

        for s in brick.supportingBricks:
            s.supportedBricks.append(brick)
        newHeight = maxHeight + 1

    heightDiff = brick.baseHeight - newHeight
    brick.baseHeight = newHeight
    brick.topHeight -= heightDiff

    if len(brick.supportingBricks) == 1:
        supportingBricks.add(brick.supportingBricks[0])

print(len(bricks) - len(supportingBricks))

def getSupportedCount(baseBrick):
    removedBricks = [baseBrick]
    newRemovedBricks = [baseBrick]
    while True:
        bricksToCheck = newRemovedBricks.copy()
        newRemovedBricks = []
        for b in bricksToCheck:
            for s in b.supportedBricks:
                if s in removedBricks or s in newRemovedBricks:
                    continue
                if all(x in removedBricks for x in s.supportingBricks):
                    newRemovedBricks.append(s)

        if not newRemovedBricks:
            break

        removedBricks.extend(newRemovedBricks)

    return len(removedBricks) - 1

total = 0
for brick in supportingBricks:
    total += getSupportedCount(brick)

print(total)

