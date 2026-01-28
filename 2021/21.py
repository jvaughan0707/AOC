from shared.utils import getInput, getNumbers

lines = getInput(21)

players = []
playerTurnStateCounts = []

for line in lines:
    startState = [getNumbers(line)[1], 0]
    players.append(startState)
    playerTurnStateCounts.append([{'w': 0, 'l': 1, tuple(startState): 1}])

player = 0
diceValue = 0
trackLength = 10
diceMax = 100

rollCount = 0

def getRollTotal():
    global diceValue
    global rollCount

    total = 0
    for i in range(3):
        diceValue +=1
        if diceValue > diceMax:
            diceValue = 1
        total += diceValue
        rollCount += 1
    return total

maxScore = 0
while maxScore < 1000:
    players[player][0] += getRollTotal() - 1
    players[player][0] %= trackLength
    players[player][0] += 1

    players[player][1] += players[player][0]
    maxScore = max(maxScore, players[player][1])
    player += 1
    player %= 2

print(players, rollCount)

print(players[player][1] * rollCount)

diceFrequencies = {x: 0 for x in range(3, 10)}

for i in range(1,4):
    for j in range(1,4):
        for k in range(1,4):
            diceFrequencies[i+j+k] += 1
freqTotal = sum(diceFrequencies.values())


def mergeCounts(current, new):
    for key in new.keys():
        if key not in current:
            current[key] = new[key]
        else:
            current[key] += new[key]

def getNextStates(currentState, weight):
    nextStates = {'w': 0, 'l': 0}
    for d in diceFrequencies:
        nextSpace = ((currentState[0] + d) - 1) % trackLength + 1
        nextScore = currentState[1] + nextSpace
        if nextScore >= 21:
            mergeCounts(nextStates, {'w': diceFrequencies[d] * weight})
        else:
            mergeCounts(nextStates, {(nextSpace, nextScore): diceFrequencies[d] * weight, 'l': diceFrequencies[d] * weight})

    return nextStates

player = 0
turn = 1

while turn <= 10:
    prevStateCount = playerTurnStateCounts[player][turn - 1]

    nextStateCount = {'w': 0, 'l': 0}

    for s in prevStateCount:
        if s in ['w', 'l']:
            continue
        prevTurn = turn - 1 if player == 0 else turn
        weight = prevStateCount[s] * playerTurnStateCounts[player ^ 1][prevTurn]['l'] // playerTurnStateCounts[player][turn - 1]['l']

        mergeCounts(nextStateCount, getNextStates(s, weight))

    playerTurnStateCounts[player].append(nextStateCount)

    player ^= 1

    if player == 0:
        turn += 1


sumA = sumB = 0

for t in playerTurnStateCounts[0]:
    sumA += t['w']

print()
for t in playerTurnStateCounts[1]:
    sumB += t['w']

print(max(sumA, sumB))
