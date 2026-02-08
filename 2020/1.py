from shared.utils import getInput 

lines = getInput(1, __file__)

numbers = set(map(int, lines))

for n in numbers:
    m = 2020 - n
    if m in numbers:
        print(n, m, n* m)
        break

for a in numbers:
    if a < 2020 // 3:
        continue
    for b in numbers:
        if a < b:
            continue
        if b < (2020 - a) // 2:
            continue
        for c in numbers:
            if b < c:
                continue
            if a + b + c == 2020:
                print(a,b,c, a*b*c)