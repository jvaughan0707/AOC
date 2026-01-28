from shared.utils import getSectionsInput, getNumbers, sub, add, scale, isCollinear

sections = getSectionsInput(19)

def getDistParts(p1, p2):
    return tuple(sorted([abs(p1[i] - p2[i]) for i in range(len(p1))]))

class Scanner:
    def __init__(self, section):
        self.pos = (0, 0, 0)
        self.id = getNumbers(section[0])[0]

        self.beacons = [
            tuple(map(int, l.split(','))) for l in section[1:]
        ]

        self.pairDistances = {}

    def processPoints(self):
        self.pairDistances = {}
        for b1 in self.beacons:
            for b2 in self.beacons:
                if b1 <= b2:
                    continue
                self.pairDistances[b1, b2] = getDistParts(b1, b2)

    def __repr__(self):
        return str(self.id)

scanners = []
for s in sections:
    scanner = Scanner(s)
    scanner.processPoints()
    scanners.append(scanner)

unlockedScanners = scanners[1:]
lockedScanners = scanners[:1]

def getPairsCount(nodesCount):
    return nodesCount * (nodesCount - 1) // 2

targetPairsCount = getPairsCount(12)

def relabelAxes(axesMap, point):
    l = []
    for i, m in enumerate(axesMap):
        d = abs(m) - 1
        v = point[d]
        if m < 0:
            v = -v

        l.append(v)

    return tuple(l)

def transform(targetScanner, matchedPairs):
    # Find 2 lines in the source map which:
    # * share one common point (a1)
    # * are not collinear
    # * have unique non-zero difference in each coordinate e.g. not (1, -1, 2) or (1, 2, 0)

    # When the loop completes we will have a1, and it's corresponding mapped point a2.
    # Also, a vector d1 and the corresponding vector in the mapped space - d2
    d1 = d2 = None
    a1 = a2 = None
    for p1 in matchedPairs:
        if len(matchedPairs[p1]) != 1:
            continue
        d1Parts = getDistParts(*p1)
        if not all([x != 0 and d1Parts.count(x) == 1 for x in d1Parts]):
            continue

        for p2 in matchedPairs:
            if p1 == p2:
                continue

            if len(matchedPairs[p2]) != 1:
                continue
            if p1[0] not in p2:
                continue

            if isCollinear(sub(*p1), sub(*p2)):
                continue

            a1, b1 = p1
            # identify which of the mapped points in p1 corresponds to a1 (it must belong to both of the mapped lines)
            a2, b2 = matchedPairs[p1][0]
            if a2 not in matchedPairs[p2][0]:
                a2, b2 = b2, a2

            d1 = sub(a1, b1)
            d2 = sub(a2, b2)

            break

        if d1 and d2:
            break

    if not d1 or not d2:
        raise Exception('No matching pairs')

    # d1 = (X, Y, Z)
    # d2 = (-Y, Z, X) for example

    # each position of the axes map is a 1-indexed position of the corresponding coordinate in d2 space
    # (a negative indicates that the axis should be flipped)
    # in the above example this will be [-2, 3, 1]
    axesMap = [d2.index(c) + 1 if c in d2 else -1 -d2.index(-c) for c in d1]

    translation = sub(a1, relabelAxes(axesMap, a2))

    newPoints = []
    for b in targetScanner.beacons:
        newPoints.append(add(relabelAxes(axesMap, b), translation))

    targetScanner.beacons = newPoints
    targetScanner.pos = translation
    targetScanner.processPoints()

def checkMatch(lockedScanner, unlockedScanner):
    matchedPairs = {}

    for p1, d1 in lockedScanner.pairDistances.items():
        for p2, d2 in unlockedScanner.pairDistances.items():
            if d1 != d2:
                continue

            if p1 not in matchedPairs:
                matchedPairs[p1] = []
            matchedPairs[p1].append(p2)

    if len(matchedPairs) < targetPairsCount:
        return False

    transform(unlockedScanner, matchedPairs)

    return True

t = 0
while unlockedScanners and t < len(scanners):
    match = None
    for s1 in lockedScanners:
        for s2 in unlockedScanners:
            if s1 == s2:
                continue

            if checkMatch(s1, s2):
                match = s2
                break

    if match:
        lockedScanners.append(match)
        unlockedScanners.remove(match)

    t += 1

allPoints = set()
for scanner in scanners:
    for beacon in scanner.beacons:
        allPoints.add(beacon)

print(len(allPoints))
maxDist = 0
for s1 in scanners:
    for s2 in scanners:
        if s1 == s2:
            continue
        maxDist = max(maxDist, sum(getDistParts(s1.pos, s2.pos)))

print(maxDist)