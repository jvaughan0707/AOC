from shared.utils import getInput, getNumbers

lines = getInput(14, __file__)

mem = {}

def apply_mask(value, mask):
    value_str = bin(value)[2:]
    value_str = '0' * (36 - len(value_str)) + value_str
    new_value = ''
    for i, c in enumerate(mask):
        if c == 'X':
            new_value += value_str[i]
        else:
            new_value += c

    return int(new_value, 2)

def apply_address_mask(address, mask):
    value_str = bin(address)[2:]
    value_str = '0' * (36 - len(value_str)) + value_str
    new_value = ''
    for i, c in enumerate(mask):
        if c == 'X':
            new_value += 'X'
        elif c == '0':
            new_value += value_str[i]
        else:
            new_value += '1'

    return new_value

def part1():
    current_mask = ''
    for line in lines:
        if line.startswith('mask'):
            current_mask = line[7:]
        else:
            addr, val = getNumbers(line)

            mem[addr] = apply_mask(val, current_mask)

    print(sum(mem.values()))

def part2():
    current_mask = ''

    
    def get_addresses(masked_address):
        results = []
        if not masked_address:
            return ['']
        
        sub_results = get_addresses(masked_address[1:])
        if masked_address[0] == 'X':
            for res in sub_results:
                results.append('0' + res)
                results.append('1' + res)
        else:
            for res in sub_results:
                results.append(masked_address[0] + res)

        return results
    
    for line in lines:
        if line.startswith('mask'):
            current_mask = line[7:]
        else:
            addr, val = getNumbers(line)
            masked_addr = apply_address_mask(addr, current_mask)

            for a in get_addresses(masked_addr):
                mem[int(a, 2)] = val

    print(sum(mem.values()))
part2()
