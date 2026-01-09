from AOC.shared.utils import getSectionsInput

cratesInput, instructionsInput = getSectionsInput(5)

stacks = {}

for i in range(len(cratesInput[-1])):
    if cratesInput[-1][i] != ' ':
        stack = []
        stacks[int(cratesInput[-1][i])] = stack
        for j in range(len(cratesInput) - 1):
            row = len(cratesInput) - 2 - j
            if i < len(cratesInput[row]) and cratesInput[row][i] != ' ':
                stack.append(cratesInput[row][i])

for instruction in instructionsInput:
    parts = instruction.split(' ')
    size = int(parts[1])
    source = int(parts[3])
    target = int(parts[5])

    # part 1
    # for s in range(size):
    #     item = stacks[source].pop()
    #     stacks[target].append(item)

    # part 2
    items = stacks[source][-size:]
    stacks[source] = stacks[source][:-size]
    stacks[target].extend(items)

print(''.join([s[-1] for s in stacks.values()]))