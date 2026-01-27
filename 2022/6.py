from AOC.shared.utils import getInput

data = getInput(6)[0]

i = 0
chunkSize = 14
for i in range(len(data) - chunkSize):
    section = data[i:i+chunkSize]
    duplicate = False
    for t in section:
        if section.count(t) > 1:
            duplicate = True
            break
    if not duplicate:
        print(section)
        break

print(i + chunkSize)


