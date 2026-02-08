from shared.utils import getInput

lines = getInput(2, __file__)

validCount = 0
validCount2 = 0

for line in lines:
    minMax, letter, password = line.split()

    letter = letter[0]
    minCount, maxCount = map(int, minMax.split('-'))

    if minCount <= password.count(letter) <= maxCount:
        validCount += 1

    if (password[minCount - 1] == letter) ^ (password[maxCount - 1] == letter):
        validCount2 += 1

print(validCount)
print(validCount2)