from AOC.shared.utils import getSectionsInput

lcm = 1

class Monkey:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.test = None
        self.divisor = 1
        self.passNext = None
        self.failNext = None
        self.counter = 0

    def __repr__(self):
        return str(self.id)

    def setTest(self, operation):
        op, val = operation
        if val == 'old':
            if op == '+':
                self.test = lambda x: x + x
            else:
                self.test = lambda x: x * x
        else:
            if op == '+':
                self.test = lambda x: x + int(val)
            else:
                self.test = lambda x: x * int(val)

    def process(self):
        for item in self.items:
            self.counter += 1
            newValue = self.test(item)
            newValue %= lcm

            if newValue % self.divisor == 0:
                self.passNext.items.append(newValue)
            else:
                self.failNext.items.append(newValue)
        self.items = []


sections = list(getSectionsInput(11))
monkeys = {n: Monkey(n) for n in range(len(sections))}

for lines in sections:
    id = int(lines[0][7:-1])
    items = list(map(int, lines[1][18:].split(', ')))
    op = lines[2][23:].split()
    div = int(lines[3][21:])
    passNext = int(lines[4][29:])
    failNext = int(lines[5][30:])

    m = monkeys[id]
    m.items = items
    m.setTest(op)
    m.divisor = div
    m.passNext = monkeys[passNext]
    m.failNext = monkeys[failNext]

    lcm *= div

for round in range(10000):
    for m in monkeys.values():
        m.process()

counts = [x.counter for x in monkeys.values()]

counts.sort()
print(counts[-1] * counts[-2])