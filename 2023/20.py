import math

from shared.utils import getInput, visualiseGraph

lines = getInput(20)

class Module:
    def __init__(self, name):
        self.name = name
        self.moduleType = ''
        self.outputs = []
        self.inputs = []
        self.state = 0

    def config(self, moduleType, outputs):
        self.moduleType = moduleType
        self.outputs = outputs

    def addInput(self, input):
        self.inputs.append(input)

    def __repr__(self):
        return  f'{self.moduleType} {self.name} {list(map(lambda x: x.name, self.outputs))}'

    def apply(self, source, pulse):
        if self.moduleType == '%':
            if pulse == 0:
                self.state ^= 1
                return self.state
            return -1
        elif self.moduleType == '&':
            if pulse == 1:
                if all(i.state == 1 for i in self.inputs):
                    self.state = 0
                    return 0
            self.state = 1
            return 1
        elif self.moduleType == 'b':
            self.state = pulse
            return pulse
        return -1

modules = {}

def getOrCreate(name):
    if name not in modules:
        modules[name] = Module(name)
    return modules[name]


for line in lines:
    l, r = line.split(' -> ')
    t = l[0]
    n = l[1:] if t in ('%', '&') else l
    o = r.split(', ')

    module = getOrCreate(n)
    outputs = list(map(getOrCreate, o))
    module.config(t, outputs)
    for output in outputs:
        output.addInput(module)

lowPulseCount = 0
highPulseCount = 0

vf = modules['vf']
endNodes = {}

for node in vf.inputs:
    endNodes[node.name] = []

presses = 0
while presses < 10000:
    presses += 1
    pulses = { 'broadcaster': [(None, 0)] }
    lowPulseCount += 1
    steps = 0
    while pulses:
        steps += 1
        newPulses = {}
        for name, inputs in pulses.items():
            for input in inputs:
                result = modules[name].apply(*input)

                if result >= 0:
                    for o in modules[name].outputs:
                        if o.name not in newPulses:
                            newPulses[o.name] = []
                        newPulses[o.name].append((name, result))
                        if result == 0:
                            lowPulseCount += 1
                        else:
                            highPulseCount += 1

        vf = modules['vf']

        for node in vf.inputs:
            if node.state == 1:
                endNodes[node.name].append((presses, steps))
        # print(newPulses)
        pulses = newPulses.copy()


# print(lowPulseCount)
# print(highPulseCount)
# print(lowPulseCount * highPulseCount)

for x,y in endNodes.items():
    print(x, y)

def key(module):
    if module.name == 'broadcaster':
        return 'broadcaster'
    return f'{module.moduleType}{module.name}'


adjMap = {}
for module in modules.values():
    adjMap[key(module)] = list(map(key, module.outputs))

# print(adjMap)

# visualiseGraph(adjMap, directed = True, colorMap=lambda x: 'red' if x[0] == '&' else 'blue' if x[0] == '%' else 'green')

periodMap = {
    x: y[-1][0] - y[0][0] for x, y in endNodes.items()
}

print(periodMap)

print(math.lcm(*periodMap.values()))