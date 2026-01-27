from AOC.shared.utils import getInput, directions, up, down, left, right, isOob, add, scale
import sys
sys.setrecursionlimit(150000)

lines = getInput(16)
# print('\n'.join(lines))
nodes = {}

class Node:
    def __init__(self, symbol, pos):
        self.inputs = {
            up: False,
            down: False,
            left: False,
            right: False,
        }
        
        self.outputs = {
            up: False,
            down: False,
            left: False,
            right: False,
        }

        self.active = False
        self.symbol = symbol
        
        self.outputMap = {}
        if symbol == '.':
            self.outputMap[up] = 'd'
            self.outputMap[down] = 'u'
            self.outputMap[left] = 'r'
            self.outputMap[right] = 'l'
        elif symbol == '/':
            self.outputMap[up] = 'l'
            self.outputMap[left] = 'u'
            self.outputMap[down] = 'r'
            self.outputMap[right] = 'd'
        elif symbol == '\\':
            self.outputMap[up] = 'r'
            self.outputMap[right] = 'u'
            self.outputMap[down] = 'l'
            self.outputMap[left] = 'd'
        elif symbol == '-':
            self.outputMap[up] = 'lr'
            self.outputMap[down] = 'lr'
            self.outputMap[left] = 'r'
            self.outputMap[right] = 'l'
        elif symbol == '|':
            self.outputMap[up] = 'd'
            self.outputMap[down] = 'u'
            self.outputMap[left] = 'ud'
            self.outputMap[right] = 'ud'
            
        self.neighbours = {}
        for d in directions:
            dir = directions[d]
            if not isOob(lines, add(dir, pos)):
                self.neighbours[dir] = add(dir, pos)
                
    def setInput(self, dir):
        if self.inputs[dir]:
            return

        # print('setInput:', self, dir)

        self.inputs[dir] = True
        self.active = True
        for o in self.outputMap[dir]:
            outputDir = directions[o]
            if self.outputs[outputDir]:
                continue
            self.outputs[outputDir] = True
            if outputDir in self.neighbours:
                nodes[self.neighbours[outputDir]].setInput(scale(outputDir, -1))

    def __repr__(self):
        if self.active:
            return 'X'
        else:
            return self.symbol
        
height = len(lines)
width = len(lines[0])

def getCount(start, startDir):
    for i in range(height):
        for j in range(width):
            nodes[(i, j)] = Node(lines[i][j], (i, j))

    nodes[start].setInput(startDir)

    # print(nodes)
    # printGrid()

    total = 0

    for node in nodes.values():
        if node.active:
            total += 1

    return total

def printGrid():
    for i in range(height):
        row = ''
        for j in range(width):
            row += str(nodes[(i, j)])
        print(row)

maximum = 0

for i in range(height):
    print(i)
    maximum = max(maximum, getCount((i, 0), left), getCount((i, width - 1), right))

for j in range(width):
    print(j)
    maximum = max(maximum, getCount((0, j), up), getCount((height - 1, j), down))

print(maximum)

# printGrid()