from fractions import Fraction
from AOC.shared.utils import getInput, sub, add, scale

inputs = getInput(24)
inf = float('inf')

testRange = [200000000000000, 400000000000000]
class Stone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        px, py, pz = position
        vx, vy, vz = velocity

        maxTx = maxTy = inf
        minTx = minTy = 0

        if vx != 0:
            maxTx = max((b - px) / vx for b in testRange)
            minTx = min((b-px) / vx for b in testRange)
        if vy != 0:
            maxTy = max((b - py) / vy for b in testRange)
            minTy = min((b - py) / vy for b in testRange)

        self.maxT = min(maxTx, maxTy)
        self.minT = max(minTx, minTy, 0)

        self.end = (px + self.maxT * vx, py + self.maxT * vy)

    def __repr__(self):
        return f'{tuple(map(int, self.position))}, {tuple(map(int, self.velocity))}'

stones = []
for inputLine in inputs:
    pos, vel = inputLine.split(' @ ')
    stones.append(Stone(tuple(map(Fraction, pos.split(', '))), tuple(map(Fraction, vel.split(', ')))))

# part 1
def getIntersections():
    intersections = []
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            s1 = stones[i]
            s2 = stones[j]

            vx1, vy1, vz1 = s1.velocity
            vx2, vy2, vz2 = s2.velocity
            px1, py1, pz1 = s1.position
            px2, py2, pz2 = s2.position

            maxT1 = s1.maxT
            maxT2 = s2.maxT
            minT1 = s1.minT
            minT2 = s2.minT

            if vy1 == 0:
                t2 = (py1 - py2) / vy2
            else:
                c = vx1 / vy1
                if vx2 - c * vy2 == 0:
                    if px1 - c * py1 - px2 + c * py2 == 0:
                        # parallel, infinite intersections
                        intersections.append((s1, s2))
                        continue
                    else:
                        #parallel - no intersections
                        # print('parallel')
                        continue
                t2 = (px1 - c * py1 - px2 + c * py2) / (vx2 - c * vy2)

            # print(t2)
            if t2 > maxT2 or t2 < minT2:
                continue
            t1 = (px2 - px1 + vx2 * t2) / vx1
            # print(t1)
            if t1 > maxT1 or t1 < minT1:
                continue
            intersections.append((s1, s2))
            print(float(px1 + vx1 * t1), float(py1 + vy1 * t1))
            print(float(px2 + vx2 * t2), float(py2 + vy2 * t2))
    print(len(intersections))

# get a pair of stones with matching z velocities
def getMatchingPair():
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            s1 = stones[i]
            s2 = stones[j]
            if s1.velocity[2] == s2.velocity[2]:
                return s1, s2
    return None

def setReferenceFrame(refStone):
    for stone in stones:
        if stone != refStone:
            stone.position = sub(stone.position, refStone.position)
            stone.velocity = sub(stone.velocity, refStone.velocity)

def getPlaneThroughOrigin(baseLine):
    x0, y0, z0 = baseLine.position
    a1 = baseLine.velocity[1]
    a2 = -baseLine.velocity[0]
    a3 = a1 * x0 + a2 * y0

    # baseLine is described by 2 equations:
    # a1 * x + a2 * y = a3
    # z = z0 (z is constant since we chose a pair with same z velocity)

    # the plane through the origin and the baseLine will be:
    # a * x + b * y + z = 0
    # (for some values a and b to be found)
    a = - z0 * a1 / a3
    b = -z0 * a2 / a3
    return a, b, 1

def getIntersection(stone, plane):
    a, b, c = plane
    px, py, pz = stone.position
    vx, vy, vz = stone.velocity
    t = (-a * px - b * py - c * pz)/(a*vx + b*vy + c*vz)

    return add(stone.position, scale(stone.velocity, t)), t

def getSolutionLine():
    s0, s1 = getMatchingPair()
    setReferenceFrame(s0)

    # solution line must lie on a plane containing the origin and s1 line
    plane = getPlaneThroughOrigin(s1)

    # pick a new stone s2 which is different from s0 and s1
    s2 = None
    for stone in stones:
        if stone not in (s0, s1):
            s2 = stone
            break

    # s2 intersection will be a point on the plane, the final solution line must pass through the origin and this point
    s2Intersection, s2IntersectionTime = getIntersection(s2, plane)

    # all intersections will be some multiple of the above vector. For s1 we scale it by the ratio of z co-ordinates
    s1Intersection = scale(s2Intersection, s1.position[2] / s2Intersection[2])
    s1IntersectionTime = (s1Intersection[0] - s1.position[0]) / s1.velocity[0]

    # now we know 2 intersection points and their times, we can work out initial position and velocity
    velocity = scale(sub(s2Intersection, s1Intersection), 1 / (s2IntersectionTime - s1IntersectionTime))
    initialPosition = sub(s2Intersection, scale(velocity, s2IntersectionTime))

    # revert to original reference frame
    velocity = add(velocity, s0.velocity)
    initialPosition = add(initialPosition, s0.position)

    return initialPosition, velocity

solution = getSolutionLine()
print(solution)

print(sum(p for p in solution[0]))
