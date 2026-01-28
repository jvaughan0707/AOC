from shared.utils import getSectionsInput, getNumbers, add, up, down, left, right, scale
import re
import math

sections = getSectionsInput(22)
rows = {}
cols = {}
grid = {}
lines = sections[0]
width = len(lines[0])
height = len(lines)

for i, line in enumerate(sections[0]):
    for j, c in enumerate(line):
        if c not in ['.', '#']:
            continue
        grid[(i,j)] = c
        if i not in rows:
            rows[i] = [j, j]
        else:
            rows[i][1] = j
        if j not in cols:
            cols[j] = [i, i]
        else:
            cols[j][1] = i

instructions = sections[1][0]
numbers = getNumbers(instructions)
turns = re.findall(r'[LR]', instructions)

start = (0, rows[0][0])
directions = [
    right,
    down,
    left,
    up
]

def getPath2d():
    current = start
    directionIndex = 0
    for i, l in enumerate(numbers):
        direction = directions[directionIndex]
        for x in range(l):
            nextPoint = add(current, direction)

            if nextPoint not in grid:
               row = rows[current[0]]
               col = cols[current[1]]
               if direction == right:
                   nextPoint = (nextPoint[0], row[0])
               elif direction == left:
                   nextPoint = (nextPoint[0], row[1])
               elif direction == down:
                   nextPoint = (col[0], nextPoint[1])
               elif direction == up:
                   nextPoint = (col[1], nextPoint[1])

            if grid[nextPoint] == '#':
                break
            else:
                current = nextPoint

        if i < len(turns):
            turn = turns[i]
            if turn == 'R':
                directionIndex = (directionIndex + 1) % 4
            else:
                directionIndex = (directionIndex - 1) % 4

    print((current[0] + 1) * 1000 + (current[1] + 1) * 4 + directionIndex)

totalPoints = len(grid.values())
faceSize = int(math.sqrt(totalPoints / 6))

faces = {}

def simplifyDirectionPath(path, turnCount = 0):
    # take a sequence of directions from one face to another, e.g. 1,1,2 (D,D,L), and collapse it into a single direction and rotation.
    # rotation is the number of 90 deg clockwise turns that a path would take when going from one face to the next

    if len(path) == 1:
        return path[0], turnCount
    if len(path) == 2:
        if path[0] == path[1]:
            return -1, 0
        return path[1], ((path[0] - path[1]) + turnCount) % 4

    # find a consecutive pair of different directions, collapse it and then substitute that back into the list and continue processing
    for i in range(len(path) - 1):
        if path[i] == path[i + 1]:
            continue

        d, t = simplifyDirectionPath([path[i],path[i + 1]])

        # any directions after the collapsed pair need to be rotated by the amount of rotation they produce.
        # negative because the face is rotated in the opposite direction relative to the path
        return simplifyDirectionPath(path[:i] + [d] + [(d2 - t) % 4 for d2 in path[i + 2:]], (turnCount + t) % 4)

    return path[0] + 2, turnCount

class Face:
    def __init__(self,x,y):
        # x and y are scaled down coordinates
        self.x = x
        self.y = y
        self.faces = {}
        self.adjacent = {}
        self.base = (self.y * faceSize, self.x * faceSize)

    def addAdjacentFaces(self):
        for d, direction in enumerate(directions):
            nextPoint = add((self.y, self.x), direction)
            if nextPoint in faces:
                self.adjacent[d] = faces[nextPoint]

    def __repr__(self):
        return f'({self.x},{self.y})'

    def addFaces(self, source, path):
        # recursively add all faces to source face, calculating direction and rotation
        # the cube net is a tree so no need to worry about cycles, just check the previous direction to prevent duplication
        if path:
            d, t = simplifyDirectionPath(path)
            if d != -1:
                if d in source.faces:
                    print('duplicate face')
                    print(source, path, d, t)
                    return
                source.faces[d] = (self, t)

        for d, f in self.adjacent.items():
            if path and (d + 2) % 4 == path[-1]:
                continue

            f.addFaces(source, path + [d])

for y in range(height//faceSize + 1):
    for x in range(width // faceSize + 1):
        if (y * faceSize, x * faceSize) in grid:
            faces[(y,x)] = Face(x,y)

for face in faces.values():
    face.addAdjacentFaces()

for face in faces.values():
    face.addFaces(face, [])
    print(face, face.faces)

def getFace(p):
    p = (p[0]//faceSize, p[1]//faceSize)
    if p not in faces:
        return None
    return faces[p]

def getPath3d():
    current = start
    directionIndex = 0
    currentFace = getFace(current)
    for i, l in enumerate(numbers):
        direction = directions[directionIndex]
        for x in range(l):
            nextPoint = add(current, direction)

            if getFace(nextPoint) != currentFace:
                nextFace, rotation = currentFace.faces[directionIndex]
                p1, p2 = nextPoint
                p1 %= faceSize
                p2 %= faceSize

                for r in range(rotation):
                    p1, p2 = p2, faceSize - p1 - 1

                nextPoint = add((p1,p2), nextFace.base)
                if grid[nextPoint] == '#':
                    break
                else:
                    currentFace = nextFace
                    directionIndex = (directionIndex + rotation) % 4
                    direction = directions[directionIndex]

            if grid[nextPoint] == '#':
                break
            else:
                current = nextPoint

        if i < len(turns):
            turn = turns[i]
            if turn == 'R':
                directionIndex = (directionIndex + 1) % 4
            else:
                directionIndex = (directionIndex - 1) % 4

    print((current[0] + 1) * 1000 + (current[1] + 1) * 4 + directionIndex)

getPath3d()