import re
rawInput = ''''''
workflowList, inputList= rawInput.split('\n\n')
workflows = {}
def addWorkflowInput(name, input):
    w = workflows[name]
    w.addInput(input)
class Workflow:
    def __init__(self, name, conditions):
        self.name = name 
        self.conditions = []
        self.inputs=[]
        for condition in conditions:
            if not condition:
                continue
            parts = re.split('[<>:]', condition)
            if len(parts) == 1:
                self.conditions.append((None, None, None, condition))
                continue
            self.conditions.append((parts[0], int(parts[1]), '<' in condition, parts[2]))
            
    def addInput(self, input):
        self.inputs.append(input)
        for condition in self.conditions:
            letter, limit, isUpper, target = condition
            
            if not letter:
                addWorkflowInput(target, input)
                continue
            
            input1 = input.copy()
            input2 = input.copy()
            rangeMin, rangeMax = input[letter]
            if isUpper:
                if limit <= rangeMin:
                    continue
                if limit > rangeMax:
                    addWorkflowInput(target, input)
                    break
                
                input1[letter] = (rangeMin, limit - 1)
                input2[letter] = (limit, rangeMax)
            else:
                if limit >= rangeMax:
                    continue
                if limit < rangeMin:
                    addWorkflowInput(target, input)
                input1[letter] = (limit + 1, rangeMax)
                input2[letter] = (rangeMin, limit)
            
            input = input2
            addWorkflowInput(target, input1)
        
for line in workflowList.splitlines():
    parts = re.split('[\{\},]', line)
    
    workflows[parts[0]] = Workflow(parts[0],parts[1:])
    
workflows['A'] = Workflow('A', [])
workflows['R'] = Workflow('R', [])
initialInput = {
    'x':(1, 4000),
    'm':(1, 4000),
    'a':(1, 4000),
    's':(1, 4000),
}
addWorkflowInput('in', initialInput)
aInputs = workflows['A'].inputs
def checkInput(input):
    for aRange in aInputs:
        match = True
        for key in input:
            if input[key] < aRange[key][0]:
                match = False
                break
            if input[key] > aRange[key][1]:
                match = False
                break
        if match:
            return True
    return False
total = 0
#for line in inputList.splitlines():
#    parts = line[1:-1].split(',')
#    
#    sum = 0
#    input= {}
#    for p in parts:
#        key, value = p.split('=')
#        input[key] = int(value)
#        sum += int(value)
#    if checkInput(input):
#        total += sum
        
for input in aInputs:
    product = 1
    for key in input:
        product *= input[key][1] - input[key][0] + 1
        
    total += product   
print(total)
