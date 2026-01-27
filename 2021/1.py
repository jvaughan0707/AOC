from AOC.shared.utils import getInput

lines = getInput(1)

numbers = [int(x) for x in lines]
def getSum(size):
    total = 0
    for i in range(0, len(numbers) - size):
        if sum(numbers[i:i+size]) < sum(numbers[i+1:i+size+1]):
            total += 1

    return total

# > 1389
print(getSum(3))