from shared.utils import getInput

numbers = list(map(int, getInput(10, __file__)))

numbers.sort()

numbers.insert(0,0)
numbers.append(numbers[-1] + 3)

diffCounts = { i: 0 for i in range(1,4)}
print(numbers)
for i in range (1, len(numbers)):
    diff = numbers[i] - numbers[i-1]
    diffCounts[diff] += 1

print(diffCounts)

print(diffCounts[1] * diffCounts[3])

cache = {}

def getCombinations(partialList):
    cacheKey = tuple(partialList)

    if cacheKey in cache:
        return cache[cacheKey]
    
    if len(partialList) < 2:
        return 1
    if partialList[0] < partialList[1] - 3:
        return 0
    if len(partialList) < 3:
        return 1
    
    result = getCombinations(partialList[1:]) + getCombinations([partialList[0]] + partialList[2:])
    cache[cacheKey] = result
    return result

print(getCombinations(numbers))