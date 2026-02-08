from shared.utils import getSectionsInput

sections = getSectionsInput(6, __file__)

unionSets = []
intersectionSets = []

for section in sections:
    unionSet = set()
    intersectionSet = set()

    for i in range(len(section)):
        line = set(section[i])
        unionSet |= line

        if i == 0:
            intersectionSet = set(line)
        else:
            intersectionSet &= line

    unionSets.append(unionSet)
    intersectionSets.append(intersectionSet)

print(unionSets)
print(intersectionSets)
print(sum(len(s) for s in unionSets))
print(sum(len(s) for s in intersectionSets))