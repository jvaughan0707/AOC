from shared.utils import getInput

lines = getInput(5, __file__)

ids = []

for line in lines:
    rowStr = line[:7].replace('F', '0').replace('B', '1')

    rowNum = int(rowStr, 2)

    colStr = line[7:].replace('L', '0').replace('R', '1')

    colNum = int(colStr, 2)

    ids.append(rowNum * 8 + colNum)

ids.sort()

for i in range(len(ids) - 1):
    if ids[i + 1] > ids[i] + 1:
        print(ids[i] + 1)
        break