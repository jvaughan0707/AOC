from shared.utils import getGridInput

grid = getGridInput(3, __file__)
width = len(grid[0])
trees = set()

for i, row in enumerate(grid):
    for j, square in enumerate(row):
        if square == '#':
            trees.add((i,j))


def checkPath(down, right):
    i = j = 0
    total = 0
    while True:
        i += down
        j += right
        j %= width

        if i >= len(grid):
            break

        if (i,j) in trees:
            total +=1

    return total

print(checkPath(1,3))

prod = 1

for slope in [(1,1), (1,3),(1,5),(1,7),(2,1)]:
    prod *= checkPath(*slope)

print(prod)