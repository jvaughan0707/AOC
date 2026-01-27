from AOC.shared.utils import getInput

tail = None

lines = getInput(9)

class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.child = None
        self.i = 0
        self.j = 0
        self.positions = {(0, 0)}

    def addChildren(self, number):
        global tail
        if number == 0:
            tail = self
            return

        self.child = Node(self)
        self.child.addChildren(number - 1)

    def updatePosition(self, iDiff, jDiff):
        self.i += iDiff
        self.j += jDiff
        self.positions.add((self.i, self.j))

        if self.child:
            self.updateChildPosition()

    def updateChildPosition(self):
        c = self.child
        iDiff = self.i - c.i
        jDiff = self.j - c.j
        iNorm = int(iDiff / max(abs(iDiff), 1))
        jNorm = int(jDiff / max(abs(jDiff), 1))

        if abs(iDiff) <= 1 and abs(jDiff) <= 1:
            return

        c.updatePosition(iNorm, jNorm)


head = Node()
head.addChildren(9)

for line in lines:
    d, l = line.split()
    l = int(l)

    for x in range(l):
        if d == 'D':
            head.updatePosition(1, 0)
        elif d == 'U':
            head.updatePosition(-1, 0)
        elif d == 'R':
            head.updatePosition(0, 1)
        else:
            head.updatePosition(0, -1)

print(tail.positions)
print(len(tail.positions))
