with open('input.txt', 'r') as fh:
    image = fh.read().strip('\n')

x = 25
y = 6
split = [image[i:i+(x*y)] for i in range(0, len(image), (x*y))]

lowest = 999
for i in split:
    zerocount = i.count('0')
    if zerocount < lowest:
        lowest = zerocount
        layer = i

print(layer.count('1')*layer.count('2'))