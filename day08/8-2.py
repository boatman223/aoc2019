with open('input.txt', 'r') as fh:
    image = fh.read().strip('\n')

x = 25
y = 6
split = [image[i:i+(x*y)] for i in range(0, len(image), (x*y))]

finalimage = ['3']*(x*y)
for layer in split:
    for i, pixel in enumerate(layer):
        if finalimage[i] == '3':
            if pixel == '0':
                finalimage[i] = ' '
            elif pixel == '1':
                finalimage[i] = '.'

split = [finalimage[i:i+x] for i in range(0, len(finalimage), x)]
for line in split:
    print(''.join(line))