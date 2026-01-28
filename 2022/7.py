from shared.utils import getInput

lines = getInput(7)

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.files = []
        self.directories = {}
        self.parent = parent
        self.size = 0

    def addSize(self, size):
        self.size += size
        if self.parent:
            self.parent.addSize(size)

    def __repr__(self):
        return f'{self.name}: {self.size}'

root = Directory("/")
current = root
allDirs = [root]

for line in lines:
    if line.startswith('$ cd'):
        target = line[5:]
        print(target)
        if target == '/':
            current = root
        elif target == '..':
            current = current.parent
        else:
            current = current.directories[target]
    elif line.startswith('dir'):
        name = line[4:]
        dir = Directory(name, current)
        allDirs.append(dir)
        current.directories[name] = dir
    elif line == '$ ls':
        continue
    else:
        size, name = line.split()
        size = int(size)
        current.files.append((size, name))
        current.addSize(size)


print(allDirs)
total = 0
for dir in allDirs:
    if dir.size <= 100000:
        total += dir.size

print(total)

requiredSpace = allDirs[0].size - (70000000 - 30000000)
print(requiredSpace)
print(min(list(filter(lambda x: x.size >= requiredSpace, allDirs)), key=lambda x: x.size))