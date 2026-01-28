from shared.utils import getInput, getNumbers

lines = getInput(15)

minY = minX = float('inf')
maxX = maxY = 0
grid = {}
sensorBeacons = {}

for line in lines:
    m = getNumbers(line)
    grid[(m[0], m[1])] = 'S'
    grid[(m[2], m[3])] = 'B'

    sensorBeacons[(m[0], m[1])] = (m[2], m[3])

impossiblePoints= set()

def pq(x,y):
    return x+y, x-y

def xy(p, q):
    return (p + q) // 2, (p - q) // 2

squares = []
for s, b in sensorBeacons.items():
    dist = abs(b[0] - s[0]) + abs(b[1] - s[1])

    minX = min(minX, s[0] - dist)
    maxX = max(maxX, s[0] + dist)
    minY = min(minY, s[1] - dist)
    maxY = max(maxY, s[1] + dist)

    p, q = pq(*s)
    squares.append(((p - dist, q - dist), (p + dist, q + dist)))

    # for d in range(dist + 1):
    #     for i in range(d):
    #         impossiblePoints.add((s[0] + i, s[1] + (d - i)))
    #         impossiblePoints.add((s[0] - i, s[1] - (d - i)))
    #
    #         impossiblePoints.add((s[0] + (d - i), s[1] - i))
    #         impossiblePoints.add((s[0] - (d - i), s[1] + i))

def printGrid1():
    for i in range(minY, maxY):
        row = ''
        for j in range(minX, maxX + 1):
            p = (j, i )
            if p in grid:
                row += grid[p]
            elif p in impossiblePoints:
                row += '#'
            else:
                row += '.'
        row += str(i)
        print(row)

# printGrid1()
print()

def getImpossiblePointsInRow(targetY):
    counter = 0
    for j in range(minX, maxX + 1):
        p = (j, targetY)
        if p in grid:
            continue
        for s, b in sensorBeacons.items():
            bDist = abs(b[0] - s[0]) + abs(b[1] - s[1])
            pDist = abs(p[0] - s[0]) + abs(p[1] - s[1])

            if pDist <= bDist:
                counter += 1
                break

    print(counter)

pSolLines = []
qSolLines = []

for s1 in squares:
    for s2 in squares:
        if s1 == s2:
            continue

        if s1[0][0] == s2[1][0] + 2:
            maxQ = min(s1[1][1], s2[1][1])
            minQ = max(s1[0][1], s2[0][1])
            pSolLines.append((s2[1][0] + 1, [minQ, maxQ]))
        elif s1[0][1] == s2[1][1] + 2:
            maxP = min(s1[1][0], s2[1][0])
            minP = max(s1[0][0], s2[0][0])
            qSolLines.append((s2[1][1] + 1, [minP, maxP]))

print(pSolLines)
print(qSolLines)

for pl in pSolLines:
    for ql in qSolLines:
        if ql[1][0] <= pl[0] <= ql[1][1] and pl[1][0] <= ql[0] <= pl[1][1]:
            print(pl[0], ql[0])
            x, y = xy(pl[0], ql[0])
            print(4000000 * x + y)
            break

