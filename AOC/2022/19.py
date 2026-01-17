from AOC.shared.utils import getInput, getNumbers, sub

lines = getInput(19)

class Blueprint:
    def __init__(self, numbers):
        self.id = numbers[0]

        self.robotCosts = [
            (numbers[1], 0, 0, 0),
            (numbers[2], 0, 0, 0),
            (numbers[3], numbers[4], 0, 0),
            (numbers[5], 0, numbers[6], 0),
        ]

blueprints = []
for line in lines:
    numbers = getNumbers(line)
    blueprints.append(Blueprint(numbers))

def canAfford(cost, resources):
    return min(list(sub(resources, cost))) >= 0


def getMaxScore(bp, maxTime):
    currentMax = 0
    robotStateCache = {}

    def getUpperBound(robots, resources, remainingTime):
        robots = robots.copy()
        resources = resources.copy()
        for t in range(remainingTime):
            for i, r in enumerate(robots):
                resources[i] = resources[i] + r

            for i in range(3):
                if canAfford(bp.robotCosts[i], resources):
                    robots[i] = robots[i] + 1
            resources[2] = resources[2] + robots[2]

            if canAfford(bp.robotCosts[3], resources):
                robots[3] = robots[3] + 1
                resources = list(sub(resources, bp.robotCosts[3]))
        return resources[3]

    def exploreDecisionTree(robots, resources, remainingTime):
        nonlocal currentMax

        cacheKey = tuple(robots)
        if cacheKey not in robotStateCache:
            robotStateCache[cacheKey] = [(remainingTime, resources)]
        else:
            for prevState in robotStateCache[cacheKey]:
                if prevState[0] >= remainingTime and min(sub(prevState[1], resources)) >= 0:
                    return
            robotStateCache[cacheKey].append((remainingTime, resources))
        newResources = resources.copy()

        if remainingTime == 0:
            currentMax = max(currentMax, resources[3])
            return

        # get upper bound & prune
        upperBound = getUpperBound(robots, newResources, remainingTime)

        if currentMax > upperBound:
            return
        # print(robots, resources, maxTime - remainingTime, currentMax, upperBound)

        for i, r in enumerate(robots):
            newResources[i] = newResources[i] + r

        for i in reversed(range(len(bp.robotCosts))):
            c = bp.robotCosts[i]
            if not canAfford(c, resources):
                continue
            # if newResources[i] > 2 * max([cost[i] for cost in bp.robotCosts]):
            #     continue
            if i < 3 and robots[i] > max([cost[i] for cost in bp.robotCosts]):
                # income never needs to exceed the max cost for that resource
                continue

            newRobots = robots.copy()

            remainingResources = list(sub(newResources, c))

            newRobots[i] = newRobots[i] + 1

            exploreDecisionTree(newRobots, remainingResources, remainingTime - 1)

            if i == 3:
                # if we can make geode robot, don't consider other options
                return

            # if i == 2:
            #     break

        exploreDecisionTree(robots, newResources, remainingTime - 1)

    exploreDecisionTree([1, 0, 0, 0], [0, 0, 0, 0], maxTime)
    return currentMax

total = 0

# for bp in blueprints:
#     maxScore = getMaxScore(bp, 24)
#     print(bp.id, maxScore)
#     total += bp.id * maxScore
#
# print(total)

product = 1
for bp in blueprints[:3]:
    maxScore = getMaxScore(bp, 32)
    print(bp.id, maxScore)
    product *= maxScore

print(product)

# > 85840