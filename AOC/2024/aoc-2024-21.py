rawInput = '''638A
965A
780A
803A
246A'''

codes = rawInput.splitlines()

codeMap = {}

class KeyPad:
    def __init__(self, isNumeric, child):
        self.target = ''
        self.parent = None
        self.child = child
        self.inputList = []
        self.isNumeric = isNumeric
        self.expandedLength = 0

        if child:
            child.parent = self

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
        self.expandedLength = 0

    def addTarget(self, target, previousTargets):
        print('addTarget:', target, previousTargets)
        self.target += target
        # print('addTarget:', target)

        if self.parent:
            if target[0] == '(':
                # "expanding" a placeholder e.g. (v<<)*4. Increase the counter.
                left, right = target.split('*')
                power = int(right[-1])
                power += 1
                code = left[1:-1]
                if previousTargets:
                    self.parent.addTarget(left + '*' + str(power), previousTargets + [previousTargets[-1]])
                else:
                    self.parent.addTarget(left + '*' + str(power), [target])
                # This should be in the length map so update the previous target lengths
                depth = 2
                for p in previousTargets:
                    if len(codeMap[p]) < depth + 1:
                        codeMap[p].append(0)
                    codeMap[p][depth] += codeMap[code][power]
                    if p == 'A':
                        print(codeMap[p], depth)
                    depth += 1

            elif target in codeMap:
                if previousTargets:
                    self.parent.addTarget('(' + target + ')*1', previousTargets + [previousTargets[-1]])
                else:
                    self.parent.addTarget('(' + target + ')*1', [target])
                depth = 2
                for p in previousTargets:
                    if len(codeMap[p]) < depth + 1:
                        codeMap[p].append(0)
                    codeMap[p][depth] += codeMap[target][1]
                    depth += 1
            else:
                codeMap[target] = [len(target)]

                for key in target:
                    expanded = ''
                    pos = self.keyPositions[key]
                    if self.isNumeric and self.pos[0] == 3 and pos[1] == 0:
                        expanded += '^' * (self.pos[0] - pos[0])
                        expanded += '<' * (self.pos[1] - pos[1])
                    elif key == '<' and self.pos == self.keyPositions['A']:
                        expanded += 'v<<'
                    else:
                        expanded += '<' * (self.pos[1] - pos[1])
                        expanded += 'v' * (pos[0] - self.pos[0])
                        expanded += '>' * (pos[1] - self.pos[1])
                        expanded += '^' * (self.pos[0] - pos[0])
                    expanded += 'A'
                    self.pos = pos
                    if not self.isNumeric:
                        depth = 1
                        for p in [target] + previousTargets:
                            if len(codeMap[p]) < depth + 1:
                                codeMap[p].append(0)
                            if len(codeMap[p]) < depth + 1:
                                print(p, codeMap[p], depth, target, previousTargets)
                            codeMap[p][depth] += len(expanded)
                            depth += 1

                        self.parent.addTarget(expanded, previousTargets+[target])
                    else:
                        self.parent.addTarget(expanded, [])
        else:
            if target[0] == '(':
                # "expanding" a placeholder e.g. (v<<)*4. Increase the counter.
                left, right = target.split('*')
                power = int(right[-1])
                code = left[1:-1]
                if len(codeMap[code]) < power + 1:
                    print(code, codeMap[code], target, previousTargets)
                self.expandedLength += codeMap[code][power]
            else:
                self.expandedLength += len(target)
    def doInput(self, key):
        self.inputList.append(key)
        if key == '^':
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif key == 'v':
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif key == '<':
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif key == '>':
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif key == 'A':
            if self.child:
                # print('child input:', self.positionKeys[self.pos], self.pos)
                self.child.doInput(self.positionKeys[self.pos])
            else:
                print(self.positionKeys[self.pos])



numberPad = KeyPad(True, None)
keypads = [numberPad]
for i in range(0, 3):
    keypads.append(KeyPad(False, keypads[-1]))

total = 0
for code in codes:
    for n in code:
        numberPad.addTarget(n, [])

    total += int(code[0:-1]) * keypads[-1].expandedLength
    # print(total)
    #
    for keypad in keypads:
        print(keypad.target, keypad.expandedLength)
        keypad.reset()

print('final:', total)

# print(codeMap)
#
# #
# for key in '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A':
#     keypads[-2].doInput(key)
#
# for keypad in keypads:
#     print(''.join(keypad.inputList))


# 238078