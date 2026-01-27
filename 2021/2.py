from AOC.shared.utils import getInput

lines = getInput(2)

i = j = 0
for line in lines:
    direction, amount = line.split(' ')

    if direction == 'forward':
        j += int(amount)
    elif direction == 'down':
        i += int(amount)
    elif direction == 'up':
        i -= int(amount)

print(i, j)
print(i * j)

i = j = 0
aim = 0

for line in lines:
    direction, amount = line.split(' ')
    if direction == 'forward':
        j += int(amount)
        i += int(amount) * aim
    elif direction == 'down':
        aim += int(amount)
    elif direction == 'up':
        aim -= int(amount)

print(i, j)
print(i * j)