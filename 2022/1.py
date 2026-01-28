from shared.utils import getSectionsInput

sections = getSectionsInput(1)

totals = []

for section in sections:
    totals.append(sum(map(int, section)))

totals.sort()

print(totals[-1])
print(sum(totals[-3:]))
