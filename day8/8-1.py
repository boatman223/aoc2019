with open('input.txt', 'r') as fh:
    image = fh.read().strip('\n')

length = 25*6
split = list(map(''.join, zip(*[iter(image)]*length)))

lowest = 999
for i in split:
    zerocount = i.count('0')
    if zerocount < lowest:
        lowest = zerocount
        layer = i

print(lowest, layer)
print(layer.count('1')*layer.count('2'))