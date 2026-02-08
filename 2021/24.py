from shared.utils import getInput

lines = getInput(24, __file__)

class Chunk:
    def __init__(self, inp):
        self.inp = inp
        self.instructions = []
        self.a = self.b = self.c = 0
        
        # inp w
        # z //= a
        # x = (z % 26 + b) != w
        # y = 25x + 1
        # z = z*y + (w + c)*x

    def addInstruction(self, op, v1, v2):
        self.instructions.append((op, v1, v2))
        l = len(self.instructions) + 1

        if l == 5:
            self.a = v2
        elif l == 6:
            self.b = v2
        elif l == 16:
            self.c = v2

    def run(self, variables, inp):
        variables = variables.copy()
        variables[self.inp] = inp
        for op, v1, v2 in self.instructions:
            if v2 in variables:
                v2 = variables[v2]

            if op == 'add':
                variables[v1] += v2
            elif op == 'mul':
                variables[v1] *= v2
            elif op == 'div':
                variables[v1] //= v2
            elif op == 'mod':
                variables[v1] %= v2
            elif op == 'eql':
                variables[v1] = int(variables[v1] == v2)
        return variables

chunks = []

for line in lines:
    s = line.split()

    op = s[0]
    v1 = s[1]

    if op == 'inp':
        chunks.append(Chunk(v1))
        continue

    v2 = s[2]
    if v2 not in 'wxyz':
        v2 = int(v2)

    chunks[-1].addInstruction(op, v1, v2)


def isViable(currentVars, inputPosition):
    currentZ = currentVars['z']
    if inputPosition >= 14:
        return currentZ == 0
    chunk = chunks[inputPosition]
    factor = int(chunk.a == 1) - int(chunk.b < 10)
    for t in range(1,10):
        newVars = chunk.run(currentVars, t)
        newZ = newVars['z']
        if newZ > 2 * currentZ * 26 ** factor:
            continue
        if isViable(newVars, inputPosition + 1):
            return True
        
    return False


def getMaxInput(currentVars, inputPosition):
    print('getMaxInput', currentVars, inputPosition)
    chunk = chunks[inputPosition]
    for t in reversed(range(1,10)):
        print('getMaxInput', currentVars, inputPosition, t)
        newVars = chunk.run(currentVars, t)

        if inputPosition == 13:
            if newVars['z'] == 0:
                return t
        elif isViable(newVars, inputPosition + 1):
            return int(str(t) + str(getMaxInput(newVars, inputPosition + 1)))
    
    return 0
        
def getMinInput(currentVars, inputPosition):
    print('getMinInput', currentVars, inputPosition)
    chunk = chunks[inputPosition]
    for t in range(1,10):
        print('getMinInput', currentVars, inputPosition, t)
        newVars = chunk.run(currentVars, t)

        if inputPosition == 13:
            if newVars['z'] == 0:
                return t
        elif isViable(newVars, inputPosition + 1):
            return int(str(t) + str(getMinInput(newVars, inputPosition + 1)))
    
    return 0

variables = {c: 0 for c in 'wxyz'}
maxInput = getMaxInput(variables, 0)

print(maxInput)
minInput = getMinInput(variables, 0)

print(minInput)

# testInput = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# for p, inp in enumerate(testInput):
#     chunk = chunks[p]
#     variables = chunk.run(variables, inp)
#     print(variables)

# for chunk in chunks:
#     print(chunk.a, chunk.b, chunk.c, chunk.a == 1, chunk.b < 10)


# inp w
# x = (z % 26 + 14) != w
# y = 25x + 1
# z = z*y + (w + 16)x

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 11
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 3
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 12
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 2
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 11
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 7
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -10
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 13
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 15
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
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -14
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 10
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 11
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -4
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
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -3
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 5
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 11
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -3
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 4
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -9
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 4
# mul y x
# add z y
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