

def expandWithPlaceholders(values, expandFunc, iterations, sizeFunc = None):
    expansionMap = {}
    if sizeFunc is None:
        sizeFunc = lambda x: len(x)

    class Item:
        def __init__(self, value, parent = None):
            self.value = value
            self.parent = parent

        def __repr__(self):
            return str(self.value)

        def updateParents(self, depth = 2):
            current = self.parent

            while current.parent:
                parent = current.parent
                if len(expansionMap[parent.value]) < depth + 1:
                    expansionMap[parent.value].append(0)
                expansionMap[parent.value][depth] += self.getSize()
                depth += 1
                current = parent

        def getSize(self):
            return sizeFunc(self.value)

    class Placeholder(Item):
        def __init__(self, value, parent, count):
            super().__init__(value, parent)
            self.count = count

        def __repr__(self):
            return f'({self.value})*{self.count}'

        def updateParents(self):
            super().updateParents(1 + self.count)

        def getSize(self):
            return expansionMap[self.value][self.count]

    items = []

    for v in values:
        items.append(Item(v))

    def recurse(currentItems, i = 1):
        newItems = []
        totalLength = 0
        for item in currentItems:
            if type(item) is Placeholder:
                item.count += 1
                newItems.append(item)
            elif item.value in expansionMap:
                newItems.append(Placeholder(item.value, item, 1))
            else:
                expanded = expandFunc(item.value)
                expandedLength = 0
                for v in expanded:
                    newItems.append(Item(v, item))
                    expandedLength += sizeFunc(v)
                expansionMap[item.value] = [sizeFunc(item.value), expandedLength]

        for item in newItems:
            item.updateParents()
            totalLength += item.getSize()

        # print('newItems:', newItems, 'length:', totalLength, 'map:', expansionMap)

        i += 1
        if i > iterations:
            return totalLength
        else:
            return recurse(newItems, i)

    return recurse(items)

def flipGrid(grid):
    newRows = []

    isStr = type(grid[0]) == str

    for j in range(len(grid[0])):
        newRow = []
        for i in range(len(grid)):
            newRow.append(grid[i][j])

        if isStr:
            newRows.append(''.join(newRow))
        else:
            newRows.append(newRow)
    return newRows

def sub (p1, p2):
    return tuple(p1[i] - p2[i] for i in range(len(p1)))

def add(p1, p2):
    return tuple(p1[i] + p2[i] for i in range(len(p1)))

def scale(p, s):
    return tuple(p[i] * s for i in range(len(p)))

def dot(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]

def isOob(grid, p):
    return not(0 <= p[0] < len(grid) and 0 <= p[1] < len(grid[0]))

def get(grid, p):
    if isOob(grid, p):
        return None
    return grid[p[0]][p[1]]

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
directions = {
    'u': up,
    'd': down,
    'l': left,
    'r': right
}

def getInput(day):
    with open(f'inputs/{day}') as f:
        return f.read().splitlines()

def getGridInput(day):
    lines = getInput(day)

    grid = []
    for line in lines:
        grid.append(list(line))

    return grid

def getFirstInGrid(grid, char):
    width = len(grid[0])
    height = len(grid)

    for i in range(height):
        for j in range(width):
            if grid[i][j] == char:
                return i, j

def getMinDist(adjacencyMatrix, start, end):
    distMap = {x: float('inf') for x in adjacencyMatrix}
    exploredNodes = set()
    explorableNodes = {start}
    distMap[start] = 0

    while True:
        minUnexploredNode = min(explorableNodes, key=distMap.get)

        if minUnexploredNode == end:
            break
        dist = distMap[minUnexploredNode]
        explorableNodes.remove(minUnexploredNode)
        exploredNodes.add(minUnexploredNode)

        neighbours = adjacencyMatrix[minUnexploredNode]
        for neighbour, nDist in neighbours.items():
            if neighbour in exploredNodes:
                continue

            distMap[neighbour] = min(dist + nDist, distMap[neighbour])

            # if nDist > 0:
            explorableNodes.add(neighbour)

    # print(distMap)
    return distMap[end]

def visualiseGraph(adjacencyMatrix, directed = False, weighted = False, colorMap = None, name = 'graph'):
    from pyvis.network import Network
    import os
    import webbrowser

    net = Network('1500px', '1500px', directed=directed)

    for k in adjacencyMatrix.keys():
        color = 'black'
        if colorMap:
            color = colorMap(k)
        net.add_node(str(k), color=color)

    for source, targets in adjacencyMatrix.items():
        for target in targets:
            if weighted:
                net.add_edge(str(source), str(target[0]), color='black', label=str(target[1]))
            else:
                net.add_edge(str(source), str(target), color='black')

    net.show_buttons(filter_=['physics'])
    name = name + '.html'
    net.show(name, notebook=False)
    webbrowser.open('file://' + os.path.realpath(name))

def getNetwork(grid, adjFunc = None, wallSymbol = '#'):
    nodes = {}
    width = len(grid[0])
    height = len(grid)
    for i in range(height):
        for j in range(width):
            current = grid[i][j]
            if current == wallSymbol:
                continue
            nodes[(i,j)] = []
            for direction in directions:
                neighbourPoint = add((i,j), directions[direction])
                neighbourSymbol = get(grid, neighbourPoint)
                if not neighbourSymbol or neighbourSymbol == wallSymbol:
                    continue
                if not adjFunc or adjFunc(current, neighbourPoint, direction):
                    nodes[(i,j)].append(neighbourPoint)
    return nodes