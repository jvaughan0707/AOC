from numpy.ma.extras import dstack

from AOC.shared.utils import getInput

lines = getInput(8)

digitDisplays = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]

digitCounts = {i: 0 for i in range(len(digitDisplays))}

for line in lines:
    patterns, output = line.split(' | ')
    patterns = patterns.split(' ')
    output = output.split(' ')

    for output in output:
        for i in [1,4,7,8]:
            if len(output) == len(digitDisplays[i]):
                digitCounts[i] += 1

print(sum(digitCounts[i] for i in [1,4,7,8]))

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

def diff(p1, p2):
    pos = ''

    for c in p1:
        if c not in p2:
            pos += c

    return pos

def findMatch(patterns, length, included = '', missingOneOf = ''):
    for pattern in patterns:
        if length != len(pattern):
            continue
        if not all([x in pattern for x in included]):
            continue
        if not missingOneOf or any([x not in pattern for x in missingOneOf]):
            return pattern

def getCorrectionMap(patterns):
    patterns.sort(key=len)

    a = diff(patterns[1], patterns[0])
    bd = diff(patterns[2], patterns[1])
    cf = patterns[0]

    six = findMatch(patterns, 6, '', cf)
    zero = findMatch(patterns, 6, '', bd)
    nine = findMatch(patterns, 6, bd + cf)

    eight = findMatch(patterns, 7)

    e = diff(eight, nine)
    c = diff(eight, six)
    d = diff(eight, zero)
    b = diff(bd, d)
    f = diff(cf, c)
    g = diff(eight, a+b+c+d+e+f)

    return {
        a: 'a',
        b: 'b',
        c: 'c',
        d: 'd',
        e: 'e',
        f: 'f',
        g: 'g',
    }

total = 0
for line in lines:
    patterns, outputs = line.split(' | ')
    patterns = patterns.split(' ')
    outputs = outputs.split(' ')
    m = getCorrectionMap(patterns)

    outputString = ''
    for output in outputs:
        mappedOutput = ''
        for x in output:
            mappedOutput += m[x]

        mappedOutput = ''.join(sorted(mappedOutput))
        outputString += str(digitDisplays.index(mappedOutput))

    print(outputString)
    total += int(outputString)

print(total)