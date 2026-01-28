from shared.utils import getSectionsInput, normalise
import json

pairs = getSectionsInput(13)

def compare(left, right):
    if type(left) == int and type(right) == int:
        return normalise(left - right)
    elif type(left) == int:
        return compare([left], right)
    elif type(right) == int:
        return compare(left, [right])
    else:
        for i in range(min(len(left), len(right))):
            res = compare(left[i], right[i])
            if res != 0:
                return res
        return normalise(len(left) - len(right))

i = 1
total = 0
packets = []

for pair in pairs:
    left, right = list(map(json.loads, pair))
    packets.extend([left, right])
    if compare(left, right) == -1:
        total += i
    i += 1

print(total)

d1 = [[2]]
d2 = [[6]]

d1Index = 1
d2Index = 2

for p in packets:
    if compare(d1, p) == 1:
        d1Index += 1
    if compare(d2, p) == 1:
        d2Index += 1

print(d1Index * d2Index)

