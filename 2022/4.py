from shared.utils import getInput

lines = getInput(4)

def parseRange(text):
    return list(map(int, text.split('-')))

def compareRanges1(range1, range2):
    return range1[0] <= range2[0] <= range2[1] <= range1[1] or range2[0] <= range1[0] <= range1[1] <= range2[1]

def compareRanges2(range1, range2):
    return range1[0] <= range2[0] <= range1[1] or range2[0] <= range1[0] <= range2[1]

total1 = 0
total2 = 0
for line in lines:
    ranges = list(map(parseRange, line.split(',')))

    if compareRanges1(ranges[0], ranges[1]):
        total1 += 1

    if compareRanges2(ranges[0], ranges[1]):
        total2 += 1

print(total1, total2)

# > 521