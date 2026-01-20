from AOC.shared.utils import getSectionsInput, expandWithPlaceholders

[template], rulesList = getSectionsInput(14)

rulesMap = {
    x:y for (x,y) in [r.split(' -> ') for r in rulesList]
}

def expand(text):
    newText = ''
    for i in range(len(text) - 1):
        a = text[i]
        b = text[i + 1]

        newText += a
        newText += rulesMap[a+b]

    newText += template[-1]
    return newText

def expandPair(text):
    a,b = text
    c = rulesMap[a+b]
    return [a + c, c + b]
#
# for t in range(10):
#     template = expand(template)
#     print(template)

def getFrequencies(text):
    frequencies = {}
    for c in text:
        if c in frequencies:
            frequencies[c] += 1
        else:
            frequencies[c] = 1

    return frequencies

initialState= [template[i] + template[i+1] for i in range(len(template)-1)]

def sizeFunc(item):
    return getFrequencies(item)

def addSizeFunc(current, new):
    if current == 0:
        current ={}
    else:
        current = current.copy()

    for c in new:
        if c in current:
            current[c] += new[c]
        else:
            current[c] = new[c]

    return current

frequencyMap = expandWithPlaceholders(initialState, expandPair, 40, sizeFunc, addSizeFunc)

# each letter other than the first and last is part of two pairs. Increase count of F & L by 1 then halve everything
frequencyMap[template[0]] += 1
frequencyMap[template[-1]] += 1

for c in frequencyMap:
    frequencyMap[c] //= 2

print(frequencyMap)


print(max(frequencyMap.values()) - min(frequencyMap.values()))