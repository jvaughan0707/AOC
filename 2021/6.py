from shared.utils import getInput,expandWithPlaceholders

line = getInput(6)[0]

initialState = list(map(int, line.split(',')))

def expand(n):
    if n == 0:
        return [6,8]
    else:
        return [n - 1]

print(expandWithPlaceholders(initialState, expand, 256, lambda x: 1))