from AOC.shared.utils import getInput

lines = getInput(3)


def priority(letter):
    if letter >= 'a':
        return ord(letter) - ord('a') + 1
    else:
        return ord(letter) - ord('A') + 27

def getCommonItem(group):
    sets = {s: set() for s in group}

    for i in range(max(len(s) for s in group)):
        for s in group:
            if i >= len(s):
                continue
            sets[s].add(s[i])

            if all(s[i] in t for t in sets.values()):
                return s[i]

total = 0
for line in lines:
    half = len(line) // 2

    l, r = line[:half], line[half:]

    item = getCommonItem([l, r])

    total += priority(item)

print(total)

total = 0

for i in range(len(lines) // 3):
    group = lines[i * 3:(i + 1) * 3]
    common = getCommonItem(group)
    total += priority(common)

print(total)