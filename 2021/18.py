import json
from copy import deepcopy

from shared.utils import getInput

inputLines = getInput(18)

def add(left, right):
    if not left:
        return right
    if not right:
        return left

    left = deepcopy(left)
    right = deepcopy(right)

    return reduce([left,right])

current = None

def reduce(pair):
    prevRegNum = None
    pairToExplode = None
    numToSplit = None
    exploded = False

    def explore(item, depth = 0):
        nonlocal prevRegNum
        nonlocal pairToExplode
        nonlocal numToSplit
        nonlocal exploded

        if exploded:
            return

        a, b = item
        # print('explore', a,b, depth, prevRegNum)

        if depth == 4 and not pairToExplode:
            pairToExplode = item
            # print('explode', item, prevRegNum)
            if prevRegNum:
                # print(prevRegNum[0][prevRegNum[1]], '+', a)
                prevRegNum[0][prevRegNum[1]] += a

        if not exploded and prevRegNum and pairToExplode is prevRegNum[0] and type(a) == int:
            # print(item[0], '+', pairToExplode[1])
            item[0] += pairToExplode[1]
            exploded = True
            return

        if not numToSplit:
            if type(a) == int and int(a) > 9:
                numToSplit = (item, 0)

        if type(a) == int:
            prevRegNum = (item, 0)
        else:
            explore(a, depth + 1)

            if pairToExplode is a:
                # print('pairToExplode', pairToExplode, a, item)
                item[0] = 0

        if not exploded and prevRegNum and pairToExplode is prevRegNum[0] and pairToExplode is not item and type(b) == int:
            # print(item[1], '+', pairToExplode[1])
            item[1] += pairToExplode[1]
            exploded = True
            return

        if not numToSplit:
            if type(b) == int and int(b) > 9:
                numToSplit = (item, 1)

        if type(b) == int:
            prevRegNum = (item, 1)
        else:
            explore(b, depth + 1)

            if pairToExplode is b:
                # print('pairToExplode', pairToExplode, b, item)
                item[1] = 0

    explore(pair)

    if pairToExplode:
        reduce(pair)
    elif numToSplit:
        location, pos = numToSplit
        value = location[pos]
        location[pos] = [value // 2, (value + 1) // 2]
        reduce(pair)

    return pair

pairs = []
for l in inputLines:
    p = json.loads(l)
    pairs.append(p)

    current = add(current, p)

print(current)

def getMagnitude(pair):
    if type(pair) == int:
        return pair
    return 3 * getMagnitude(pair[0]) + 2 * getMagnitude(pair[1])

print(getMagnitude(current))

maxValue = 0

def getSumValue(p1, p2):
    return getMagnitude(add(p1, p2))

for x in pairs:
    for y in pairs:
        if x is y:
            continue
        maxValue = max(maxValue, getSumValue(x, y))
        maxValue = max(maxValue, getSumValue(y, x))

print(maxValue)

