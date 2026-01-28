from shared.utils import getInput

lines = getInput(3)

combined = [0] * len(lines[0])

for line in lines:
    for i, x in enumerate(line):
        combined[i] += int(x)

print(combined)

gamma = ['1' if t > len(lines)/2 else '0' for t in combined]
epsilon = ['1' if t < len(lines)// 2 else '0' for t in combined]

print(gamma, epsilon)

gamma = int(''.join(gamma), 2)
epsilon = int(''.join(epsilon), 2)

print(gamma, epsilon)
print(gamma * epsilon)

def filterMostCommon():
    numbers = lines.copy()
    i = 0
    while len(numbers) > 1:
        total = sum([int(l[i]) for l in numbers])
        mostCommon = '1' if total >= len(numbers) / 2 else '0'

        print('mostCommon', mostCommon, numbers)
        numbers = list(filter(lambda l: l[i] == mostCommon, numbers))
        i += 1
    return numbers[0]


def filterLeastCommon():
    numbers = lines.copy()
    i = 0
    while len(numbers) > 1:
        total = sum([int(l[i]) for l in numbers])
        leastCommon = '0' if total >= len(numbers) / 2 else '1'
        print('leastCommon', leastCommon, numbers)

        numbers = list(filter(lambda l: l[i] == leastCommon, numbers))
        i+= 1
    return numbers[0]

a = filterMostCommon()
b = filterLeastCommon()

print(a, b)

a = int(a, 2)
b = int(b, 2)
print(a, b)
print(a * b)
