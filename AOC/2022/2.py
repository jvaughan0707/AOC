from AOC.shared.utils import getInput

lines = getInput(2)

inputMap = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'R',
    'Y': 'P',
    'Z': 'S',
}

shapeScore = {
    'R': 1,
    'P': 2,
    'S': 3,
}

total = 0

for line in lines:
    opponent, me = list(map(lambda x: inputMap[x], line.split()))

    score = shapeScore[me]

    if opponent == me:
        score += 3
    elif (shapeScore[opponent] + 1) % 3 == shapeScore[me] % 3:
        score += 6

    total += score

print(total)

shapes = ['S', 'R', 'P']

total = 0
for line in lines:
    opponent = inputMap[line.split()[0]]
    outcome =  line.split()[1]

    score = 0
    if outcome == 'X':
        shape = shapes[(shapeScore[opponent] + 2) % 3]
    elif outcome == 'Y':
        score += 3
        shape = shapes[(shapeScore[opponent]) % 3]
    else:
        score += 6
        shape = shapes[(shapeScore[opponent] + 1) % 3]

    score += shapeScore[shape]

    total += score

print(total)