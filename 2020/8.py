from shared.utils import getInput
from copy import deepcopy

lines = getInput(8, __file__)

defaultInstructions = []

nops = set()
jmps = set()

for i, line in enumerate(lines):
    ins, arg = line.split()
    arg = int(arg)
    defaultInstructions.append([ins, arg])
    if ins == 'jmp':
        jmps.add(i)
    elif ins == 'nop':
        nops.add(i)

def runProgram(instructions):
    index = 0
    acc = 0
    visitedInstructions = set()

    while index not in visitedInstructions:
        if index >= len(instructions):
            return (acc, index)
        
        ins, arg = instructions[index]
        visitedInstructions.add(index)

        if ins == 'nop':
            index += 1
        elif ins == 'acc':
            index += 1
            acc += arg
        elif ins == 'jmp':
            index += arg

    return (acc, index)

# print(runProgram(defaultInstructions))

stop = False
for j in jmps:
    instructionsCopy = deepcopy(defaultInstructions)
    instructionsCopy[j][0] = 'nop'
    (finalAcc, finalIndex) = runProgram(instructionsCopy)

    if finalIndex == len(instructionsCopy):
        stop = True
        print(finalAcc)
        break

if not stop:
    for n in nops:
        instructionsCopy = defaultInstructions.copy()
        instructionsCopy[n][0] = 'jmp'
        (finalAcc, finalIndex) = runProgram(instructionsCopy)

        if finalIndex == len(instructionsCopy):
            stop = True
            print(finalAcc)
            break