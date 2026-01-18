from AOC.shared.utils import getInput, up as N, down as S, left as W, right as E, add

lines = getInput(23)

NE = add(N,E)
NW = add(N,W)
SE = add(S,E)
SW = add(S,W)

directionGroups = [(N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)]

elves = {}
nextPoints = {}

class Elf:
    def __init__(self, startingPos):
        self.pos = startingPos
        self.next = startingPos

    def checkNext(self):
        self.next = self.pos

        availableDirections = []
        for dg in directionGroups:
            if not any([add(d, self.pos) in elves for d in dg]):
                availableDirections.append(dg[0])

        if len(availableDirections) == 4:
            return

        if availableDirections:
            self.next = add(self.pos, availableDirections[0])

        if self.next not in nextPoints:
            nextPoints[self.next] = 1
        else:
            nextPoints[self.next] += 1

    def move(self):
        if self.pos != self.next and nextPoints[self.next] == 1:
            del elves[self.pos]
            self.pos = self.next
            elves[self.pos] = self
            return True
        return False

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == '#':
            elves[(i, j)] = Elf((i, j))

r = 0
while r < 1000:
    r += 1
    for elf in elves.values():
        elf.checkNext()

    anyMoved = False
    for elf in list(elves.values()):
        anyMoved |= elf.move()

    nextPoints = {}
    minI = min([elf.pos[0] for elf in elves.values()])
    minJ = min([elf.pos[1] for elf in elves.values()])
    maxI = max([elf.pos[0] for elf in elves.values()])
    maxJ = max([elf.pos[1] for elf in elves.values()])

    # print(minI, minJ, maxI, maxJ)

    # for i in range(minI, maxI+1):
    #     row = ''
    #     for j in range(minJ, maxJ+1):
    #         if (i, j) in elves:
    #             row += '#'
    #         else:
    #             row += '.'
    #
    #     print(row)
    directionGroups = directionGroups[1:] + [directionGroups[0]]
    # print()

    if not anyMoved:
        break

print((maxI - minI + 1) * (maxJ - minJ + 1) - len(elves))
print(r)
# < 6320