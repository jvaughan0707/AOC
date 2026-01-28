from shared.utils import expandWithPlaceholders

rawInput = '''638A
965A
780A
803A
246A'''
codes = rawInput.splitlines()
codeMap = {}

class KeyPad:
    def __init__(self, isNumeric):
        self.target = ''
        self.isNumeric = isNumeric

        if isNumeric:
            self.keyPositions = {'0': (3, 1)}
            for i in range(1,10):
                self.keyPositions[str(i)] = (2 - ((i - 1) // 3), (i - 1) % 3)
            self.keyPositions['A'] = (3, 2)
        else:
            self.keyPositions = {
                '^': (0, 1),
                '<': (1, 0),
                'v': (1, 1),
                '>': (1, 2),
                'A': (0, 2),
            }

        self.pos = self.keyPositions['A']
        self.positionKeys = {}
        for key in self.keyPositions:
            self.positionKeys[self.keyPositions[key]] = key

    def reset(self):
        self.pos = self.keyPositions['A']
        self.target = ''

    def expand(self, code):
        results = []
        for key in code:
            fromKey = self.positionKeys[self.pos]
            expanded = ''
            pos = self.keyPositions[key]
            if self.isNumeric and self.pos[0] == 3 and pos[1] == 0:
                expanded += '^' * (self.pos[0] - pos[0])
                expanded += '<' * (self.pos[1] - pos[1])
            elif self.isNumeric and pos[0] == 3 and self.pos[1] == 0:
                expanded += '>' * (pos[1] - self.pos[1])
                expanded += 'v' * (pos[0] - self.pos[0])
            elif key == '<':
                expanded += 'v' * (pos[0] - self.pos[0])
                expanded += '<' * (self.pos[1] - pos[1])
            elif fromKey == '<':
                expanded += '>' * (pos[1] - self.pos[1])
                expanded += '^' * (self.pos[0] - pos[0])
            else:
                expanded += '<' * (self.pos[1] - pos[1])
                expanded += 'v' * (pos[0] - self.pos[0])
                expanded += '^' * (self.pos[0] - pos[0])
                expanded += '>' * (pos[1] - self.pos[1])
            expanded += 'A'
            self.pos = pos
            results.append(expanded)

        return results

def expansionFunction(code):
    isNumeric = code[0] <= '9'
    keypad = KeyPad(isNumeric)
    return keypad.expand(code)

total = 0
for code in codes:
    length = expandWithPlaceholders([code], expansionFunction, 26)

    total += int(code[0:-1]) * length
    print(code, length, total)

print('final:', total)