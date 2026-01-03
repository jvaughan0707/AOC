from AOC.shared.utils import getInput, sub, add

lines = getInput(22)

bricks = []

baseGrid = {}
# names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class Brick:
    def __init__(self, start, end):
        self.supportingBricks = []
        self.start = tuple(map(int, start.split(',')))
        self.end =  tuple(map(int, end.split(',')))
        # self.name = names[len(bricks)]

        if self.start[0] != self.end[0]:
            self.orientation = 0
        elif self.start[1] != self.end[1]:
            self.orientation = 1
        else:
            self.orientation = 2

        self.baseHeight = min(self.start[2], self.end[2])
        self.topHeight = max(self.start[2], self.end[2])

        self.locked = False
        self.length = self.end[self.orientation] + 1 - self.start[self.orientation]

        if self.length <= 0:
            print(self, self.start, self.end, self.length)
        self.direction = tuple(1 if t > 0 else 0 for t in sub(self.end, self.start))

        self.overlappingProjections = set()

        self.cubes = []
        cube = self.start
        for i in range(self.length):
            self.cubes.append(cube)
            cube = add(cube, self.direction)

        for cube in self.cubes:
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

    def __repr__(self):
        return str(self.start) + '-' + str(self.end)

for line in lines:
    brick = Brick(*line.split('~'))
    bricks.append(brick)

bricks.sort(key=lambda b: b.baseHeight)

supportingBricks = set()
for brick in bricks:
    newHeight = 1
    if brick.overlappingProjections:
        if any(not x.locked for x in brick.overlappingProjections):
            print('not locked')
        maxHeight = max(brick.overlappingProjections, key=lambda b: b.topHeight).topHeight
        brick.supportingBricks.extend(filter(lambda p : p.topHeight == maxHeight, brick.overlappingProjections))
        newHeight = maxHeight + 1

    heightDiff = brick.baseHeight - newHeight
    brick.baseHeight = newHeight
    brick.topHeight -= heightDiff
    newCubes = []
    for cube in brick.cubes:
        newCubes.append((cube[0], cube[1], cube[2] - heightDiff))
    brick.cubes = newCubes
    if len(brick.supportingBricks) == 1:
        supportingBricks.add(brick.supportingBricks[0])

    brick.locked = True

print(len(supportingBricks))
print(len(bricks))
print(len(bricks) - len(supportingBricks))

# > 384

allCubes = set()

for brick in bricks:
    for cube in brick.cubes:
        if cube in allCubes:
            print('duplicate cube:', cube)

        allCubes.add(cube)

print(len(allCubes))

# for brick in bricks:
#     print(brick.name, brick.cubes)