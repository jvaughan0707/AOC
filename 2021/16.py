from AOC.shared.utils import getInput

hexInput = getInput(16)[0]

hexMap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

binString = ''.join([hexMap[h] for h in hexInput])
print(binString)
print(len(binString))

class Packet:
    def __init__(self, version, typeId, value, totalLength):
        self.version = version
        self.typeId = typeId
        self.subPackets = []
        self.value = value
        self.totalLength = totalLength

    def __repr__(self):
        if self.subPackets:
            return f'Packet(Version:{self.version}, Type:{self.typeId}, Length:{self.totalLength}, SubPackets:{self.subPackets})'
        else:
            return f'Packet(Version:{self.version}, Type:{self.typeId}, Length:{self.totalLength}, Value:{self.value})'

    def getVersionSum(self):
        return self.version + sum(s.getVersionSum() for s in self.subPackets)

    def getValue(self):
        if not self.subPackets:
            return self.value
        if self.typeId == 0:
            return sum(s.getValue() for s in self.subPackets)
        if self.typeId == 1:
            product = 1
            for s in self.subPackets:
                product *= s.getValue()
            return product
        if self.typeId == 2:
            return min(s.getValue() for s in self.subPackets)
        if self.typeId == 3:
            return max(s.getValue() for s in self.subPackets)
        if self.typeId == 5:
            return 1 if self.subPackets[0].getValue() > self.subPackets[1].getValue() else 0
        if self.typeId == 6:
            return 1 if self.subPackets[0].getValue() < self.subPackets[1].getValue() else 0
        if self.typeId == 7:
            return 1 if self.subPackets[0].getValue() == self.subPackets[1].getValue() else 0

def processLiteral(bits):
    print('literal:', bits)
    outputStr = ''
    chunks = 0
    while True:
        chunks += 1
        outputStr += bits[1:5]

        if bits[0] == '0':
            break

        bits = bits[5:]

    print(outputStr)
    return int(outputStr, 2), chunks * 5

def getPackets(bits, number = 0):
    n = 0
    packets = []
    while (number == 0 or n < number) and bits and int(bits, 2) > 0:
        n += 1
        versionStr = bits[:3]
        bits = bits[3:]
        version = int(versionStr, 2)
        typeStr = bits[:3]
        bits = bits[3:]
        typeId = int(typeStr, 2)

        # print('v', versionStr, version)
        # print('t', typeStr, typeId)

        if typeId == 4:
            value, length = processLiteral(bits)
            # print('literal value:', value, 'length:', length)
            packet = Packet(version, typeId, value, length + 6)
            packets.append(packet)
            bits = bits[length:]
            continue

        lengthTypeStr = bits[0]
        bits = bits[1:]
        # print('length type:', lengthTypeStr)

        packet = Packet(version, typeId, 0, 7)
        packets.append(packet)

        if lengthTypeStr == '0':
            length = int(bits[:15], 2)
            packet.totalLength += 15
            print('length:', length)
            subPackets = getPackets(bits[15:15+length])
        else:
            length = int(bits[:11], 2)
            packet.totalLength += 11
            print('number:', length)
            subPackets = getPackets(bits[11:], length)

        packet.subPackets = subPackets
        packet.totalLength += sum(p.totalLength for p in subPackets)
        bits = bits[packet.totalLength - 7:]

    if number and n < number:
        raise Exception('not enough sub packets. Expected: ' + str(number) + ', Actual: ' + str(n))
    # print('return packets')
    return packets

topLevelPacket = getPackets(binString)[0]

print(topLevelPacket)

totalVersion = topLevelPacket.getVersionSum()

print(totalVersion)
print(topLevelPacket.getValue())
