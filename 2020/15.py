from shared.utils import getInput
import numpy as np

numbers = getInput(15, __file__)[0].split(',')

num_index = {}

last_number = 0
current_index = 0

for num in numbers:
    num = int(num)
    num_index[num] = current_index
    print(current_index + 1, num)
    last_number = num
    current_index += 1

del num_index[last_number]

while current_index < 30000000:
    new_number = 0
    if last_number in num_index:
        gap = current_index - 1 - num_index[last_number]
        new_number = gap

    num_index[last_number] = current_index - 1
    last_number = new_number

    if current_index % 100000 == 0:
        print(current_index + 1, new_number)
    current_index += 1

print(last_number)