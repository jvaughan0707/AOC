from AOC.shared.utils import expandWithPlaceholders

# start = [125, 17]
start = [0 ,7 ,6618216, 26481, 885 ,42, 202642, 8791]

def expand(value):
    if value == 0:
        return [1]
    elif len(str(value)) % 2 == 0:
        s = str(value)
        l = s[:len(s)//2]
        r = s[len(s)//2:]
        return [int(l), int(r)]
    else:
        return [value * 2024]


print(expandWithPlaceholders(start, expand, 75, lambda x: 1))