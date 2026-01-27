from AOC.shared.utils import getSectionsInput

sections = getSectionsInput(4)

numbers = sections[0][0].split(',')

class Board:
    def __init__(self, lines):
        self.sets = []
        self.all = set()

        for line in lines:
            values = line.split()

            self.sets.append(list(values))
            for v in values:
                self.all.add(v)

        cols = []
        for i in range(len(self.sets[0])):
            cols.append(set([s[i] for s in self.sets]))

        self.sets.extend(cols)

    def check(self, number):
        if number in self.all:
            self.all.remove(number)
            for s in self.sets:
                if number in s:
                    s.remove(number)

                    if not s:
                        return True

        return False

boards = []
for section in sections[1:]:
    boards.append(Board(section))

def runGame():
    for number in numbers:
        for board in boards:
            if board.check(number):
                return board, number



while len(boards) >= 1:
    winningBoard, finalNumber = runGame()
    boards.remove(winningBoard)
    print(int(finalNumber) * sum(int(x) for x in winningBoard.all))