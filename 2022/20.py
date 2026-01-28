from shared.utils import getInput

lines = getInput(20)

numbers = list(map(int, lines))

print(numbers)

class Number:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return str(self.number)

readList = []
writeList = []
zeroNum = None

for x in numbers:
    n = Number(x)
    readList.append(n)
    writeList.append(n)
    if x == 0:
        zeroNum = n

def mix(rounds, key = 1):
    for r in range(rounds):
        for num in readList:
            index = writeList.index(num)
            writeList.remove(num)
            newIndex = (index + num.number * key) % len(writeList)
            writeList.insert(newIndex, num)

        print(writeList)

    total = 0
    zeroIndex = writeList.index(zeroNum)
    for i in range(1,4):
        total += writeList[(zeroIndex + i * 1000) % len(writeList)].number

        # print(writeList[(zeroIndex + i * 1000) % len(writeList)].number)
    return total * key

print(mix(10, 811589153))



