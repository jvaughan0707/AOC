from shared.utils import getInput

lines = getInput(10)

brackets = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

errorScore = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

completionScore = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def removeValid(line):
    positionsToRemove = []
    for i in range(len(line) - 1):
        c1 = line[i]
        c2 = line[i+1]
        if c1 in brackets:
            if c2 == brackets[c1]:
                positionsToRemove.append(i)
                positionsToRemove.append(i+1)

            elif c2 in brackets.values():
                return True, c2

    if not positionsToRemove:
        return False, line

    newLine = ''
    for i in range(len(line)):
        if i not in positionsToRemove:
            newLine += line[i]

    return removeValid(newLine)

autoCompleteScores = []
errorTotal = 0
for l in lines:
    isError, result = removeValid(l)

    if isError:
        errorTotal += errorScore[result]
    else:
        score = 0
        for b in reversed(result):
            close = brackets[b]
            score *= 5
            score += completionScore[close]
        autoCompleteScores.append(score)

print(errorTotal)
autoCompleteScores.sort()
print(autoCompleteScores[(len(autoCompleteScores)-1)// 2])