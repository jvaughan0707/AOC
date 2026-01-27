from AOC.shared.utils import getInput, directions, add, scale
import sys
sys.setrecursionlimit(150000)
lines = getInput(18)

minI, minJ, maxI, maxJ = 0, 0, 0, 0

turns = []


for line in lines:
    d, l, colour = line.split()

    num = colour[2:-2]
    dirMap = {
        0: 'r',
        1: 'd',
        2: 'l',
        3: 'u',
    }
    dir = dirMap[int(colour[-2])]

    # direction = directions[dir]

    length = int(num, 16)
    # length = int(l)

    turns.append((dir, length))

lefts = []
rights = []
pos = (0,0)

for i in range(len(turns)):
    d, length = turns[i]
    direction = directions[d.lower()]
    if i == 0:
        prevTurn = turns[-1][0]
    else:
        prevTurn = turns[i-1][0]

    if i == len(turns)-1:
        nextTurn = turns[0][0]
    else:
        nextTurn = turns[i+1][0]

    pos = add(pos, scale(direction, length))
    minI = min(minI, pos[0])
    minJ = min(minJ, pos[1])
    maxI = max(maxI, pos[0])
    maxJ = max(maxJ, pos[1])

    clockwiseLength = antiClockwiseLength = length + 1

    if d == 'l':
        if prevTurn == 'u':
            clockwiseLength -= 1
        else:
            antiClockwiseLength -= 1

        if nextTurn == 'd':
            clockwiseLength -= 1
        else:
            antiClockwiseLength -= 1

        lefts.append((pos[0], clockwiseLength, antiClockwiseLength))
    elif d == 'r':
        if prevTurn == 'd':
            clockwiseLength -= 1
        else:
            antiClockwiseLength -= 1

        if nextTurn == 'u':
            clockwiseLength -= 1
        else:
            antiClockwiseLength -= 1

        rights.append((pos[0], clockwiseLength, antiClockwiseLength))

print(minI, minJ, maxI, maxJ)
print(pos)
print(rights, lefts)


area1 = 0
area2 = 0

for i, clockwiseLength, antiClockwiseLength in rights:
    area1 += (maxI - i + 1) * clockwiseLength
    area2 += (maxI - i + 1) * antiClockwiseLength

    print(i, clockwiseLength, (maxI - i + 1) * clockwiseLength)

for i, clockwiseLength, antiClockwiseLength in lefts:
    area1 -= (maxI - i) * clockwiseLength
    area2 -= (maxI - i) * antiClockwiseLength
    print(i, clockwiseLength, -((maxI - i) * clockwiseLength))

print(max(area1, area2))