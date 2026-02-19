from shared.utils import getInput

lines = list(map(int, getInput(9, __file__)))

preLength = 25

sums = [set() for _ in range(preLength)]

for a in range(preLength):
    for b in range(a + 1, preLength):
        total = lines[a] + lines[b]

        sums[b].add(total)

target = 0

def getTarget():
    for i in range(preLength, len(lines)):
        num = lines[i]

        valid = False

        for j in range(i - preLength, i):
            if num in sums[j]:
                valid = True
                break

        if not valid:
            return num

        sums.append([num + x for x in lines[i - preLength + 1: i]])

target = getTarget()

def matchTarget():
    for i in range(len(lines)):
        for l in range(1, len(lines) - i):
            total = sum(lines[i:i + l])
            if total == target:
                return min(lines[i:i + l]) + max(lines[i:i + l])
            
            if total > target:
                break

print(matchTarget())
