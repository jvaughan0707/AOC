from shared.utils import getInput

lines = getInput(8)

u, r, d, l = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Tree:
    def __init__(self, value, i, j):
        self.value = value
        self.i = i
        self.j = j

        self.dirDists = {
            u: 0,
            r: 0,
            d: 0,
            l: 0
        }

    def incr(self, dir):
        self.dirDists[dir] = self.dirDists[dir] + 1

    def getScore(self):
        x = 1
        for v in self.dirDists.values():
            x *= v
        return x


grid = []

i = 0
for line in lines:
    row = []
    for j in range(len(line)):
        row.append(Tree(int(line[j]), i, j))
    grid.append(row)
    i += 1

width = len(grid[0])
height = len(grid)

def traverse(i, j, dir):
    visTrees = set()

    while 0 <= i < height and 0 <= j < width:
        current = grid[i][j]
        for t in visTrees.copy():
            t.incr(dir)
            if t.value <= current.value:
                visTrees.remove(t)

        visTrees.add(current)
        i += dir[0]
        j += dir[1]


for i in range(height):
    traverse(i, 0, r)
    traverse(i, width - 1, l)

for j in range(width):
    traverse(0, j, d)
    traverse(height - 1, j, u)

total = 0
print()

print(max([max([t.getScore() for t in r]) for r in grid]))