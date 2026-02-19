from shared.utils import getInput, orderedDirections, compassDirections, add, scale, rotate
lines = getInput(12, __file__)

dirIndex = 1

position = (0,0)

for line in lines:
    d = line[0]
    v = int(line[1:])

    if d in compassDirections:
        position = add(position, scale(compassDirections[d], v))
    elif d == 'F':
        position = add(position, scale(orderedDirections[dirIndex], v))
    elif d == 'R':
        dirIndex += v // 90
        dirIndex %= 4
    elif d == 'L':
        dirIndex -= v // 90
        dirIndex %= 4

print(sum([abs(t) for t in position]))

position = (0,0)
waypoint = (-1, 10)
for line in lines:
    d = line[0]
    v = int(line[1:])
    
    if d in compassDirections:
        waypoint = add(waypoint, scale(compassDirections[d], v))
    elif d == 'F':
        position = add(position, scale(waypoint, v))
    elif d == 'R':
        waypoint = rotate(waypoint, -v)
    elif d == 'L':
        waypoint = rotate(waypoint, v)

print(round(sum([abs(t) for t in position])))