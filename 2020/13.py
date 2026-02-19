from shared.utils import getInput
import math

lines = getInput(13, __file__)

minTime = int(lines[0])
allBuses = [int(x) if x != 'x' else 'x' for x in lines[1].split(',')]
buses = [int(x) for x in lines[1].split(',') if x != 'x']

minBus = min(buses)

def part1():
    for i in range(minBus):
        t = minTime + i

        for b in buses:
            if t % b == 0:
                return b * i
            
print(part1())
    
def part2():
    # x0 = 7, t == 0 (%7)
    # x1 = 13, x1 % x0 = 6, s * 6 == 1 (%7)
    
    # t= 77 + k(lcm(7.13)), t+1 = 78

    currentBaseTime = 0
    lcm = 1

    for i, bus in enumerate(allBuses):
        if bus == 'x':
            continue
        if currentBaseTime == 0:
            currentBaseTime = bus + i
            lcm = bus
            continue

        for j in range(0, bus):
            if (currentBaseTime + j * lcm + i) % bus == 0:
                currentBaseTime += j * lcm
                break


        lcm = math.lcm(lcm, bus)
        print(bus, currentBaseTime, lcm)

    return currentBaseTime

print(part2())

