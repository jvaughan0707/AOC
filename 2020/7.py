from shared.utils import getInput

lines = getInput(7, __file__)

bagMap = {}

for line in lines:
    key, rest = line.split(' bags contain ')
    bagMap[key] = {}

    if rest.startswith('no'):
        continue
    for child in rest.split(', '):
        num, n1, n2, _ = child.split()
        bagMap[key][f'{n1} {n2}'] = int(num)

target = 'shiny gold'

targetMap = {}

def checkTarget(bag):
    if bag in targetMap:
        return targetMap[bag]
    
    result = False
    for child in bagMap[bag]:
        if child == target:
            result = True
        if checkTarget(child):
            result = True
        
    targetMap[bag] = result
    return result

countMap = {}

def getChildCount(bag):
    if bag in countMap:
        return countMap[bag]
    
    result = 0
    for child in bagMap[bag]:
        result += bagMap[bag][child] * (getChildCount(child) + 1)

    countMap[bag] = result
    return result

checkCount = 0
for b in bagMap:
    if checkTarget(b):
        checkCount += 1

print(checkCount)

print(getChildCount(target))