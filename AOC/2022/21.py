import re
from AOC.shared.utils import getInput, visualiseGraph

lines = getInput(21)
monkeys = {}

class Monkey:
    def __init__(self, name, job):
        self.name = name
        self.children = []
        self.job = job
        self.number = 0
        self.op = ''
        self.parent = None
        self.humanDependent = False
        self.target = 0

    def __repr__(self):
        return self.name

    def init(self):
        if re.match('\d+', self.job):
            self.number = int(self.job)
        else:
            left, op, right = self.job.split()
            self.children = [monkeys[left], monkeys[right]]
            for c in self.children:
                if c.parent:
                    print('monkey already has parent:', c, c.parent, self)
                else:
                    c.parent = self
            self.op = op

    def getValue(self):
        if not self.children:
            return self.number
        left = self.children[0].getValue()
        right = self.children[1].getValue()

        if self.op == '+':
            return left + right
        elif self.op == '*':
            return left * right
        elif self.op == '/':
            return left // right
        else:
            return left - right

for line in lines:
    m = Monkey(*line.split(': '))
    monkeys[m.name] = m

for m in monkeys.values():
    m.init()

# print(monkeys['root'].getValue())
#
# adjMap = { m: m.children  for m in monkeys.values()}
#
# visualiseGraph(adjMap)

human = monkeys['humn']
root = monkeys['root']

current = human
while current:
    current.humanDependent = True
    current = current.parent

root.op = '='

current = root
while current != human:
    print(current, current.children)
    value = 0
    nextChild = None
    for c in current.children:
        if c.humanDependent:
            nextChild = c
            continue

        value = c.getValue()

    if current.op == '=':
        nextChild.target = value
    elif current.op == '+':
        nextChild.target = current.target - value
    elif current.op == '*':
        nextChild.target = current.target // value
    elif current.op == '/':
        if nextChild == current.children[0]:
            nextChild.target = current.target * value
        else:
            nextChild.target = value // current.target
    elif current.op == '-':
        if nextChild == current.children[0]:
            nextChild.target = current.target + value
        else:
            nextChild.target = value - current.target

    current = nextChild

print(human.target)