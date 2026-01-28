from shared.utils import getInput

lines = getInput(10)

x = 1
cycleValues = [x]
for line in lines:
    if line == 'noop':
        cycleValues.append(x)
        continue
    cycleValues.append(x)
    val = int(line[5:])
    x += val
    cycleValues.append(x)

total = 0
for i in [20, 60, 100, 140, 180, 220]:
    print(cycleValues[i])
    total += i * cycleValues[i - 1]

print(total)

cycle = 0
grid = []
for row in range(6):
    grid.append([])
    for col in range(40):
        v = cycleValues[cycle]
        if col - 1 <= v <= col + 1:
            grid[row].append('#')
        else:
            grid[row].append(' ')
        cycle += 1

for row in grid:
    print(''.join(row))