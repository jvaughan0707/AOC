import math

from shared.utils import getInput

positions = getInput(7)[0]

values = list(map(int, positions.split(',')))

values.sort()

class Group:
    def __init__(self, x):
        self.x = x
        self.items = []
        self.size = 0

    def addItem(self, v):
        self.items.append(v)
        self.size += 1

def getGroups():
    groups = []
    for value in values:
        if not groups or groups[-1].x < value:
            groups.append(Group(value))
        groups[-1].addItem(value)
    return groups

def part1():
    cost = 0
    groups = getGroups()
    while groups[0].size < len(values) / 2:
        group1 = groups.pop(0)
        group2 = groups[0]

        cost += abs(group2.x - group1.x) * group1.size

        for item in group1.items:
            group2.addItem(item + 1)

    finalH = groups[0].x
    for group in groups[1:]:
        cost += abs(group.x - finalH) * group.size

    print(cost)

def getCost(start, end):
    diff = abs(end - start)
    return (diff * (diff + 1)) // 2

def part2():
    groups = getGroups()
    minCost = float('inf')
    for s in range(groups[0].x, groups[-1].x + 1):
        cost = sum([getCost(x, s) for x in values])
        print(s, cost)
        minCost = min(minCost, cost)

    print(minCost)

part2()