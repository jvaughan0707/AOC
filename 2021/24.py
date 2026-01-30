from shared.utils import getInput

lines = getInput(24)

variables = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 15
}

inputs = [3] * 14
inputIndex = -1
for line in lines:
    s = line.split()

    op = s[0]
    v1 = s[1]
    if op == 'inp':
        inputIndex += 1
        variables[v1] = inputs[inputIndex]
        continue

    v2 = s[2]
    value = int(v2) if v2 not in variables else variables[v2]

    if op == 'add':
        variables[v1] += value
    elif op == 'mul':
        variables[v1] *= value
    elif op == 'div':
        variables[v1] //= value
    elif op == 'mod':
        variables[v1] %= value
    elif op == 'eql':
        variables[v1] = int(variables[v1] == value)

    print(variables, inputIndex)


# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -12
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 6
# mul y x
# add z y