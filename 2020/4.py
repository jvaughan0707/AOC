from shared.utils import getSectionsInput
import re

sections = getSectionsInput(4, __file__)
requiredFields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
]

validCount = 0
validCount2 = 0

def isValidNumber(text, minValue, maxValue):
    return text.isdigit() and minValue <= int(text) <= maxValue

for section in sections:
    values = {}

    for line in section:
        for pair in line.split():
            k, v = pair.split(':')
            values[k] = v


    if all(f in values for f in requiredFields):
        validCount += 1

        byr = values['byr']
        iyr = values['iyr']
        eyr = values['eyr']
        hgt = values['hgt']
        hcl = values['hcl']
        ecl = values['ecl']
        pid = values['pid']

        if not isValidNumber(byr, 1920,2002):
            continue
        if not isValidNumber(iyr, 2010, 2020):
            continue
        if not isValidNumber(eyr, 2020, 2030):
            continue
        if hgt[-2:] == 'cm':
            if not isValidNumber(hgt[:-2], 150, 193):
                continue
        elif hgt[-2:] == 'in':
            if not isValidNumber(hgt[:-2], 59, 76):
                continue
        else:
            continue
        if not re.match(r'#([a-f]|[0-9]){6}', hcl):
            continue
        if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            continue
        if len(pid) != 9 or not isValidNumber(pid, 0, 10**9):
            continue

        validCount2 += 1

    print(values)

print(validCount)
print(validCount2)
