from shared.utils import getInput

lines = getInput(25)

def snafuToDec(input):
    unit = 1
    output = 0
    for char in reversed(input):
        if char == '-':
            output -= unit
        elif char == '=':
            output -= 2 * unit
        else:
            output += int(char) * unit
        unit *= 5

    return output

def decToSnafu(input):
    unit = 1
    output = ''

    while unit <= input:
        remainder = input % (5 * unit) // unit
        if remainder == 3:
            output = '=' + output
            input += 2 * unit
        elif remainder == 4:
            output = '-' + output
            input += unit
        else:
            output = str(remainder) + output

        unit *= 5

    return output

total = 0

for line in lines:
    d = snafuToDec(line)
    total += d

print(total)
print(decToSnafu(total))