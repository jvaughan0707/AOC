# rawInput = '''Register A: 45483412
# Register B: 0
# Register C: 0
#
# Program: 2,4,1,3,7,5,0,3,4,1,1,5,5,5,3,0'''
#
#
# A = 0
# B = 0
# C = 0
# program = []
#
# for row in rawInput.splitlines():
#     if 'A' in row:
#         A = int(row[12:])
#     if 'B' in row:
#         B = int(row[12:])
#     if 'C' in row:
#         C = int(row[12:])
#
#     if 'Program' in row:
#         program = list(map(int, row[9:].split(',')))
#
# position = 0
#
# output = []
#
# def runOp(code, value):
#     global position
#     global program
#     global A
#     global B
#     global C
#     global output
#     combo = A if value == 4 else B if value == 5 else C if value == 6 else value
#
#     if code == 0:
#         # print('A =>', A, '/', 2 ** combo)
#         A //= (2 ** combo)
#     elif code == 1:
#         # print('B =>', B, '^', value)
#         B ^= value
#     elif code == 2:
#         # print('B => ', combo, '% 8')
#         B = combo % 8
#     elif code == 3:
#         if A > 0:
#             # print('Jump', value)
#             position = value
#             return
#     elif code == 4:
#         # print('B =>', B, '')
#         B ^= C
#     elif code == 5:
#         output.append(combo % 8)
#     elif code == 6:
#         B = A // (2 ** combo)
#     elif code == 7:
#         C = A // (2 ** combo)
#
#     position += 2
#
# print(A,B,C, output)
#
# while position < len(program) - 1:
#     opCode = program[position]
#     operand = program[position + 1]
#
#     print(opCode, operand)
#     runOp(opCode, operand)
#     print(A,B,C, output)
#
#
# print(','.join(str(x) for x in output))


# target 2,4,1,3,7,5,0,3,4,1,1,5,5,5,3,0


def getOutput(A):
    B = C = 0
    # A = 45483412  # must be at least 8 ** 15  (~35 billion)
    output = []
    while A > 0:
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('B = last 3 bits of A')
        B = A % 8 # B = last 3 bits of A
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('Flip last 2 bits')
        B ^= 3 # Flip last 2 bits
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('Remove last B bits from A, take final 3 bits')
        C = (A // 2 ** B) % 8 # A without last B bits
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('remove last 3 bits of A')
        A //= 2 ** 3 # remove last 3 bits of A
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('B XOR C')
        B ^= C
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('B XOR 101')
        B ^= 5
        # print(bin(A)[2:], bin(B)[2:], bin(C)[2:])
        # print('output B')
        output.append(B % 8)

    return output

startA = 0
# target = [5,3,0]
target = [2,4,1,3,7,5,0,3,4,1,1,5,5,5,3,0]

def recurse():
    global startA
    if not target:
        return True
    print(target)

    value = target.pop()
    startA *= 8

    for i in range(0, 8):
        output = getOutput(startA + i)
        print(output)
        if output and output[0] == value:
            startA += i

            if recurse():
                return True
            else:
                startA -= i
        # print(i, output)

    startA /= 8
    startA = int(startA)
    target.append(value)
    return False

recurse()
print(startA)

print(getOutput(236581108670061))
