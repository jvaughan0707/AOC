import math

rawInput = '''Time:        40     92     97     90
Distance:   215   1064   1505   1100'''

[times, distances] = rawInput.splitlines()

times = [''.join(times.split()[1:])]
distances = [''.join(distances.split()[1:])]
print(times, distances)

total = 1
for i in range(len(times)):
    # x(T - x) > D + 1
    # 0 > x^2 - Tx + D + 1
    T = int(times[i])
    D = int(distances[i])
    b = T / 2
    r = math.sqrt(b**2 - D - 1)
    x1 = math.ceil(b - r)
    x2 = math.floor(b + r)

    print(x1, x2)
    total *= (x2 - x1 + 1)

print(total)
